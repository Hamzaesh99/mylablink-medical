import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mylablink_python.settings')
django.setup()

from django.db import connection

def create_table():
    with connection.cursor() as cursor:
        try:
            # Create Testimonial Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS api_testimonial (
                    id bigint AUTO_INCREMENT NOT NULL PRIMARY KEY,
                    content longtext NOT NULL,
                    rating smallint UNSIGNED NOT NULL,
                    is_approved bool NOT NULL,
                    created_at datetime(6) NOT NULL,
                    user_id bigint NOT NULL,
                    CONSTRAINT api_testimonial_user_id_fk_accounts_customuser_id FOREIGN KEY (user_id) REFERENCES accounts_customuser (id)
                )
            """)
            print("Table api_testimonial created.")
        except Exception as e:
            print(f"Error creating table: {e}")

create_table()
