# نص برمجي لتطبيق الـ migrations بشكل احترافي

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "   تطبيق تحديثات قاعدة البيانات      " -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# الخطوة 1: عرض حالة الـ migrations
Write-Host "الخطوة 1: عرض حالة الـ migrations الحالية..." -ForegroundColor Yellow
python manage.py showmigrations api

Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# الخطوة 2: تطبيق الـ migrations
Write-Host "الخطوة 2: تطبيق الـ migrations..." -ForegroundColor Yellow
python manage.py migrate

Write-Host ""
Write-Host "======================================" -ForegroundColor Green
Write-Host "   تم الانتهاء بنجاح!                " -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Green
Write-Host ""
Write-Host "يمكنك الآن تشغيل السيرفر باستخدام:" -ForegroundColor Cyan
Write-Host "python manage.py runserver" -ForegroundColor White
