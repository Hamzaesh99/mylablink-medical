# سكريبت لحل المشكلة وتشغيل السيرفر

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "   حل مشكلة قاعدة البيانات وتشغيل السيرفر" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# الخطوة 1: عرض حالة Migrations
Write-Host "الخطوة 1: فحص حالة Migrations..." -ForegroundColor Yellow
python manage.py showmigrations api

Write-Host "`n"

# الخطوة 2: تطبيق Migrations
Write-Host "الخطوة 2: تطبيق Migrations..." -ForegroundColor Yellow
python manage.py migrate

Write-Host "`n"

# الخطوة 3: التحقق من النجاح
Write-Host "الخطوة 3: التحقق من التطبيق..." -ForegroundColor Yellow
python verify_fix.py

Write-Host "`n"

# الخطوة 4: تشغيل السيرفر
Write-Host "========================================" -ForegroundColor Green
Write-Host "   جاهز! تشغيل السيرفر الآن..." -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Green

Write-Host "السيرفر سيعمل على: http://127.0.0.1:8000" -ForegroundColor Cyan
Write-Host "لإيقاف السيرفر: اضغط CTRL+C`n" -ForegroundColor Yellow

python manage.py runserver
