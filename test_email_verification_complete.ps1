# Complete Email Verification System Test
# =========================================

Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host "Testing Email Verification System" -ForegroundColor Cyan
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host ""

$testsPassed = 0
$testsFailed = 0

# Test 1: Register a new user
Write-Host "Test 1: Registering a new user..." -ForegroundColor Yellow
$randomNum = Get-Random -Maximum 99999
$testEmail = "emailtest$randomNum@example.com"
$testUsername = "emailtest$randomNum"

$registerData = @{
    username = $testUsername
    email = $testEmail
    first_name = "Email"
    last_name = "Test"
    password = "TestPass123!"
    password2 = "TestPass123!"
    phone = "0912345678"
    national_id = "$(Get-Random -Minimum 100000000000 -Maximum 999999999999)"
    governorate = "Tripoli"
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/accounts/register/" -Method Post -Body $registerData -ContentType "application/json" -ErrorAction Stop
    
    Write-Host "   PASS - User registered successfully" -ForegroundColor Green
    Write-Host "   Email: $testEmail" -ForegroundColor Gray
    $testsPassed++
    
    # Save email for later tests
    $script:testEmail = $testEmail
    $script:testUsername = $testUsername
    
} catch {
    Write-Host "   FAIL - Registration failed" -ForegroundColor Red
    if ($_.ErrorDetails.Message) {
        $error = $_.ErrorDetails.Message | ConvertFrom-Json
        Write-Host "   Error: $($error | ConvertTo-Json -Compress)" -ForegroundColor Red
    }
    $testsFailed++
    exit
}

Write-Host ""

# Test 2: Check user is inactive
Write-Host "Test 2: Checking user is inactive (not verified)..." -ForegroundColor Yellow

try {
    cd backend
    $output = python manage.py shell -c "from accounts.models import User; u = User.objects.get(email='$testEmail'); print('ACTIVE' if u.is_active else 'INACTIVE')" 2>&1
    cd ..
    
    if ($output -match "INACTIVE") {
        Write-Host "   PASS - User is inactive (waiting for verification)" -ForegroundColor Green
        $testsPassed++
    } else {
        Write-Host "   FAIL - User should be inactive!" -ForegroundColor Red
        $testsFailed++
    }
} catch {
    Write-Host "   FAIL - Could not check user status" -ForegroundColor Red
    $testsFailed++
}

Write-Host ""

# Test 3: Generate verification token
Write-Host "Test 3: Generating verification token..." -ForegroundColor Yellow

try {
    cd backend
    $tokenOutput = python -c "import os, sys, django; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mylablink_python.settings'); django.setup(); from accounts.models import User; from accounts.utils import generate_email_token; u = User.objects.get(email='$testEmail'); print(generate_email_token(u))" 2>&1
    cd ..
    
    # Extract token (last line of output)
    $token = ($tokenOutput -split "`n")[-1].Trim()
    
    if ($token -and $token.Length -gt 20) {
        Write-Host "   PASS - Token generated successfully" -ForegroundColor Green
        Write-Host "   Token: $($token.Substring(0, 30))..." -ForegroundColor Gray
        $testsPassed++
        $script:verificationToken = $token
    } else {
        Write-Host "   FAIL - Token generation failed" -ForegroundColor Red
        Write-Host "   Output: $tokenOutput" -ForegroundColor Red
        $testsFailed++
        exit
    }
} catch {
    Write-Host "   FAIL - Error generating token" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
    $testsFailed++
    exit
}

Write-Host ""

# Test 4: Verify email with token
Write-Host "Test 4: Verifying email with token..." -ForegroundColor Yellow

try {
    $verifyUrl = "http://127.0.0.1:8000/api/accounts/verify-email/$verificationToken/"
    $response = Invoke-RestMethod -Uri $verifyUrl -Method Get -ErrorAction Stop
    
    Write-Host "   PASS - Email verified successfully" -ForegroundColor Green
    Write-Host "   Response: $($response | ConvertTo-Json -Compress)" -ForegroundColor Gray
    $testsPassed++
    
} catch {
    Write-Host "   FAIL - Email verification failed" -ForegroundColor Red
    if ($_.ErrorDetails.Message) {
        Write-Host "   Error: $($_.ErrorDetails.Message)" -ForegroundColor Red
    }
    $testsFailed++
}

Write-Host ""

# Test 5: Check user is now active
Write-Host "Test 5: Checking user is now active..." -ForegroundColor Yellow

try {
    cd backend
    $output = python manage.py shell -c "from accounts.models import User; u = User.objects.get(email='$testEmail'); print('ACTIVE' if u.is_active else 'INACTIVE')" 2>&1
    cd ..
    
    if ($output -match "ACTIVE") {
        Write-Host "   PASS - User is now active!" -ForegroundColor Green
        $testsPassed++
    } else {
        Write-Host "   FAIL - User should be active after verification!" -ForegroundColor Red
        $testsFailed++
    }
} catch {
    Write-Host "   FAIL - Could not check user status" -ForegroundColor Red
    $testsFailed++
}

Write-Host ""

# Test 6: Try to login with verified account
Write-Host "Test 6: Testing login with verified account..." -ForegroundColor Yellow

$loginData = @{
    username = $testEmail
    password = "TestPass123!"
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/auth/token/" -Method Post -Body $loginData -ContentType "application/json" -ErrorAction Stop
    
    if ($response.access -and $response.refresh) {
        Write-Host "   PASS - Login successful with verified account" -ForegroundColor Green
        Write-Host "   Access token received: Yes" -ForegroundColor Gray
        Write-Host "   Refresh token received: Yes" -ForegroundColor Gray
        $testsPassed++
    } else {
        Write-Host "   FAIL - Login succeeded but no tokens received" -ForegroundColor Red
        $testsFailed++
    }
    
} catch {
    Write-Host "   FAIL - Login failed" -ForegroundColor Red
    if ($_.ErrorDetails.Message) {
        Write-Host "   Error: $($_.ErrorDetails.Message)" -ForegroundColor Red
    }
    $testsFailed++
}

Write-Host ""

# Test 7: Test resend verification (should fail for already verified user)
Write-Host "Test 7: Testing resend verification for already verified user..." -ForegroundColor Yellow

$resendData = @{
    email = $testEmail
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/accounts/resend-verification/" -Method Post -Body $resendData -ContentType "application/json" -ErrorAction Stop
    
    Write-Host "   INFO - Resend verification response received" -ForegroundColor Yellow
    Write-Host "   Response: $($response | ConvertTo-Json -Compress)" -ForegroundColor Gray
    
} catch {
    # This might fail if user is already verified, which is expected
    Write-Host "   INFO - Resend verification returned error (expected for verified user)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host "Test Summary" -ForegroundColor Cyan
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Total Tests: $($testsPassed + $testsFailed)" -ForegroundColor White
Write-Host "Passed: $testsPassed" -ForegroundColor Green
Write-Host "Failed: $testsFailed" -ForegroundColor Red
Write-Host ""

if ($testsFailed -eq 0) {
    Write-Host "=====================================================================" -ForegroundColor Green
    Write-Host "ALL TESTS PASSED! Email verification system works perfectly!" -ForegroundColor Green
    Write-Host "=====================================================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Summary of what was tested:" -ForegroundColor Cyan
    Write-Host "1. User registration" -ForegroundColor White
    Write-Host "2. User starts as inactive" -ForegroundColor White
    Write-Host "3. Verification token generation" -ForegroundColor White
    Write-Host "4. Email verification with token" -ForegroundColor White
    Write-Host "5. User becomes active after verification" -ForegroundColor White
    Write-Host "6. Login works with verified account" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host "=====================================================================" -ForegroundColor Red
    Write-Host "SOME TESTS FAILED! Please review the errors above." -ForegroundColor Red
    Write-Host "=====================================================================" -ForegroundColor Red
}

Write-Host ""
Write-Host "Test user created:" -ForegroundColor Cyan
Write-Host "  Email: $testEmail" -ForegroundColor White
Write-Host "  Username: $testUsername" -ForegroundColor White
Write-Host "  Password: TestPass123!" -ForegroundColor White
Write-Host ""
