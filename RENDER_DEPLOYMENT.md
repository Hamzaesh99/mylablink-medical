# دليل النشر على Render
## Render Deployment Guide

هذا الدليل يشرح كيفية نشر تطبيق MyLabLink على منصة Render.

### الملفات المطلوبة ✅

تم إنشاء الملفات التالية للنشر:

1. **build.sh** - سكريبت بناء المشروع
2. **render.yaml** - ملف تكوين Render (اختياري)
3. **.gitattributes** - لضمان نهايات الأسطر الصحيحة

### الخطوات المطلوبة للنشر:

#### 1. إعداد المشروع على Render

1. قم بزيارة [Render.com](https://render.com) وسجل الدخول
2. اختر "New +" ثم "Web Service"
3. اربط مستودع Git الخاص بك

#### 2. إعدادات Web Service

- **Name**: mylablink
- **Region**: اختر المنطقة الأقرب لك
- **Branch**: main (أو الفرع الرئيسي لديك)
- **Runtime**: Python 3
- **Build Command**: `./build.sh`
- **Start Command**: `cd backend && gunicorn mylablink_python.wsgi:application`

#### 3. متغيرات البيئة (Environment Variables)

قم بإضافة المتغيرات التالية:

```bash
# Django Settings
DJANGO_SECRET_KEY=<your-secret-key-here>
DEBUG=False

# Database (سيتم توفيرها من Render Database)
DATABASE_URL=<from-render-database>

# Email Settings
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=<your-email>
EMAIL_HOST_PASSWORD=<your-app-password>
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=MyLabLink <no-reply@mylablink.com>

# Site Settings
SITE_BASE_URL=https://your-app.onrender.com
```

#### 4. إنشاء قاعدة البيانات

1. في لوحة تحكم Render، اختر "New +" ثم "PostgreSQL" (أو MySQL)
2. اسم قاعدة البيانات: `mylablink-db`
3. بعد إنشاء قاعدة البيانات، انسخ `DATABASE_URL`
4. أضف `DATABASE_URL` إلى متغيرات البيئة في Web Service

> **ملاحظة**: إذا كنت تستخدم MySQL، ستحتاج لتعديل إعدادات DATABASES في settings.py لتحليل DATABASE_URL

#### 5. الملفات الثابتة (Static Files)

الإعدادات الحالية في `settings.py`:
```python
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
ALLOWED_HOSTS = ['.onrender.com', '127.0.0.1', 'localhost']
```

السكريبت `build.sh` سيقوم تلقائياً بتشغيل:
```bash
python manage.py collectstatic --noinput
```

#### 6. النشر

1. اضغط على "Create Web Service"
2. Render سيقوم بـ:
   - تشغيل `build.sh`
   - تثبيت المتطلبات من `requirements.txt`
   - جمع الملفات الثابتة
   - تشغيل migrations
   - بدء الخادم باستخدام gunicorn

#### 7. التحقق من النشر

بعد اكتمال النشر:
- زر الموقع على `https://your-app.onrender.com`
- تحقق من واجهة المسؤول: `https://your-app.onrender.com/admin/`
- اختبر تسجيل الدخول والتسجيل

### المشاكل الشائعة وحلولها:

#### مشكلة: الملفات الثابتة لا تظهر
**الحل**: تأكد من:
- تشغيل `collectstatic` في build.sh
- إعدادات STATIC_ROOT صحيحة
- WhiteNoise مثبت ومفعّل (موصى به)

#### مشكلة: خطأ في الاتصال بقاعدة البيانات
**الحل**: 
- تحقق من DATABASE_URL
- تأكد من أن قاعدة البيانات تعمل
- راجع إعدادات DATABASES في settings.py

#### مشكلة: Internal Server Error (500)
**الحل**:
- راجع السجلات (Logs) في Render
- تأكد من `DEBUG=False`
- تحقق من ALLOWED_HOSTS

### ملاحظات إضافية:

1. **WhiteNoise** (موصى به لتقديم الملفات الثابتة):
   - متأكد من وجوده في requirements.txt
   - أضفه إلى MIDDLEWARE في settings.py

2. **الأمان**:
   - لا تحفظ DJANGO_SECRET_KEY في الكود
   - استخدم متغيرات البيئة دائماً
   - تأكد من DEBUG=False في الإنتاج

3. **النسخ الاحتياطي**:
   - قم بنسخ احتياطي لقاعدة البيانات بانتظام
   - Render يوفر backups تلقائية للخطط المدفوعة

### موارد مفيدة:

- [Render Django Documentation](https://render.com/docs/deploy-django)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)

---

تم إنشاء هذا الدليل بتاريخ: 2025-12-16
