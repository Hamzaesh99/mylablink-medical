# 🚀 أوامر سريعة - Quick Commands
## Render Deployment - Useful Commands

---

## 📦 قبل النشر - Pre-Deployment

### رفع الكود إلى Git
```bash
cd C:\Users\HP\Desktop\mylablink-medical-lab
git add .
git commit -m "Ready for Render deployment"
git push origin main
```

### اختبار build.sh محلياً (Git Bash / WSL)
```bash
chmod +x build.sh
./build.sh
```

### اختبار settings_production.py
```bash
cd backend
export DJANGO_SETTINGS_MODULE=mylablink_python.settings_production
python manage.py check --deploy
```

---

## 🔧 Django Management Commands

### جمع Static Files
```bash
cd backend
python manage.py collectstatic --noinput
```

### تشغيل Migrations
```bash
cd backend
python manage.py migrate
```

### إنشاء Superuser
```bash
cd backend
python manage.py createsuperuser
```

### فحص المشروع
```bash
cd backend
python manage.py check
python manage.py check --deploy  # للإنتاج
```

---

## 🧪 الاختبار المحلي

### تشغيل الخادم (Development)
```bash
cd backend
python manage.py runserver
```

### اختبار Gunicorn محلياً
```bash
cd backend
gunicorn mylablink_python.wsgi:application
```

### اختبار مع Production Settings
```bash
cd backend
set DJANGO_SETTINGS_MODULE=mylablink_python.settings_production
python manage.py runserver
```

---

## 🗄️ قاعدة البيانات

### عمل migrations جديدة
```bash
cd backend
python manage.py makemigrations
python manage.py migrate
```

### عرض migrations الحالية
```bash
cd backend
python manage.py showmigrations
```

### Rollback migration
```bash
cd backend
python manage.py migrate app_name migration_name
```

### إعادة تعيين قاعدة البيانات (حذر!)
```bash
cd backend
python manage.py flush
```

---

## 📧 البريد الإلكتروني

### اختبار إرسال بريد
```bash
cd backend
python manage.py shell
>>> from django.core.mail import send_mail
>>> send_mail('Test', 'This is a test', 'from@example.com', ['to@example.com'])
```

---

## 🔐 الأمان

### توليد SECRET_KEY جديد
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### تغيير كلمة مرور Superuser
```bash
cd backend
python manage.py changepassword username
```

---

## 📊 البيانات

### تصدير البيانات (dump)
```bash
cd backend
python manage.py dumpdata > backup.json
python manage.py dumpdata app_name > app_backup.json
```

### استيراد البيانات (load)
```bash
cd backend
python manage.py loaddata backup.json
```

---

## 🧹 التنظيف والصيانة

### حذف الملفات المؤقتة
```bash
# Windows PowerShell
Get-ChildItem -Recurse -Include "__pycache__","*.pyc" | Remove-Item -Recurse -Force
```

```bash
# Git Bash / Linux
find . -type d -name "__pycache__" -exec rm -r {} +
find . -type f -name "*.pyc" -delete
```

### حذف staticfiles القديمة
```bash
cd backend
Remove-Item -Recurse -Force staticfiles
python manage.py collectstatic --noinput
```

---

## 🔍 التشخيص

### عرض إعدادات Django
```bash
cd backend
python manage.py diffsettings
```

### فحص URLs
```bash
cd backend
python manage.py show_urls  # إذا كان مثبت django-extensions
```

### عرض Models
```bash
cd backend
python manage.py inspectdb
```

---

## 📦 المتطلبات - Requirements

### تحديث requirements.txt
```bash
cd backend
pip freeze > requirements.txt
```

### تثبيت المتطلبات
```bash
cd backend
pip install -r requirements.txt
pip install -r ../requirements-render.txt
```

### تحديث المكتبات
```bash
pip list --outdated
pip install --upgrade package-name
```

---

## 🌐 Render - الأوامر على السيرفر

### عرض Logs المباشرة
في Render Dashboard → Logs → Live Logs

### إعادة نشر يدوي
في Render Dashboard → Manual Deploy → Deploy Latest Commit

### SSH إلى الخادم (إذا متاح)
```bash
ssh user@your-app.onrender.com
```

---

## 🐛 حل المشاكل - Troubleshooting

### عرض جميع متغيرات البيئة
```bash
cd backend
python manage.py shell
>>> import os
>>> print(os.environ)
```

### اختبار اتصال Database
```bash
cd backend
python manage.py dbshell
```

### عرض رسائل الخطأ التفصيلية
في `settings_production.py` مؤقتاً:
```python
DEBUG = True  # فقط للتشخيص، أعد إلى False بعد ذلك
```

---

## 🔄 التحديث المستمر - CI/CD

### رفع تحديث جديد
```bash
git add .
git commit -m "Your update description"
git push origin main
# Render will auto-deploy ✅
```

### إلغاء آخر commit
```bash
git reset --soft HEAD~1  # يحتفظ بالتغييرات
git reset --hard HEAD~1  # يحذف التغييرات (حذر!)
```

---

## 💡 نصائح مفيدة

### تشغيل Django Shell
```bash
cd backend
python manage.py shell
```

### حذف جميع Sessions
```bash
cd backend
python manage.py clearsessions
```

### إنشاء app جديد
```bash
cd backend
python manage.py startapp app_name
```

---

## 🎯 للاستخدام اليومي

### سير العمل المعتاد:
```bash
# 1. تحديث الكود محلياً
cd backend
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput

# 2. اختبار
python manage.py runserver

# 3. رفع إلى Git
cd ..
git add .
git commit -m "Description"
git push

# 4. Render ينشر تلقائياً! ✅
```

---

**ملاحظة:** احفظ هذا الملف للرجوع إليه عند الحاجة! 📌
