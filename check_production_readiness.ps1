# Production Readiness Check Script
# ==================================

Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host "MyLabLink - Production Readiness Check" -ForegroundColor Cyan
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host ""

$checks = @()
$passed = 0
$failed = 0

# Function to add check result
function Add-Check {
    param($name, $status, $message)
    $script:checks += @{Name=$name; Status=$status; Message=$message}
    if ($status) { $script:passed++ } else { $script:failed++ }
}

Write-Host "Running production readiness checks..." -ForegroundColor Yellow
Write-Host ""

# Check 1: .env file exists
Write-Host "1. Checking .env file..." -ForegroundColor Gray
if (Test-Path "backend\mylablink_python\.env") {
    Add-Check ".env file" $true "Found"
    Write-Host "   OK - .env file exists" -ForegroundColor Green
} else {
    Add-Check ".env file" $false "Not found - copy from .env.example"
    Write-Host "   FAIL - .env file not found!" -ForegroundColor Red
}

# Check 2: .gitignore exists
Write-Host "2. Checking .gitignore..." -ForegroundColor Gray
if (Test-Path ".gitignore") {
    Add-Check ".gitignore" $true "Found"
    Write-Host "   OK - .gitignore exists" -ForegroundColor Green
} else {
    Add-Check ".gitignore" $false "Not found"
    Write-Host "   FAIL - .gitignore not found!" -ForegroundColor Red
}

# Check 3: requirements.txt exists
Write-Host "3. Checking requirements.txt..." -ForegroundColor Gray
if (Test-Path "backend\requirements.txt") {
    Add-Check "requirements.txt" $true "Found"
    Write-Host "   OK - requirements.txt exists" -ForegroundColor Green
} else {
    Add-Check "requirements.txt" $false "Not found"
    Write-Host "   FAIL - requirements.txt not found!" -ForegroundColor Red
}

# Check 4: Database connection
Write-Host "4. Checking database connection..." -ForegroundColor Gray
try {
    $output = python backend\manage.py check --database default 2>&1
    if ($LASTEXITCODE -eq 0) {
        Add-Check "Database" $true "Connected"
        Write-Host "   OK - Database connection successful" -ForegroundColor Green
    } else {
        Add-Check "Database" $false "Connection failed"
        Write-Host "   FAIL - Database connection failed!" -ForegroundColor Red
    }
} catch {
    Add-Check "Database" $false "Error checking"
    Write-Host "   FAIL - Error checking database!" -ForegroundColor Red
}

# Check 5: Migrations
Write-Host "5. Checking migrations..." -ForegroundColor Gray
try {
    $output = python backend\manage.py showmigrations 2>&1
    if ($output -match "\[ \]") {
        Add-Check "Migrations" $false "Unapplied migrations found"
        Write-Host "   WARNING - Unapplied migrations found!" -ForegroundColor Yellow
    } else {
        Add-Check "Migrations" $true "All applied"
        Write-Host "   OK - All migrations applied" -ForegroundColor Green
    }
} catch {
    Add-Check "Migrations" $false "Error checking"
    Write-Host "   FAIL - Error checking migrations!" -ForegroundColor Red
}

# Check 6: Static files
Write-Host "6. Checking static files..." -ForegroundColor Gray
if (Test-Path "backend\staticfiles") {
    Add-Check "Static files" $true "Collected"
    Write-Host "   OK - Static files collected" -ForegroundColor Green
} else {
    Add-Check "Static files" $false "Not collected - run collectstatic"
    Write-Host "   WARNING - Static files not collected!" -ForegroundColor Yellow
}

# Check 7: SECRET_KEY in .env
Write-Host "7. Checking SECRET_KEY..." -ForegroundColor Gray
if (Test-Path "backend\mylablink_python\.env") {
    $envContent = Get-Content "backend\mylablink_python\.env" -Raw
    if ($envContent -match "SECRET_KEY=.+") {
        Add-Check "SECRET_KEY" $true "Set in .env"
        Write-Host "   OK - SECRET_KEY is set" -ForegroundColor Green
    } else {
        Add-Check "SECRET_KEY" $false "Not set in .env"
        Write-Host "   WARNING - SECRET_KEY not set!" -ForegroundColor Yellow
    }
}

# Check 8: Email configuration
Write-Host "8. Checking email configuration..." -ForegroundColor Gray
if (Test-Path "backend\mylablink_python\.env") {
    $envContent = Get-Content "backend\mylablink_python\.env" -Raw
    if ($envContent -match "EMAIL_HOST_USER=.+@.+") {
        Add-Check "Email config" $true "Configured"
        Write-Host "   OK - Email is configured" -ForegroundColor Green
    } else {
        Add-Check "Email config" $false "Not configured"
        Write-Host "   WARNING - Email not configured!" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host "Summary" -ForegroundColor Cyan
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host ""

foreach ($check in $checks) {
    $status = if ($check.Status) { "PASS" } else { "FAIL" }
    $color = if ($check.Status) { "Green" } else { "Red" }
    Write-Host "[$status] $($check.Name): $($check.Message)" -ForegroundColor $color
}

Write-Host ""
Write-Host "Total: $passed passed, $failed failed" -ForegroundColor $(if ($failed -eq 0) { "Green" } else { "Yellow" })
Write-Host ""

if ($failed -eq 0) {
    Write-Host "=====================================================================" -ForegroundColor Green
    Write-Host "All checks passed! Your application is ready for production!" -ForegroundColor Green
    Write-Host "=====================================================================" -ForegroundColor Green
} else {
    Write-Host "=====================================================================" -ForegroundColor Yellow
    Write-Host "Some checks failed. Please review and fix before deploying." -ForegroundColor Yellow
    Write-Host "=====================================================================" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Next steps for production:" -ForegroundColor Cyan
Write-Host "1. Review دليل_النشر_للإنتاج.md" -ForegroundColor White
Write-Host "2. Set up SMTP email" -ForegroundColor White
Write-Host "3. Configure PostgreSQL" -ForegroundColor White
Write-Host "4. Enable HTTPS" -ForegroundColor White
Write-Host "5. Add Rate Limiting" -ForegroundColor White
Write-Host "6. Run collectstatic" -ForegroundColor White
Write-Host "7. Deploy to production server" -ForegroundColor White
Write-Host ""
