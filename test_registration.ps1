# Test Registration API
# ======================

Write-Host "Starting registration test..." -ForegroundColor Cyan
Write-Host ""

$registerUrl = "http://127.0.0.1:8000/api/accounts/register/"

$randomNum = Get-Random -Maximum 9999
$userData = @{
    username = "ahmed_test_$randomNum"
    email = "ahmed_test_$randomNum@example.com"
    first_name = "Ahmed"
    password = "TestPass123!"
    password2 = "TestPass123!"
    phone = "0912345678"
    national_id = "123456789012"
    governorate = "Tripoli"
} | ConvertTo-Json

Write-Host "Sending request to: $registerUrl" -ForegroundColor Gray
Write-Host "Data:" -ForegroundColor Gray
Write-Host $userData -ForegroundColor Gray
Write-Host ""

try {
    $response = Invoke-RestMethod -Uri $registerUrl -Method Post -Body $userData -ContentType "application/json"
    
    Write-Host "SUCCESS! Registration completed!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Response:" -ForegroundColor Cyan
    $response | ConvertTo-Json -Depth 3 | Write-Host
    Write-Host ""
    
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "NEXT STEPS:" -ForegroundColor Yellow
    Write-Host "1. Check Django Server terminal" -ForegroundColor White
    Write-Host "2. Find the verification email" -ForegroundColor White
    Write-Host "3. Copy the verification link" -ForegroundColor White
    Write-Host "4. Open the link in browser" -ForegroundColor White
    Write-Host "========================================" -ForegroundColor Cyan
    
} catch {
    Write-Host "FAILED! Registration error!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Error details:" -ForegroundColor Yellow
    Write-Host $_.Exception.Message -ForegroundColor Red
    
    if ($_.ErrorDetails.Message) {
        Write-Host ""
        Write-Host "Server response:" -ForegroundColor Yellow
        $_.ErrorDetails.Message | ConvertFrom-Json | ConvertTo-Json -Depth 3 | Write-Host -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "Test completed" -ForegroundColor Cyan
