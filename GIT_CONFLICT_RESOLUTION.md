# 🔧 حل تعارض Git - خطوات يدوية
## Manual Git Conflict Resolution

---

## ✅ ما تم إنجازه:

1. ✅ تم حل التعارض في ملف `.gitignore`
2. ✅ الملف الآن يحتوي على جميع القواعد المطلوبة

---

## 📝 الخطوات التالية (نسخ والصق):

### 1️⃣ إضافة .gitignore المُحدّث:
```powershell
cd C:\Users\HP\Desktop\mylablink-medical-lab
git add .gitignore
```

### 2️⃣ إكمال عملية الدمج:
```powershell
git commit -m "Resolve .gitignore merge conflict"
```

### 3️⃣ إضافة ملفات النشر:
```powershell
git add build.sh render.yaml requirements-render.txt .env.render.example .gitattributes
git add backend/Procfile backend/mylablink_python/settings_production.py backend/mylablink_python/settings.py
git add DEPLOYMENT_FILES.md README_DEPLOYMENT.md DEPLOYMENT_CHECKLIST.md QUICK_COMMANDS.md RENDER_DEPLOYMENT.md
```

### 4️⃣ عمل Commit للتغييرات الجديدة:
```powershell
git commit -m "Add complete Render deployment configuration"
```

### 5️⃣ رفع الكود إلى GitHub:
```powershell
git push origin main
```

---

## 🚀 أو استخدم السكريبت التلقائي:

```powershell
.\resolve_and_push.ps1
```

---

## ❌ إذا واجهت مشكلة "الملفات كبيرة جداً"

### حذف الملفات الكبيرة من Git cache:
```powershell
# حذف staticfiles من التتبع
git rm -r --cached backend/staticfiles

# حذف __pycache__ من التتبع
git rm -r --cached backend/**/__pycache__

# حذف ملفات .pyc
git rm --cached **/*.pyc

# إضافة التغييرات
git add .gitignore
git commit -m "Remove large files from Git tracking"
```

---

## 🔍 التحقق من الملفات المتتبعة:

```powershell
# عرض الملفات التي سيتم رفعها
git status

# عرض حجم الملفات
git ls-files | ForEach-Object { Get-Item $_ } | Sort-Object Length -Descending | Select-Object -First 20
```

---

## 🧹 تنظيف الملفات الكبيرة:

إذا كانت المشكلة في ملفات محددة:

```powershell
# حذف staticfiles محلياً ثم collectstatic مرة أخرى
Remove-Item -Recurse -Force backend/staticfiles

# حذف __pycache__
Get-ChildItem -Recurse -Include "__pycache__","*.pyc" | Remove-Item -Recurse -Force

# جمع static files من جديد
cd backend
python manage.py collectstatic --noinput
cd ..
```

---

## ✅ بعد الحل:

```powershell
git add .
git commit -m "Clean up and ready for deployment"
git push origin main
```

---

## 📋 ملف .gitignore الحالي يستبعد:

✅ `__pycache__/` و `*.pyc` - ملفات Python المؤقتة  
✅ `venv/` و `.venv/` - البيئات الافتراضية  
✅ `staticfiles/` - الملفات الثابتة المجمعة  
✅ `media/` - ملفات المستخدمين  
✅ `.env` و `.env.production` - متغيرات البيئة الحساسة  
✅ `db.sqlite3` - قاعدة البيانات المحلية  
✅ `*.log` - ملفات السجلات  
✅ الملفات الحساسة مثل `token.txt`, `verification_links.txt`

---

## 🎯 الهدف النهائي:

بعد تنفيذ الخطوات أعلاه:
1. التعارض سيكون محلولاً ✅
2. جميع ملفات النشر سترفع إلى GitHub ✅
3. المشروع جاهز للنشر على Render ✅

---

**اختر الطريقة:**
- 🤖 **تلقائي**: شغّل `.\resolve_and_push.ps1`
- ✋ **يدوي**: نفّذ الأوامر أعلاه واحدة تلو الأخرى
