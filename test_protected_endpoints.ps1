# Test Protected Endpoints
# =========================

Write-Host "Testing Protected Endpoints..." -ForegroundColor Cyan
Write-Host ""

# Check if tokens.json exists
if (Test-Path "tokens.json") {
    Write-Host "Loading tokens from tokens.json..." -ForegroundColor Gray
    $tokens = Get-Content "tokens.json" | ConvertFrom-Json
    $accessToken = $tokens.access
    
    Write-Host "Access Token found!" -ForegroundColor Green
    Write-Host ""
} else {
    Write-Host "No tokens.json file found!" -ForegroundColor Yellow
    Write-Host "Please run test_login.ps1 first to get tokens." -ForegroundColor Yellow
    exit
}

# Create authorization header
$headers = @{
    "Authorization" = "Bearer $accessToken"
}

Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host "Testing Endpoints" -ForegroundColor Cyan
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host ""

# Test 1: Get current user info
Write-Host "1. Testing GET /api/accounts/me/" -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/accounts/me/" -Method Get -Headers $headers
    Write-Host "   SUCCESS!" -ForegroundColor Green
    Write-Host "   User: $($response.username) ($($response.email))" -ForegroundColor White
    Write-Host "   Name: $($response.first_name) $($response.last_name)" -ForegroundColor White
    Write-Host "   Role: $($response.role)" -ForegroundColor White
    Write-Host ""
} catch {
    Write-Host "   FAILED!" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
}

# Test 2: Get users list (if admin)
Write-Host "2. Testing GET /api/accounts/users/" -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/accounts/users/" -Method Get -Headers $headers
    Write-Host "   SUCCESS!" -ForegroundColor Green
    Write-Host "   Found $($response.count) users" -ForegroundColor White
    Write-Host ""
} catch {
    Write-Host "   FAILED (might need admin permissions)" -ForegroundColor Yellow
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
}

# Test 3: Update profile
Write-Host "3. Testing PATCH /api/accounts/me/" -ForegroundColor Yellow
$updateData = @{
    first_name = "Ahmed"
    last_name = "Updated"
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/accounts/me/" -Method Patch -Headers $headers -Body $updateData -ContentType "application/json"
    Write-Host "   SUCCESS!" -ForegroundColor Green
    Write-Host "   Updated name: $($response.first_name) $($response.last_name)" -ForegroundColor White
    Write-Host ""
} catch {
    Write-Host "   FAILED!" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
}

Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host "Testing completed!" -ForegroundColor Cyan
Write-Host "=====================================================================" -ForegroundColor Cyan
