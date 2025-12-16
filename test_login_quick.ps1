# Quick Login Test
# ================

Write-Host "Quick Login Test" -ForegroundColor Cyan
Write-Host ""

# Test credentials - UPDATE THESE WITH YOUR ACTUAL CREDENTIALS
$username = "test@example.com"
$password = "TestPass123!"

Write-Host "Testing login with:" -ForegroundColor Yellow
Write-Host "  Username: $username" -ForegroundColor Gray
Write-Host "  Password: ********" -ForegroundColor Gray
Write-Host ""

$loginUrl = "http://127.0.0.1:8000/api/auth/token/"

$loginData = @{
    username = $username
    password = $password
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri $loginUrl -Method Post -Body $loginData -ContentType "application/json"
    
    Write-Host "SUCCESS!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Access Token:" -ForegroundColor Cyan
    Write-Host $response.access -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Refresh Token:" -ForegroundColor Cyan
    Write-Host $response.refresh -ForegroundColor Yellow
    Write-Host ""
    
    # Save to file
    $response | ConvertTo-Json | Out-File -FilePath "tokens.json" -Encoding UTF8
    Write-Host "Tokens saved to tokens.json" -ForegroundColor Green
    
} catch {
    Write-Host "FAILED!" -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    
    if ($_.ErrorDetails.Message) {
        Write-Host ""
        Write-Host "Server response:" -ForegroundColor Yellow
        $_.ErrorDetails.Message | Write-Host -ForegroundColor Red
    }
}
