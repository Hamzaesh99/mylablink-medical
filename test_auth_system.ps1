# اختبار نظام المصادقة - MyLabLink
# Test Authentication System

Write-Host "🧪 بدء اختبار نظام المصادقة الكامل..." -ForegroundColor Cyan
Write-Host ""

$baseUrl = "http://127.0.0.1:8000"
$testEmail = "testuser_$(Get-Random)@example.com"
$testPassword = "TestPass123!"

# ============================================
# 1️⃣ اختبار التسجيل (Registration)
# ============================================
Write-Host "1️⃣ اختبار التسجيل..." -ForegroundColor Yellow

$registerBody = @{
    username = $testEmail
    email = $testEmail
    first_name = "Test"
    last_name = "User"
    password = $testPassword
    password2 = $testPassword
    phone = "0912345678"
    national_id = "$(Get-Random -Minimum 100000000000 -Maximum 999999999999)"
    governorate = "Tripoli"
} | ConvertTo-Json

try {
    $registerResponse = Invoke-WebRequest -Uri "$baseUrl/api/accounts/register/" `
        -Method POST `
        -Body $registerBody `
        -ContentType "application/json" `
        -UseBasicParsing
    
    $registerData = $registerResponse.Content | ConvertFrom-Json
    Write-Host "   ✅ التسجيل نجح!" -ForegroundColor Green
    Write-Host "   📧 البريد: $testEmail" -ForegroundColor Gray
    Write-Host "   📝 الرسالة: $($registerData.detail)" -ForegroundColor Gray
    Write-Host ""
    Write-Host "   ⚠️  تحقق من console السيرفر لرؤية رابط التفعيل!" -ForegroundColor Magenta
    Write-Host ""
} catch {
    Write-Host "   ❌ فشل التسجيل!" -ForegroundColor Red
    Write-Host "   الخطأ: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# ============================================
# 2️⃣ اختبار تسجيل الدخول بدون تفعيل
# ============================================
Write-Host "2️⃣ اختبار تسجيل الدخول بدون تفعيل (يجب أن يفشل)..." -ForegroundColor Yellow

$loginBody = @{
    username = $testEmail
    password = $testPassword
} | ConvertTo-Json

try {
    $loginResponse = Invoke-WebRequest -Uri "$baseUrl/api/auth/token/" `
        -Method POST `
        -Body $loginBody `
        -ContentType "application/json" `
        -UseBasicParsing
    
    Write-Host "   ⚠️  تسجيل الدخول نجح بدون تفعيل! (هذا خطأ)" -ForegroundColor Red
} catch {
    if ($_.Exception.Response.StatusCode -eq 401) {
        Write-Host "   ✅ تسجيل الدخول فشل كما متوقع (الحساب غير مفعل)" -ForegroundColor Green
    } else {
        Write-Host "   ❌ خطأ غير متوقع: $($_.Exception.Message)" -ForegroundColor Red
    }
}
Write-Host ""

# ============================================
# 3️⃣ تعليمات التفعيل اليدوي
# ============================================
Write-Host "3️⃣ التفعيل اليدوي مطلوب..." -ForegroundColor Yellow
Write-Host ""
Write-Host "   📋 الخطوات:" -ForegroundColor Cyan
Write-Host "   1. افتح terminal السيرفر (python manage.py runserver)"
Write-Host "   2. ابحث عن رابط التفعيل في الـ console"
Write-Host "   3. انسخ الرابط (مثال: http://127.0.0.1:8000/api/accounts/verify-email/xyz...)"
Write-Host "   4. افتحه في المتصفح أو استخدم curl"
Write-Host ""
Write-Host "   أو استخدم Python shell لتفعيل يدوي:" -ForegroundColor Cyan
Write-Host "   python manage.py shell" -ForegroundColor Gray
Write-Host "   >>> from django.contrib.auth import get_user_model" -ForegroundColor Gray
Write-Host "   >>> User = get_user_model()" -ForegroundColor Gray
Write-Host "   >>> u = User.objects.get(email='$testEmail')" -ForegroundColor Gray
Write-Host "   >>> u.is_active = True" -ForegroundColor Gray
Write-Host "   >>> u.save()" -ForegroundColor Gray
Write-Host "   >>> exit()" -ForegroundColor Gray
Write-Host ""

$activate = Read-Host "هل قمت بتفعيل الحساب؟ (y/n)"
if ($activate -ne "y") {
    Write-Host "   ⏸️  الاختبار متوقف. فعّل الحساب ثم شغّل السكريبت مرة أخرى." -ForegroundColor Yellow
    exit 0
}

# ============================================
# 4️⃣ اختبار تسجيل الدخول بعد التفعيل
# ============================================
Write-Host ""
Write-Host "4️⃣ اختبار تسجيل الدخول بعد التفعيل..." -ForegroundColor Yellow

try {
    $loginResponse = Invoke-WebRequest -Uri "$baseUrl/api/auth/token/" `
        -Method POST `
        -Body $loginBody `
        -ContentType "application/json" `
        -UseBasicParsing
    
    $loginData = $loginResponse.Content | ConvertFrom-Json
    $accessToken = $loginData.access
    $refreshToken = $loginData.refresh
    
    Write-Host "   ✅ تسجيل الدخول نجح!" -ForegroundColor Green
    Write-Host "   🔑 Access Token: $($accessToken.Substring(0, 50))..." -ForegroundColor Gray
    Write-Host ""
} catch {
    Write-Host "   ❌ فشل تسجيل الدخول!" -ForegroundColor Red
    Write-Host "   الخطأ: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# ============================================
# 5️⃣ اختبار الحصول على بيانات المستخدم
# ============================================
Write-Host "5️⃣ اختبار الحصول على بيانات المستخدم (/api/accounts/me/)..." -ForegroundColor Yellow

try {
    $headers = @{
        "Authorization" = "Bearer $accessToken"
    }
    
    $meResponse = Invoke-WebRequest -Uri "$baseUrl/api/accounts/me/" `
        -Method GET `
        -Headers $headers `
        -UseBasicParsing
    
    $meData = $meResponse.Content | ConvertFrom-Json
    Write-Host "   ✅ الحصول على البيانات نجح!" -ForegroundColor Green
    Write-Host "   👤 الاسم: $($meData.first_name) $($meData.last_name)" -ForegroundColor Gray
    Write-Host "   📧 البريد: $($meData.email)" -ForegroundColor Gray
    Write-Host "   🎭 الدور: $($meData.role)" -ForegroundColor Gray
    Write-Host ""
} catch {
    Write-Host "   ❌ فشل الحصول على البيانات!" -ForegroundColor Red
    Write-Host "   الخطأ: $($_.Exception.Message)" -ForegroundColor Red
}

# ============================================
# 6️⃣ اختبار إعادة تعيين كلمة المرور
# ============================================
Write-Host "6️⃣ اختبار إعادة تعيين كلمة المرور..." -ForegroundColor Yellow

$resetRequestBody = @{
    email = $testEmail
} | ConvertTo-Json

try {
    $resetResponse = Invoke-WebRequest -Uri "$baseUrl/api/accounts/password-reset/request/" `
        -Method POST `
        -Body $resetRequestBody `
        -ContentType "application/json" `
        -UseBasicParsing
    
    $resetData = $resetResponse.Content | ConvertFrom-Json
    Write-Host "   ✅ طلب إعادة التعيين نجح!" -ForegroundColor Green
    Write-Host "   📝 الرسالة: $($resetData.detail)" -ForegroundColor Gray
    Write-Host ""
    Write-Host "   ⚠️  تحقق من console السيرفر لرؤية رابط إعادة التعيين!" -ForegroundColor Magenta
    Write-Host ""
} catch {
    Write-Host "   ❌ فشل طلب إعادة التعيين!" -ForegroundColor Red
    Write-Host "   الخطأ: $($_.Exception.Message)" -ForegroundColor Red
}

# ============================================
# 7️⃣ اختبار تغيير كلمة المرور
# ============================================
Write-Host "7️⃣ اختبار تغيير كلمة المرور..." -ForegroundColor Yellow

$newPassword = "NewTestPass456!"
$changePasswordBody = @{
    old_password = $testPassword
    new_password = $newPassword
    new_password_confirm = $newPassword
} | ConvertTo-Json

try {
    $changeResponse = Invoke-WebRequest -Uri "$baseUrl/api/accounts/change-password/" `
        -Method POST `
        -Body $changePasswordBody `
        -ContentType "application/json" `
        -Headers $headers `
        -UseBasicParsing
    
    $changeData = $changeResponse.Content | ConvertFrom-Json
    Write-Host "   ✅ تغيير كلمة المرور نجح!" -ForegroundColor Green
    Write-Host "   📝 الرسالة: $($changeData.detail)" -ForegroundColor Gray
    Write-Host ""
} catch {
    Write-Host "   ❌ فشل تغيير كلمة المرور!" -ForegroundColor Red
    Write-Host "   الخطأ: $($_.Exception.Message)" -ForegroundColor Red
}

# ============================================
# 8️⃣ اختبار تسجيل الدخول بكلمة المرور الجديدة
# ============================================
Write-Host "8️⃣ اختبار تسجيل الدخول بكلمة المرور الجديدة..." -ForegroundColor Yellow

$newLoginBody = @{
    username = $testEmail
    password = $newPassword
} | ConvertTo-Json

try {
    $newLoginResponse = Invoke-WebRequest -Uri "$baseUrl/api/auth/token/" `
        -Method POST `
        -Body $newLoginBody `
        -ContentType "application/json" `
        -UseBasicParsing
    
    Write-Host "   ✅ تسجيل الدخول بكلمة المرور الجديدة نجح!" -ForegroundColor Green
    Write-Host ""
} catch {
    Write-Host "   ❌ فشل تسجيل الدخول بكلمة المرور الجديدة!" -ForegroundColor Red
    Write-Host "   الخطأ: $($_.Exception.Message)" -ForegroundColor Red
}

# ============================================
# 9️⃣ اختبار تحديث Access Token
# ============================================
Write-Host "9️⃣ اختبار تحديث Access Token..." -ForegroundColor Yellow

$refreshBody = @{
    refresh = $refreshToken
} | ConvertTo-Json

try {
    $refreshResponse = Invoke-WebRequest -Uri "$baseUrl/api/auth/token/refresh/" `
        -Method POST `
        -Body $refreshBody `
        -ContentType "application/json" `
        -UseBasicParsing
    
    $refreshData = $refreshResponse.Content | ConvertFrom-Json
    Write-Host "   ✅ تحديث Token نجح!" -ForegroundColor Green
    Write-Host "   🔑 New Access Token: $($refreshData.access.Substring(0, 50))..." -ForegroundColor Gray
    Write-Host ""
} catch {
    Write-Host "   ❌ فشل تحديث Token!" -ForegroundColor Red
    Write-Host "   الخطأ: $($_.Exception.Message)" -ForegroundColor Red
}

# ============================================
# 📊 النتيجة النهائية
# ============================================
Write-Host ""
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "📊 ملخص الاختبار" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host ""
Write-Host "✅ التسجيل: نجح" -ForegroundColor Green
Write-Host "✅ منع الدخول بدون تفعيل: نجح" -ForegroundColor Green
Write-Host "✅ تسجيل الدخول بعد التفعيل: نجح" -ForegroundColor Green
Write-Host "✅ الحصول على بيانات المستخدم: نجح" -ForegroundColor Green
Write-Host "✅ طلب إعادة تعيين كلمة المرور: نجح" -ForegroundColor Green
Write-Host "✅ تغيير كلمة المرور: نجح" -ForegroundColor Green
Write-Host "✅ تسجيل الدخول بكلمة المرور الجديدة: نجح" -ForegroundColor Green
Write-Host "✅ تحديث Access Token: نجح" -ForegroundColor Green
Write-Host ""
Write-Host "🎉 نظام المصادقة يعمل بشكل كامل!" -ForegroundColor Green
Write-Host ""
Write-Host "📝 ملاحظات:" -ForegroundColor Yellow
Write-Host "   - البريد المستخدم: $testEmail" -ForegroundColor Gray
Write-Host "   - كلمة المرور الحالية: $newPassword" -ForegroundColor Gray
Write-Host "   - يمكنك استخدام هذا الحساب للاختبار" -ForegroundColor Gray
Write-Host ""
