# Test Login API (JWT Authentication)
# ====================================

Write-Host "Testing Login API..." -ForegroundColor Cyan
Write-Host ""

$loginUrl = "http://127.0.0.1:8000/api/auth/token/"

# Prompt for credentials
Write-Host "Enter login credentials:" -ForegroundColor Yellow
$username = Read-Host "Username (or email)"
$password = Read-Host "Password" -AsSecureString
$passwordPlain = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($password))

# Create login data
$loginData = @{
    username = $username
    password = $passwordPlain
} | ConvertTo-Json

Write-Host ""
Write-Host "Sending login request to: $loginUrl" -ForegroundColor Gray
Write-Host ""

try {
    # Send login request
    $response = Invoke-RestMethod -Uri $loginUrl -Method Post -Body $loginData -ContentType "application/json"
    
    Write-Host "=====================================================================" -ForegroundColor Green
    Write-Host "SUCCESS! Login completed!" -ForegroundColor Green
    Write-Host "=====================================================================" -ForegroundColor Green
    Write-Host ""
    
    # Display tokens
    Write-Host "ACCESS TOKEN:" -ForegroundColor Cyan
    Write-Host "---------------------------------------------------------------------" -ForegroundColor Gray
    Write-Host $response.access -ForegroundColor Yellow
    Write-Host "---------------------------------------------------------------------" -ForegroundColor Gray
    Write-Host ""
    
    Write-Host "REFRESH TOKEN:" -ForegroundColor Cyan
    Write-Host "---------------------------------------------------------------------" -ForegroundColor Gray
    Write-Host $response.refresh -ForegroundColor Yellow
    Write-Host "---------------------------------------------------------------------" -ForegroundColor Gray
    Write-Host ""
    
    # Save tokens to file
    $tokensFile = "tokens.json"
    $response | ConvertTo-Json | Out-File -FilePath $tokensFile -Encoding UTF8
    
    Write-Host "Tokens saved to: $tokensFile" -ForegroundColor Green
    Write-Host ""
    
    Write-Host "=====================================================================" -ForegroundColor Cyan
    Write-Host "NEXT STEPS:" -ForegroundColor Yellow
    Write-Host "1. Copy the ACCESS token above" -ForegroundColor White
    Write-Host "2. Use it in Authorization header: 'Bearer <access_token>'" -ForegroundColor White
    Write-Host "3. Test protected endpoints (e.g., /api/accounts/me/)" -ForegroundColor White
    Write-Host "4. When access token expires, use refresh token to get new one" -ForegroundColor White
    Write-Host "=====================================================================" -ForegroundColor Cyan
    
    # Test the access token
    Write-Host ""
    Write-Host "Testing access token with /api/accounts/me/ ..." -ForegroundColor Yellow
    
    try {
        $headers = @{
            "Authorization" = "Bearer $($response.access)"
        }
        $meResponse = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/accounts/me/" -Method Get -Headers $headers
        
        Write-Host ""
        Write-Host "SUCCESS! User info retrieved:" -ForegroundColor Green
        Write-Host "---------------------------------------------------------------------" -ForegroundColor Gray
        $meResponse | ConvertTo-Json -Depth 3 | Write-Host -ForegroundColor White
        Write-Host "---------------------------------------------------------------------" -ForegroundColor Gray
        
    } catch {
        Write-Host ""
        Write-Host "Could not test /api/accounts/me/ endpoint" -ForegroundColor Yellow
        Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    }
    
} catch {
    Write-Host "=====================================================================" -ForegroundColor Red
    Write-Host "FAILED! Login error!" -ForegroundColor Red
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
    Write-Host "1. Username or password is incorrect" -ForegroundColor White
    Write-Host "2. User account is not activated (check email verification)" -ForegroundColor White
    Write-Host "3. User does not exist in database" -ForegroundColor White
}

Write-Host ""
Write-Host "Test completed" -ForegroundColor Cyan
