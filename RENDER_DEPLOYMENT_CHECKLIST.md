# 🚀 قائمة مرجعية لنشر MyLabLink على Render

## ✅ التحضيرات المكتملة

### 1. الملفات الأساسية ✓
- [x] **wsgi.py** - محدّث ويدعم إعدادات الإنتاج
- [x] **render.yaml** - تكوين Render كامل
- [x] **build.sh** - سكريبت البناء جاهز
- [x] **settings_production.py** - إعدادات الإنتاج شاملة
- [x] **requirements.txt** - جميع المكتبات المطلوبة موجودة
- [x] **requirements-render.txt** - مكتبات Render الخاصة

### 2. المكتبات المطلوبة ✓
- [x] gunicorn (21.2.0)
- [x] whitenoise (6.6.0)
- [x] dj-database-url (2.1.0)
- [x] psycopg2-binary (لـ PostgreSQL)

---

## 📝 خطوات النشر على Render

### المرحلة 1: إعداد المستودع (Repository)

1. **رفع المشروع إلى GitHub**
   ```bash
   git init
   git add .
   git commit -m "Prepare for Render deployment"
   git branch -M main
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

### المرحلة 2: إنشاء الخدمات على Render

#### أ) إنشاء قاعدة البيانات PostgreSQL

1. اذهب إلى [Render Dashboard](https://dashboard.render.com/)
2. اضغط على **"New +"** → **"PostgreSQL"**
3. املأ المعلومات:
   - **Name**: `mylablink-db`
   - **Database**: `mylablink_db`
   - **User**: `mylablink_user`
   - **Region**: اختر الأقرب لك (مثل Frankfurt)
   - **Plan**: Free أو مدفوع حسب احتياجك
4. اضغط **"Create Database"**
5. **احفظ تفاصيل الاتصال** (ستحتاجها لاحقاً)

#### ب) إنشاء Web Service

1. اضغط على **"New +"** → **"Web Service"**
2. اختر **"Build and deploy from a Git repository"**
3. اختر المستودع من GitHub
4. املأ المعلومات:
   - **Name**: `mylablink`
   - **Region**: نفس منطقة قاعدة البيانات
   - **Branch**: `main`
   - **Root Directory**: اتركه فارغاً
   - **Environment**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `cd backend && gunicorn mylablink_python.wsgi:application --workers 2 --threads 4 --timeout 120`

### المرحلة 3: ضبط متغيرات البيئة (Environment Variables)

في صفحة إعدادات Web Service، أضف المتغيرات التالية:

#### ✅ متغيرات أساسية (مطلوبة)

```env
# Django Settings
DJANGO_SECRET_KEY=$cw^plkzxj*hyg0oq5p6xx9+8)e!rne$0sqsc)i%y@-rm(n^0g
DEBUG=False
DJANGO_SETTINGS_MODULE=mylablink_python.settings_production
PYTHON_VERSION=3.11.0

# Allowed Hosts
ALLOWED_HOSTS=.onrender.com,127.0.0.1,localhost

# Database (سيتم ربطها تلقائياً من خلال render.yaml)
DATABASE_URL=postgresql://mylablink_user:hAtziVWFJD5sv1cfneieepGRTzy9yTEk@dpg-d518q1vfte5s73908v60-a.frankfurt-postgres.render.com/mylablink_db_aqx5

# Security
SECURE_SSL_REDIRECT=True
```

#### ⚠️ متغيرات البريد الإلكتروني (مطلوبة للتفعيل الكامل)

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=<your-email@gmail.com>
EMAIL_HOST_PASSWORD=<your-app-specific-password>
DEFAULT_FROM_EMAIL=MyLabLink <no-reply@mylablink.com>
```

**ملاحظة**: للحصول على App Password من Gmail:
1. اذهب إلى [Google Account Security](https://myaccount.google.com/security)
2. فعّل المصادقة الثنائية (2FA)
3. اذهب إلى "App passwords"
4. أنشئ كلمة مرور للتطبيق

#### 📊 متغيرات اختيارية

```env
SITE_BASE_URL=https://mylablink.onrender.com
ACCOUNT_EMAIL_VERIFICATION=mandatory
CORS_ALLOW_ALL=False
DJANGO_LOG_LEVEL=INFO
```

### المرحلة 4: الربط والنشر

1. **ربط قاعدة البيانات بـ Web Service**:
   - في صفحة Web Service، اذهب إلى "Environment"
   - أضف متغير `DATABASE_URL` واختر "Add from database"
   - اختر `mylablink-db`

2. **حفظ ونشر**:
   - اضغط "Save Changes"
   - Render سيبدأ تلقائياً في عملية البناء والنشر

3. **انتظر اكتمال البناء**:
   - تابع Logs في الوقت الفعلي
   - يجب أن ترى:
     ```
     Installing Python dependencies...
     Collecting static files...
     Running database migrations...
     Build completed successfully!
     ```

### المرحلة 5: التحقق بعد النشر

✅ **اختبارات يجب إجراؤها:**

1. **الصفحة الرئيسية**
   ```
   https://mylablink.onrender.com/
   ```

2. **لوحة الإدارة**
   ```
   https://mylablink.onrender.com/admin/
   ```

3. **API التسجيل والدخول**
   ```
   https://mylablink.onrender.com/api/accounts/register/
   https://mylablink.onrender.com/api/accounts/login/
   ```

4. **Static Files**
   - تأكد أن الصور والـ CSS يعملان

5. **Database**
   - أنشئ حساب اختباري
   - تحقق من وصول البريد الإلكتروني

---

## 🔧 استكشاف الأخطاء

### مشكلة: Static Files لا تظهر

**الحل:**
```bash
# في Render Shell
cd backend
python manage.py collectstatic --noinput
```

### مشكلة: Database Connection Error

**الحل:**
1. تحقق من `DATABASE_URL` في Environment Variables
2. تأكد من أن قاعدة البيانات تعمل
3. راجع Logs للتفاصيل

### مشكلة: Build Timeout

**الحل:**
- قلل عدد Dependencies غير المستخدمة
- استخدم خطة مدفوعة للحصول على موارد أكثر

### مشكلة: Email لا يُرسل

**الحل:**
1. تحقق من صحة `EMAIL_HOST_USER` و `EMAIL_HOST_PASSWORD`
2. تأكد من أن App Password من Gmail صحيح
3. تحقق من Logs للأخطاء

---

## 📊 معلومات إضافية

### الأوامر المفيدة في Render Shell

```bash
# الوصول إلى Shell
# 1. اذهب إلى Web Service
# 2. اضغط "Shell" في القائمة العلوية

# تشغيل Django Shell
cd backend
python manage.py shell

# إنشاء superuser
python manage.py createsuperuser

# عرض الـ Migrations
python manage.py showmigrations

# تطبيق Migrations يدوياً
python manage.py migrate
```

### الأداء والتحسين

1. **استخدم CDN للملفات الثابتة** (اختياري)
2. **فعّل Caching** باستخدام Redis
3. **راقب استخدام الموارد** في Render Dashboard
4. **استخدم Gunicorn workers المناسبة**:
   - Formula: `(2 × CPU cores) + 1`
   - Free plan: 2 workers كافية

### النسخ الاحتياطي

- **قاعدة البيانات**: Render يعمل نسخ احتياطي تلقائي
- **الكود**: محفوظ في GitHub
- **الملفات المرفوعة (Media)**: استخدم خدمة تخزين خارجية مثل:
  - AWS S3
  - Cloudinary
  - Google Cloud Storage

---

## ✅ قائمة التحقق النهائية

قبل النشر، تأكد من:

- [ ] رفع الكود إلى GitHub
- [ ] إنشاء PostgreSQL Database على Render
- [ ] إنشاء Web Service على Render
- [ ] إضافة جميع Environment Variables
- [ ] ربط DATABASE_URL
- [ ] إضافة بيانات البريد الإلكتروني
- [ ] اختبار الموقع بعد النشر
- [ ] إنشاء حساب superuser
- [ ] اختبار جميع الوظائف الأساسية

---

## 🎉 بعد النشر الناجح

1. **شارك الرابط** مع المستخدمين
2. **راقب الأداء** في Render Dashboard
3. **تابع Logs** لأي أخطاء
4. **قم بالتحديثات** عبر Git Push

---

**ملاحظة**: الخطة المجانية في Render قد تتوقف بعد 15 دقيقة من عدم النشاط. أول طلب بعد ذلك قد يستغرق 30-60 ثانية.

**حظاً موفقاً في النشر! 🚀**
