#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Quick Test Script - MyLabLink Medical Lab
Tests the Notification API endpoint to verify the fix
"""

import requests
import json

def test_notifications_api():
    """Test the notifications API endpoint"""
    
    print("=" * 70)
    print("🧪 اختبار API الإشعارات")
    print("=" * 70)
    print()
    
    url = "http://127.0.0.1:8000/api/notifications/"
    
    print(f"📡 إرسال طلب إلى: {url}")
    print()
    
    try:
        response = requests.get(url, timeout=5)
        
        print(f"📊 حالة الاستجابة: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ النجاح! API يعمل بشكل صحيح")
            print()
            
            data = response.json()
            print(f"📦 عدد الإشعارات: {len(data)}")
            
            if len(data) > 0:
                print()
                print("📋 أول إشعار:")
                print(json.dumps(data[0], indent=2, ensure_ascii=False))
        
        elif response.status_code == 401:
            print("🔐 يتطلب تسجيل دخول (متوقع)")
            print("✅ API يعمل لكن يحتاج authentication")
        
        else:
            print(f"⚠️ حالة غير متوقعة: {response.status_code}")
            print(response.text[:500])
            
    except requests.exceptions.ConnectionError:
        print("❌ لا يمكن الاتصال بالسيرفر")
        print("💡 تأكد من تشغيل السيرفر أولاً:")
        print("   python manage.py runserver")
        
    except Exception as e:
        print(f"❌ خطأ: {e}")
    
    print()
    print("=" * 70)

if __name__ == "__main__":
    test_notifications_api()
