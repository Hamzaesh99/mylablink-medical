import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mylablink_python.settings')
django.setup()

from django.db import connection

def check_columns():
    with connection.cursor() as cursor:
        cursor.execute("DESCRIBE api_message")
        columns = [col[0] for col in cursor.fetchall()]
        print("Columns in api_message:", columns)

check_columns()
