# Test Token Refresh
# ===================

Write-Host "Testing Token Refresh..." -ForegroundColor Cyan
Write-Host ""

# Check if tokens.json exists
if (Test-Path "tokens.json") {
    Write-Host "Loading tokens from tokens.json..." -ForegroundColor Gray
    $tokens = Get-Content "tokens.json" | ConvertFrom-Json
    $refreshToken = $tokens.refresh
    
    Write-Host "Refresh Token found!" -ForegroundColor Green
    Write-Host ""
} else {
    Write-Host "No tokens.json file found!" -ForegroundColor Yellow
    Write-Host "Please run test_login.ps1 first to get tokens." -ForegroundColor Yellow
    exit
}

$refreshUrl = "http://127.0.0.1:8000/api/auth/token/refresh/"

$refreshData = @{
    refresh = $refreshToken
} | ConvertTo-Json

Write-Host "Sending refresh request to: $refreshUrl" -ForegroundColor Gray
Write-Host ""

try {
    $response = Invoke-RestMethod -Uri $refreshUrl -Method Post -Body $refreshData -ContentType "application/json"
    
    Write-Host "=====================================================================" -ForegroundColor Green
    Write-Host "SUCCESS! Token refreshed!" -ForegroundColor Green
    Write-Host "=====================================================================" -ForegroundColor Green
    Write-Host ""
    
    Write-Host "NEW ACCESS TOKEN:" -ForegroundColor Cyan
    Write-Host "---------------------------------------------------------------------" -ForegroundColor Gray
    Write-Host $response.access -ForegroundColor Yellow
    Write-Host "---------------------------------------------------------------------" -ForegroundColor Gray
    Write-Host ""
    
    # Update tokens file
    $tokens.access = $response.access
    $tokens | ConvertTo-Json | Out-File -FilePath "tokens.json" -Encoding UTF8
    
    Write-Host "Updated tokens saved to tokens.json" -ForegroundColor Green
    Write-Host ""
    Write-Host "=====================================================================" -ForegroundColor Cyan
    Write-Host "You can now use the new access token for API requests!" -ForegroundColor White
    Write-Host "=====================================================================" -ForegroundColor Cyan
    
} catch {
    Write-Host "=====================================================================" -ForegroundColor Red
    Write-Host "FAILED! Token refresh error!" -ForegroundColor Red
    Write-Host "=====================================================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "Error details:" -ForegroundColor Yellow
    Write-Host $_.Exception.Message -ForegroundColor Red
    
    if ($_.ErrorDetails.Message) {
        Write-Host ""
        Write-Host "Server response:" -ForegroundColor Yellow
        $_.ErrorDetails.Message | Write-Host -ForegroundColor Red
    }
    
    Write-Host ""
    Write-Host "Possible reasons:" -ForegroundColor Yellow
    Write-Host "1. Refresh token has expired" -ForegroundColor White
    Write-Host "2. Refresh token is invalid" -ForegroundColor White
    Write-Host "3. You need to login again" -ForegroundColor White
}

Write-Host ""
Write-Host "Test completed" -ForegroundColor Cyan
