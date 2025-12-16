# ✅ Checklist للنشر على Render
## Pre-Deployment Checklist

استخدم هذا الـ Checklist للتأكد من جاهزية المشروع للنشر.

---

## 📝 قبل رفع الكود

### ✅ الملفات الأساسية
- [x] `build.sh` - موجود في الجذر
- [x] `backend/Procfile` - موجود في مجلد backend
- [x] `render.yaml` - موجود في الجذر (اختياري)
- [x] `requirements-render.txt` - موجود في الجذر
- [x] `.gitattributes` - موجود في الجذر
- [x] `backend/mylablink_python/settings_production.py` - موجود

### ✅ المتطلبات
- [x] `gunicorn` موجود في requirements.txt
- [x] `whitenoise` موجود في requirements.txt
- [x] `psycopg2-binary` موجود في requirements-render.txt
- [x] `dj-database-url` موجود في requirements-render.txt

### ✅ إعدادات Django
- [x] `ALLOWED_HOSTS` يحتوي على `.onrender.com`
- [x] `WhiteNoise` مضاف إلى MIDDLEWARE
- [x] `STATIC_ROOT` محدد بشكل صحيح
- [x] `STATICFILES_STORAGE` مضبوط لـ WhiteNoise

---

## 🚀 على منصة Render

### 1️⃣ إنشاء PostgreSQL Database
- [ ] اسم Database: `mylablink-db`
- [ ] المنطقة: اختر الأقرب لك
- [ ] نسخ `Internal Database URL`

### 2️⃣ إنشاء Web Service
- [ ] اسم Service: `mylablink`
- [ ] ربط Git repository
- [ ] Branch: `main` (أو الفرع الصحيح)
- [ ] Runtime: Python 3
- [ ] Build Command: `./build.sh`
- [ ] Start Command: `cd backend && gunicorn mylablink_python.wsgi:application`

### 3️⃣ متغيرات البيئة الأساسية
- [ ] `DJANGO_SETTINGS_MODULE=mylablink_python.settings_production`
- [ ] `DEBUG=False`
- [ ] `DATABASE_URL=<من PostgreSQL Database>`
- [ ] `DJANGO_SECRET_KEY` (سيتم توليده تلقائياً)

### 4️⃣ متغيرات البيئة للبريد الإلكتروني (موصى به)
- [ ] `EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend`
- [ ] `EMAIL_HOST=smtp.gmail.com`
- [ ] `EMAIL_PORT=587`
- [ ] `EMAIL_HOST_USER=<your-email@gmail.com>`
- [ ] `EMAIL_HOST_PASSWORD=<your-app-password>`
- [ ] `EMAIL_USE_TLS=True`
- [ ] `DEFAULT_FROM_EMAIL=MyLabLink <no-reply@mylablink.com>`

### 5️⃣ متغيرات البيئة الإضافية (اختياري)
- [ ] `SITE_BASE_URL=https://mylablink.onrender.com`
- [ ] `SECURE_SSL_REDIRECT=True`
- [ ] `CORS_ALLOW_ALL=False`

---

## 🔍 بعد النشر - التحقق

### ✅ التحقق من Build
- [ ] Build logs لا تحتوي على أخطاء
- [ ] `collectstatic` تم بنجاح
- [ ] `migrate` تم بنجاح
- [ ] الخادم بدأ بنجاح

### ✅ التحقق من الموقع
- [ ] الصفحة الرئيسية تعمل: `https://your-app.onrender.com`
- [ ] لوحة الإدارة تعمل: `https://your-app.onrender.com/admin/`
- [ ] Static files (CSS/JS) تحمّل بشكل صحيح
- [ ] الصور والأيقونات تظهر

### ✅ التحقق من الوظائف
- [ ] تسجيل الدخول يعمل
- [ ] إنشاء حساب جديد يعمل
- [ ] البريد الإلكتروني يُرسل بشكل صحيح
- [ ] قاعدة البيانات تعمل (إنشاء/قراءة/تحديث/حذف)

---

## 🐛 في حالة وجود مشاكل

### ❌ Build Failed
1. [ ] راجع Build Logs في Render
2. [ ] تحقق من `build.sh` syntax
3. [ ] تأكد من `requirements.txt` صحيح
4. [ ] تأكد من Python version متوافق

### ❌ Application Error (500)
1. [ ] راجع Application Logs
2. [ ] تحقق من `DATABASE_URL`
3. [ ] تحقق من `DJANGO_SETTINGS_MODULE`
4. [ ] تأكد من migrations تمت بنجاح

### ❌ Static Files لا تظهر
1. [ ] تحقق من `collectstatic` في build logs
2. [ ] تأكد من WhiteNoise في MIDDLEWARE
3. [ ] تحقق من `STATICFILES_STORAGE`

### ❌ DisallowedHost Error
1. [ ] أضف domain إلى Environment Variables:
   ```
   ALLOWED_HOSTS=your-app.onrender.com
   ```

### ❌ Database Connection Error
1. [ ] تحقق من `DATABASE_URL` في Environment
2. [ ] تأكد من Database متصلة وتعمل
3. [ ] راجع Database logs في Render

---

## 🔄 التحديثات المستقبلية

عند كل تحديث:

1. [ ] اختبر التغييرات محلياً
2. [ ] رفع الكود إلى Git:
   ```bash
   git add .
   git commit -m "Description"
   git push
   ```
3. [ ] Render سينشر تلقائياً
4. [ ] راجع Logs للتأكد من نجاح النشر

---

## 📊 المراقبة المستمرة

### يومياً:
- [ ] راجع Application Logs لأي أخطاء
- [ ] تحقق من توفر الخدمة (uptime)

### أسبوعياً:
- [ ] راجع استخدام Database
- [ ] تحقق من رسائل البريد الإلكتروني

### شهرياً:
- [ ] نسخ احتياطي لقاعدة البيانات
- [ ] تحديث المكتبات (security updates)

---

## 🎯 النشر الناجح!

إذا كانت جميع النقاط أعلاه ✅، تهانينا! 🎉

المشروع الآن:
- ✅ على الإنتاج
- ✅ آمن
- ✅ جاهز للاستخدام

---

**آخر تحديث:** 2025-12-16  
**الحالة:** جاهز للنشر ✅
