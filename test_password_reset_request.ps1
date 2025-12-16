# Test Password Reset Request
# ===========================

Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host "Testing Password Reset Request" -ForegroundColor Cyan
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host ""

$resetRequestUrl = "http://127.0.0.1:8000/api/accounts/password-reset/request/"

# Prompt for email
Write-Host "Enter email address to reset password:" -ForegroundColor Yellow
$email = Read-Host "Email"

if ([string]::IsNullOrWhiteSpace($email)) {
    $email = "test@example.com"
    Write-Host "Using default: $email" -ForegroundColor Gray
}

Write-Host ""

$requestData = @{
    email = $email
} | ConvertTo-Json

Write-Host "Sending password reset request..." -ForegroundColor Gray
Write-Host "Email: $email" -ForegroundColor Gray
Write-Host ""

try {
    $response = Invoke-RestMethod -Uri $resetRequestUrl -Method Post -Body $requestData -ContentType "application/json"
    
    Write-Host "=====================================================================" -ForegroundColor Green
    Write-Host "SUCCESS! Password reset email sent!" -ForegroundColor Green
    Write-Host "=====================================================================" -ForegroundColor Green
    Write-Host ""
    
    Write-Host "Server Response:" -ForegroundColor Cyan
    $response | ConvertTo-Json -Depth 3 | Write-Host -ForegroundColor White
    Write-Host ""
    
    Write-Host "=====================================================================" -ForegroundColor Yellow
    Write-Host "NEXT STEPS:" -ForegroundColor Yellow
    Write-Host "=====================================================================" -ForegroundColor Yellow
    Write-Host "1. Check Django Server console/terminal" -ForegroundColor White
    Write-Host "2. Look for the password reset email" -ForegroundColor White
    Write-Host "3. Find the reset link (starts with http://127.0.0.1:8000/reset-password/?token=...)" -ForegroundColor White
    Write-Host "4. Copy the TOKEN from the URL" -ForegroundColor White
    Write-Host "5. Run test_password_reset_confirm.ps1 with the token" -ForegroundColor White
    Write-Host ""
    Write-Host "OR use Django command to get the token:" -ForegroundColor Cyan
    Write-Host "  cd backend" -ForegroundColor Gray
    Write-Host "  python manage.py shell -c `"from accounts.utils import generate_password_reset_token; from accounts.models import User; user = User.objects.get(email='$email'); print(generate_password_reset_token(user))`"" -ForegroundColor Gray
    Write-Host ""
    
} catch {
    Write-Host "=====================================================================" -ForegroundColor Red
    Write-Host "FAILED! Password reset request error!" -ForegroundColor Red
    Write-Host "=====================================================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "Error details:" -ForegroundColor Yellow
    Write-Host $_.Exception.Message -ForegroundColor Red
    
    if ($_.ErrorDetails.Message) {
        Write-Host ""
        Write-Host "Server response:" -ForegroundColor Yellow
        try {
            $_.ErrorDetails.Message | ConvertFrom-Json | ConvertTo-Json -Depth 3 | Write-Host -ForegroundColor Red
        } catch {
            Write-Host $_.ErrorDetails.Message -ForegroundColor Red
        }
    }
    
    Write-Host ""
    Write-Host "Possible reasons:" -ForegroundColor Yellow
    Write-Host "1. Email address does not exist in database" -ForegroundColor White
    Write-Host "2. Email service is not configured" -ForegroundColor White
    Write-Host "3. Server error" -ForegroundColor White
}

Write-Host ""
Write-Host "Test completed" -ForegroundColor Cyan
