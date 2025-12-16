# Git Conflict Resolution and Push Script
# حل تعارض Git ورفع الكود

Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "Git Conflict Resolution & Push Helper" -ForegroundColor Green
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host ""

# 1. التحقق من حالة Git
Write-Host "1️⃣ Checking Git status..." -ForegroundColor Yellow
git status
Write-Host ""

# 2. إضافة ملف .gitignore بعد حل التعارض
Write-Host "2️⃣ Adding resolved .gitignore..." -ForegroundColor Yellow
git add .gitignore
Write-Host "✅ .gitignore added" -ForegroundColor Green
Write-Host ""

# 3. إكمال عملية الدمج
Write-Host "3️⃣ Completing merge..." -ForegroundColor Yellow
git commit -m "Resolve .gitignore merge conflict"
Write-Host "✅ Merge conflict resolved" -ForegroundColor Green
Write-Host ""

# 4. إضافة ملفات النشر الجديدة
Write-Host "4️⃣ Adding deployment files..." -ForegroundColor Yellow
git add build.sh
git add render.yaml
git add requirements-render.txt
git add .env.render.example
git add .gitattributes
git add backend/Procfile
git add backend/mylablink_python/settings_production.py
git add backend/mylablink_python/settings.py
git add DEPLOYMENT_FILES.md
git add README_DEPLOYMENT.md
git add DEPLOYMENT_CHECKLIST.md
git add QUICK_COMMANDS.md
git add RENDER_DEPLOYMENT.md
Write-Host "✅ Deployment files added" -ForegroundColor Green
Write-Host ""

# 5. Commit جديد
Write-Host "5️⃣ Committing changes..." -ForegroundColor Yellow
git commit -m "Add complete Render deployment configuration

- Add build.sh for automated deployment
- Add Procfile for Gunicorn configuration
- Add render.yaml for Render configuration
- Add requirements-render.txt for PostgreSQL support
- Update settings.py with WhiteNoise
- Update settings_production.py with DATABASE_URL support
- Add comprehensive deployment documentation (5 files)
- Add .gitattributes for proper line endings
- Add .env.render.example for environment variables reference
"
Write-Host "✅ Changes committed" -ForegroundColor Green
Write-Host ""

# 6. عرض الحالة الحالية
Write-Host "6️⃣ Current Git status:" -ForegroundColor Yellow
git status
Write-Host ""

# 7. Push إلى GitHub
Write-Host "7️⃣ Ready to push to GitHub" -ForegroundColor Yellow
Write-Host "Do you want to push now? (Y/N)" -ForegroundColor Cyan
$response = Read-Host

if ($response -eq "Y" -or $response -eq "y") {
    Write-Host "Pushing to origin main..." -ForegroundColor Yellow
    git push origin main
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "=" * 60 -ForegroundColor Green
        Write-Host "🎉 SUCCESS! Code pushed to GitHub!" -ForegroundColor Green
        Write-Host "=" * 60 -ForegroundColor Green
        Write-Host ""
        Write-Host "Next steps:" -ForegroundColor Cyan
        Write-Host "1. Go to Render.com and create a new Web Service" -ForegroundColor White
        Write-Host "2. Connect your GitHub repository" -ForegroundColor White
        Write-Host "3. Follow the guide in DEPLOYMENT_FILES.md" -ForegroundColor White
        Write-Host ""
    }
    else {
        Write-Host ""
        Write-Host "⚠️ Push failed. Please check the error above." -ForegroundColor Red
        Write-Host ""
    }
}
else {
    Write-Host ""
    Write-Host "Push cancelled. You can push manually later with:" -ForegroundColor Yellow
    Write-Host "git push origin main" -ForegroundColor White
    Write-Host ""
}

Write-Host "Script completed!" -ForegroundColor Green
