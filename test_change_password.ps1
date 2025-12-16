# Test Change Password (Authenticated User)
# ==========================================

Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host "Testing Change Password (Authenticated User)" -ForegroundColor Cyan
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host ""

$changePasswordUrl = "http://127.0.0.1:8000/api/accounts/change-password/"

# Check if tokens.json exists
if (Test-Path "tokens.json") {
    Write-Host "Loading access token from tokens.json..." -ForegroundColor Gray
    $tokens = Get-Content "tokens.json" | ConvertFrom-Json
    $accessToken = $tokens.access
    Write-Host "Access token found!" -ForegroundColor Green
    Write-Host ""
} else {
    Write-Host "No tokens.json file found!" -ForegroundColor Yellow
    Write-Host "Please run test_login.ps1 first to get access token." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Or enter access token manually:" -ForegroundColor Yellow
    $accessToken = Read-Host "Access Token"
    
    if ([string]::IsNullOrWhiteSpace($accessToken)) {
        Write-Host "ERROR: Access token is required!" -ForegroundColor Red
        exit
    }
}

# Prompt for passwords
Write-Host "Enter current password:" -ForegroundColor Yellow
$oldPassword = Read-Host "Current Password" -AsSecureString
$oldPasswordPlain = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($oldPassword))

Write-Host "Enter new password:" -ForegroundColor Yellow
$newPassword = Read-Host "New Password" -AsSecureString
$newPasswordPlain = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($newPassword))

Write-Host "Confirm new password:" -ForegroundColor Yellow
$confirmPassword = Read-Host "Confirm Password" -AsSecureString
$confirmPasswordPlain = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($confirmPassword))

Write-Host ""

# Create authorization header
$headers = @{
    "Authorization" = "Bearer $accessToken"
}

$changeData = @{
    old_password = $oldPasswordPlain
    new_password = $newPasswordPlain
    new_password_confirm = $confirmPasswordPlain
} | ConvertTo-Json

Write-Host "Sending change password request..." -ForegroundColor Gray
Write-Host ""

try {
    $response = Invoke-RestMethod -Uri $changePasswordUrl -Method Post -Headers $headers -Body $changeData -ContentType "application/json"
    
    Write-Host "=====================================================================" -ForegroundColor Green
    Write-Host "SUCCESS! Password has been changed!" -ForegroundColor Green
    Write-Host "=====================================================================" -ForegroundColor Green
    Write-Host ""
    
    Write-Host "Server Response:" -ForegroundColor Cyan
    $response | ConvertTo-Json -Depth 3 | Write-Host -ForegroundColor White
    Write-Host ""
    
    Write-Host "=====================================================================" -ForegroundColor Yellow
    Write-Host "IMPORTANT NOTES:" -ForegroundColor Yellow
    Write-Host "=====================================================================" -ForegroundColor Yellow
    Write-Host "1. Your password has been changed successfully" -ForegroundColor White
    Write-Host "2. Your current access token is still valid" -ForegroundColor White
    Write-Host "3. Next time you login, use the NEW password" -ForegroundColor White
    Write-Host "4. Test login with new password: test_login.ps1" -ForegroundColor White
    Write-Host ""
    
} catch {
    Write-Host "=====================================================================" -ForegroundColor Red
    Write-Host "FAILED! Change password error!" -ForegroundColor Red
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
    Write-Host "1. Current password is incorrect" -ForegroundColor White
    Write-Host "2. New passwords do not match" -ForegroundColor White
    Write-Host "3. New password does not meet requirements (min 8 characters)" -ForegroundColor White
    Write-Host "4. Access token is invalid or expired" -ForegroundColor White
}

Write-Host ""
Write-Host "Test completed" -ForegroundColor Cyan
