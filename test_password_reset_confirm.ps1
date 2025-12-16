# Test Password Reset Confirm
# ============================

Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host "Testing Password Reset Confirmation" -ForegroundColor Cyan
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host ""

$resetConfirmUrl = "http://127.0.0.1:8000/api/accounts/password-reset/confirm/"

# Prompt for token and new password
Write-Host "Enter the reset token from the email:" -ForegroundColor Yellow
$token = Read-Host "Token"

if ([string]::IsNullOrWhiteSpace($token)) {
    Write-Host "ERROR: Token is required!" -ForegroundColor Red
    exit
}

Write-Host ""
Write-Host "Enter new password:" -ForegroundColor Yellow
$newPassword = Read-Host "New Password" -AsSecureString
$newPasswordPlain = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($newPassword))

Write-Host "Confirm new password:" -ForegroundColor Yellow
$confirmPassword = Read-Host "Confirm Password" -AsSecureString
$confirmPasswordPlain = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($confirmPassword))

Write-Host ""

$confirmData = @{
    token = $token
    new_password = $newPasswordPlain
    new_password_confirm = $confirmPasswordPlain
} | ConvertTo-Json

Write-Host "Sending password reset confirmation..." -ForegroundColor Gray
Write-Host ""

try {
    $response = Invoke-RestMethod -Uri $resetConfirmUrl -Method Post -Body $confirmData -ContentType "application/json"
    
    Write-Host "=====================================================================" -ForegroundColor Green
    Write-Host "SUCCESS! Password has been reset!" -ForegroundColor Green
    Write-Host "=====================================================================" -ForegroundColor Green
    Write-Host ""
    
    Write-Host "Server Response:" -ForegroundColor Cyan
    $response | ConvertTo-Json -Depth 3 | Write-Host -ForegroundColor White
    Write-Host ""
    
    Write-Host "=====================================================================" -ForegroundColor Yellow
    Write-Host "NEXT STEPS:" -ForegroundColor Yellow
    Write-Host "=====================================================================" -ForegroundColor Yellow
    Write-Host "1. You can now login with your new password" -ForegroundColor White
    Write-Host "2. Run test_login.ps1 to test the new password" -ForegroundColor White
    Write-Host ""
    
} catch {
    Write-Host "=====================================================================" -ForegroundColor Red
    Write-Host "FAILED! Password reset confirmation error!" -ForegroundColor Red
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
    Write-Host "1. Token is invalid or expired" -ForegroundColor White
    Write-Host "2. Passwords do not match" -ForegroundColor White
    Write-Host "3. Password does not meet requirements (min 8 characters)" -ForegroundColor White
}

Write-Host ""
Write-Host "Test completed" -ForegroundColor Cyan
