# Test with your actual token
# ==========================

Write-Host "Testing with your Access Token..." -ForegroundColor Cyan
Write-Host ""

# Your actual access token
$accessToken = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzYzODIyNzA5LCJpYXQiOjE3NjM4MTkxMDksImp0aSI6IjBlZTg5M2Y0NzgyYTQyODhhNzAxMDJkYmYwMWVhYjI4IiwidXNlcl9pZCI6IjIifQ.Xmhq9ONupO9nWaYtepgkmPrTlGUguo9X_64n1ZGWErg"

# Create authorization header
$headers = @{
    "Authorization" = "Bearer $accessToken"
}

Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host "Testing Protected Endpoints" -ForegroundColor Cyan
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host ""

# Test 1: Get current user info
Write-Host "1. GET /api/accounts/me/" -ForegroundColor Yellow
Write-Host "   Getting your user information..." -ForegroundColor Gray
Write-Host ""

try {
    $response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/accounts/me/" -Method Get -Headers $headers
    
    Write-Host "   SUCCESS!" -ForegroundColor Green
    Write-Host "   =====================================================================" -ForegroundColor Green
    Write-Host "   YOUR USER INFORMATION:" -ForegroundColor Cyan
    Write-Host "   =====================================================================" -ForegroundColor Green
    Write-Host "   ID:         $($response.id)" -ForegroundColor White
    Write-Host "   Username:   $($response.username)" -ForegroundColor White
    Write-Host "   Email:      $($response.email)" -ForegroundColor White
    Write-Host "   Name:       $($response.first_name) $($response.last_name)" -ForegroundColor White
    Write-Host "   Role:       $($response.role)" -ForegroundColor White
    Write-Host "   Phone:      $($response.phone)" -ForegroundColor White
    Write-Host "   Active:     $($response.is_active)" -ForegroundColor White
    Write-Host "   =====================================================================" -ForegroundColor Green
    Write-Host ""
    
    # Save full response
    Write-Host "   Full Response:" -ForegroundColor Cyan
    $response | ConvertTo-Json -Depth 3 | Write-Host -ForegroundColor Gray
    Write-Host ""
    
} catch {
    Write-Host "   FAILED!" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
    
    if ($_.ErrorDetails.Message) {
        Write-Host "   Server response:" -ForegroundColor Yellow
        $_.ErrorDetails.Message | Write-Host -ForegroundColor Red
    }
    Write-Host ""
}

Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host "Test completed!" -ForegroundColor Cyan
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "NEXT STEPS:" -ForegroundColor Yellow
Write-Host "1. You can now use this token to access all protected endpoints" -ForegroundColor White
Write-Host "2. Try updating your profile: PATCH /api/accounts/me/" -ForegroundColor White
Write-Host "3. Try changing password: POST /api/accounts/change-password/" -ForegroundColor White
Write-Host "4. When token expires, use refresh token to get a new one" -ForegroundColor White
Write-Host ""
