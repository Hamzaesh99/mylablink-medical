"""
Check data types and fix incompatibility
"""
import os
import django
import pymysql

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mylablink_python.settings')
django.setup()

from django.conf import settings

db_settings = settings.DATABASES['default']

print("🔧 Connecting to database...")
connection = pymysql.connect(
    host=db_settings['HOST'],
    user=db_settings['USER'],
    password=db_settings['PASSWORD'],
    database=db_settings['NAME'],
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

try:
    with connection.cursor() as cursor:
        # Check id column type in accounts_customuser
        cursor.execute("""
            SELECT COLUMN_TYPE 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = 'accounts_customuser' 
            AND COLUMN_NAME = 'id'
            AND TABLE_SCHEMA = %s
        """, (db_settings['NAME'],))
        
        user_id_type = cursor.fetchone()
        print(f"\n📊 accounts_customuser.id type: {user_id_type['COLUMN_TYPE']}")
        
        # Check receiver_id and sender_id types
        cursor.execute("""
            SELECT COLUMN_NAME, COLUMN_TYPE 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = 'api_message' 
            AND COLUMN_NAME IN ('receiver_id', 'sender_id')
            AND TABLE_SCHEMA = %s
        """, (db_settings['NAME'],))
        
        message_cols = cursor.fetchall()
        print(f"\n📊 api_message foreign key columns:")
        for col in message_cols:
            print(f"  • {col['COLUMN_NAME']}: {col['COLUMN_TYPE']}")
        
        # Extract the base type (bigint or int)
        target_type = user_id_type['COLUMN_TYPE'].upper()
        
        print(f"\n🔧 Will update foreign keys to match: {target_type}")
        
        # Update receiver_id type
        print("\n  🔄 Updating receiver_id to match...")
        cursor.execute(f"""
            ALTER TABLE api_message 
            MODIFY COLUMN receiver_id {target_type} NOT NULL
        """)
        print("  ✅ Updated receiver_id")
        
        # Update sender_id type
        print("  🔄 Updating sender_id to match...")
        cursor.execute(f"""
            ALTER TABLE api_message 
            MODIFY COLUMN sender_id {target_type} NOT NULL
        """)
        print("  ✅ Updated sender_id")
        
        # Now add foreign keys
        print("\n🔗 Adding foreign keys...")
        
        # Check if sender_id FK already exists
        cursor.execute(f"""
            SELECT CONSTRAINT_NAME 
            FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
            WHERE TABLE_NAME = 'api_message'
            AND COLUMN_NAME = 'sender_id'
            AND CONSTRAINT_NAME LIKE '%fk%'
            AND TABLE_SCHEMA = '{db_settings['NAME']}'
        """)
        
        if not cursor.fetchone():
            print("  ➕ Adding sender_id foreign key...")
            cursor.execute("""
                ALTER TABLE api_message 
                ADD CONSTRAINT api_message_sender_id_fk 
                FOREIGN KEY (sender_id) 
                REFERENCES accounts_customuser(id)
                ON DELETE CASCADE
            """)
            print("  ✅ Added sender_id foreign key")
        else:
            print("  ✅ sender_id foreign key already exists")
        
        # Check if receiver_id FK already exists
        cursor.execute(f"""
            SELECT CONSTRAINT_NAME 
            FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
            WHERE TABLE_NAME = 'api_message'
            AND COLUMN_NAME = 'receiver_id'
            AND CONSTRAINT_NAME LIKE '%fk%'
            AND TABLE_SCHEMA = '{db_settings['NAME']}'
        """)
        
        if not cursor.fetchone():
            print("  ➕ Adding receiver_id foreign key...")
            cursor.execute("""
                ALTER TABLE api_message 
                ADD CONSTRAINT api_message_receiver_id_fk 
                FOREIGN KEY (receiver_id) 
                REFERENCES accounts_customuser(id)
                ON DELETE CASCADE
            """)
            print("  ✅ Added receiver_id foreign key")
        else:
            print("  ✅ receiver_id foreign key already exists")
        
        connection.commit()
        
        print("\n" + "="*60)
        print("✅ All fixes completed successfully!")
        print("="*60)
        
        # Final verification
        print("\n📊 Final column types:")
        cursor.execute("""
            SELECT COLUMN_NAME, COLUMN_TYPE, IS_NULLABLE
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = 'api_message' 
            AND TABLE_SCHEMA = %s
            ORDER BY ORDINAL_POSITION
        """, (db_settings['NAME'],))
        
        columns = cursor.fetchall()
        for col in columns:
            nullable = "NULL" if col['IS_NULLABLE'] == 'YES' else "NOT NULL"
            print(f"  • {col['COLUMN_NAME']}: {col['COLUMN_TYPE']} {nullable}")
        
        print("\n🎉 Database is ready! Restart the server and test!")
        
except Exception as e:
    print(f"\n❌ Error: {e}")
    connection.rollback()
    import traceback
    traceback.print_exc()
finally:
    connection.close()
    print("\n🔌 Database connection closed")
