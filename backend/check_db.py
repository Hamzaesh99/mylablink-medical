import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mylablink_python.settings')
django.setup()

from django.db import connection, OperationalError

def check_table():
    with connection.cursor() as cursor:
        try:
            cursor.execute("SHOW TABLES LIKE 'api_testimonial'")
            row = cursor.fetchone()
            if row:
                print("TABLE_EXISTS")
            else:
                print("TABLE_DOES_NOT_EXIST")
        except OperationalError as e:
            print(f"Error: {e}")

check_table()
