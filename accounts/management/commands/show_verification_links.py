from django.core.management.base import BaseCommand
from accounts.models import CustomUser
from accounts.utils import generate_email_token
import webbrowser
import os


class Command(BaseCommand):
    help = 'Generate email verification link and open in browser'

    def handle(self, *args, **options):
        inactive_users = CustomUser.objects.filter(is_active=False)
        
        if not inactive_users.exists():
            self.stdout.write(self.style.WARNING('No inactive users found!'))
            return
        
        # Create HTML file
        html_content = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Verification Links</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background: #f5f5f5;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #dc2626;
            text-align: center;
        }
        .user-card {
            background: #f9fafb;
            padding: 20px;
            margin: 20px 0;
            border-radius: 8px;
            border-left: 4px solid #dc2626;
        }
        .user-info {
            margin-bottom: 15px;
        }
        .user-info strong {
            color: #374151;
        }
        .link-box {
            background: #fff;
            padding: 15px;
            border-radius: 6px;
            border: 2px solid #dc2626;
            margin: 10px 0;
            word-break: break-all;
        }
        .link-box a {
            color: #dc2626;
            text-decoration: none;
            font-weight: bold;
        }
        .link-box a:hover {
            text-decoration: underline;
        }
        .instructions {
            background: #fef3c7;
            padding: 15px;
            border-radius: 6px;
            margin-top: 20px;
        }
        .instructions h3 {
            margin-top: 0;
            color: #92400e;
        }
        .instructions ol {
            margin: 10px 0;
        }
        .copy-btn {
            background: #dc2626;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            cursor: pointer;
            margin-top: 10px;
        }
        .copy-btn:hover {
            background: #b91c1c;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔗 روابط تفعيل الحسابات</h1>
        
"""
        
        for user in inactive_users:
            token = generate_email_token(user)
            link = f"http://127.0.0.1:8000/api/accounts/verify-email/{token}/"
            
            html_content += f"""
        <div class="user-card">
            <div class="user-info">
                <strong>اسم المستخدم:</strong> {user.username}<br>
                <strong>البريد الإلكتروني:</strong> {user.email}<br>
                <strong>الاسم:</strong> {user.first_name or 'غير محدد'}
            </div>
            <div class="link-box">
                <a href="{link}" target="_blank">{link}</a>
                <br>
                <button class="copy-btn" onclick="navigator.clipboard.writeText('{link}').then(() => alert('تم نسخ الرابط!'))">📋 نسخ الرابط</button>
            </div>
        </div>
"""
        
        html_content += """
        <div class="instructions">
            <h3>📝 التعليمات:</h3>
            <ol>
                <li>انقر على الرابط أعلاه (سيفتح في نافذة جديدة)</li>
                <li>أو انسخ الرابط والصقه في المتصفح</li>
                <li>سيتم تفعيل الحساب تلقائياً</li>
                <li>بعد التفعيل، يمكنك تسجيل الدخول</li>
            </ol>
        </div>
    </div>
</body>
</html>
"""
        
        # Save HTML file
        html_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'verification_links.html')
        html_path = os.path.abspath(html_path)
        
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        self.stdout.write(self.style.SUCCESS(f'✓ HTML file created: {html_path}'))
        self.stdout.write(self.style.SUCCESS(f'✓ Found {inactive_users.count()} inactive user(s)'))
        self.stdout.write(self.style.SUCCESS('✓ Opening in browser...'))
        
        # Open in browser
        webbrowser.open('file://' + html_path)
        
        self.stdout.write(self.style.SUCCESS('✓ Done!'))
