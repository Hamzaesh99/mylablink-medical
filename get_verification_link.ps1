# Get Verification Link
# ====================

Write-Host "Getting verification link for inactive user..." -ForegroundColor Cyan
Write-Host ""

$pythonScript = @"
from accounts.models import User
from accounts.utils import generate_email_token

user = User.objects.filter(is_active=False).last()

if not user:
    print('NO_INACTIVE_USERS')
else:
    token = generate_email_token(user)
    print(f'USERNAME:{user.username}')
    print(f'EMAIL:{user.email}')
    print(f'NAME:{user.first_name}')
    print(f'LINK:http://127.0.0.1:8000/api/accounts/verify-email/{token}/')
"@

cd backend
$output = python manage.py shell -c $pythonScript

if ($output -match "NO_INACTIVE_USERS") {
    Write-Host "No inactive users found!" -ForegroundColor Yellow
    Write-Host "All users are already activated." -ForegroundColor Yellow
} else {
    $username = ($output | Select-String -Pattern "USERNAME:(.+)" | ForEach-Object { $_.Matches.Groups[1].Value })
    $email = ($output | Select-String -Pattern "EMAIL:(.+)" | ForEach-Object { $_.Matches.Groups[1].Value })
    $name = ($output | Select-String -Pattern "NAME:(.+)" | ForEach-Object { $_.Matches.Groups[1].Value })
    $link = ($output | Select-String -Pattern "LINK:(.+)" | ForEach-Object { $_.Matches.Groups[1].Value })
    
    Write-Host "======================================================================" -ForegroundColor Green
    Write-Host "User Details:" -ForegroundColor Cyan
    Write-Host "  Username: $username" -ForegroundColor White
    Write-Host "  Email: $email" -ForegroundColor White
    Write-Host "  Name: $name" -ForegroundColor White
    Write-Host "======================================================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "VERIFICATION LINK:" -ForegroundColor Yellow
    Write-Host "----------------------------------------------------------------------" -ForegroundColor Gray
    Write-Host $link -ForegroundColor Green
    Write-Host "----------------------------------------------------------------------" -ForegroundColor Gray
    Write-Host ""
    Write-Host "INSTRUCTIONS:" -ForegroundColor Cyan
    Write-Host "  1. Copy the link above" -ForegroundColor White
    Write-Host "  2. Paste it in your browser" -ForegroundColor White
    Write-Host "  3. Press Enter" -ForegroundColor White
    Write-Host "  4. Your account will be activated!" -ForegroundColor White
    Write-Host ""
    Write-Host "======================================================================" -ForegroundColor Green
}

cd ..
