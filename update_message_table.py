"""
Script to update api_message table structure
Handles foreign key constraints properly
"""
import os
import django
import pymysql

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mylablink_python.settings')
django.setup()

from django.conf import settings

# Get database settings
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
        print("\n📋 Step 1: Checking current table structure...")
        
        # Get all foreign keys on api_message table
        cursor.execute("""
            SELECT CONSTRAINT_NAME, COLUMN_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME
            FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
            WHERE TABLE_NAME = 'api_message'
            AND TABLE_SCHEMA = %s
            AND REFERENCED_TABLE_NAME IS NOT NULL
        """, (db_settings['NAME'],))
        
        foreign_keys = cursor.fetchall()
        fk_to_drop = []
        
        print(f"\n🔍 Found {len(foreign_keys)} foreign keys:")
        for fk in foreign_keys:
            print(f"  • {fk['CONSTRAINT_NAME']}: {fk['COLUMN_NAME']} -> {fk['REFERENCED_TABLE_NAME']}.{fk['REFERENCED_COLUMN_NAME']}")
            if fk['COLUMN_NAME'] in ['recipient_id', 'sender_id']:
                fk_to_drop.append(fk)
        
        # Step 2: Drop foreign keys
        if fk_to_drop:
            print(f"\n📋 Step 2: Dropping {len(fk_to_drop)} foreign key(s)...")
            for fk in fk_to_drop:
                print(f"  ➖ Dropping {fk['CONSTRAINT_NAME']}...")
                cursor.execute(f"""
                    ALTER TABLE api_message 
                    DROP FOREIGN KEY {fk['CONSTRAINT_NAME']}
                """)
                print(f"  ✅ Dropped {fk['CONSTRAINT_NAME']}")
        
        # Step 3: Rename recipient_id to receiver_id
        print("\n📋 Step 3: Renaming columns...")
        
        cursor.execute("""
            SELECT COLUMN_NAME 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = 'api_message' 
            AND TABLE_SCHEMA = %s
            AND COLUMN_NAME = 'recipient_id'
        """, (db_settings['NAME'],))
        
        if cursor.fetchone():
            print("  🔄 Renaming 'recipient_id' to 'receiver_id'...")
            cursor.execute("""
                ALTER TABLE api_message 
                CHANGE COLUMN recipient_id receiver_id INT(11) NOT NULL
            """)
            print("  ✅ Renamed 'recipient_id' to 'receiver_id'")
        else:
            print("  ℹ️  'recipient_id' not found, assuming already renamed")
        
        # Check if body exists and rename to content
        cursor.execute("""
            SELECT COLUMN_NAME 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = 'api_message' 
            AND TABLE_SCHEMA = %s
            AND COLUMN_NAME = 'body'
        """, (db_settings['NAME'],))
        
        if cursor.fetchone():
            print("  🔄 Renaming 'body' to 'content'...")
            cursor.execute("""
                ALTER TABLE api_message 
                CHANGE COLUMN body content LONGTEXT NOT NULL
            """)
            print("  ✅ Renamed 'body' to 'content'")
        
        # Rename created_at to timestamp
        cursor.execute("""
            SELECT COLUMN_NAME 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = 'api_message' 
            AND TABLE_SCHEMA = %s
            AND COLUMN_NAME = 'created_at'
        """, (db_settings['NAME'],))
        
        if cursor.fetchone():
            print("  🔄 Renaming 'created_at' to 'timestamp'...")
            cursor.execute("""
                ALTER TABLE api_message 
                CHANGE COLUMN created_at timestamp DATETIME(6) NOT NULL
            """)
            print("  ✅ Renamed 'created_at' to 'timestamp'")
        
        # Step 4: Add file_attachment column
        print("\n📋 Step 4: Adding new columns...")
        
        cursor.execute("""
            SELECT COLUMN_NAME 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = 'api_message' 
            AND TABLE_SCHEMA = %s
            AND COLUMN_NAME = 'file_attachment'
        """, (db_settings['NAME'],))
        
        if not cursor.fetchone():
            print("  ➕ Adding 'file_attachment' column...")
            cursor.execute("""
                ALTER TABLE api_message 
                ADD COLUMN file_attachment VARCHAR(100) NULL
            """)
            print("  ✅ Added 'file_attachment' column")
        else:
            print("  ✅ 'file_attachment' already exists")
        
        # Step 5: Remove subject column
        print("\n📋 Step 5: Removing obsolete columns...")
        
        cursor.execute("""
            SELECT COLUMN_NAME 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = 'api_message' 
            AND TABLE_SCHEMA = %s
            AND COLUMN_NAME = 'subject'
        """, (db_settings['NAME'],))
        
        if cursor.fetchone():
            print("  ➖ Removing 'subject' column...")
            cursor.execute("""
                ALTER TABLE api_message 
                DROP COLUMN subject
            """)
            print("  ✅ Removed 'subject' column")
        
        # Step 6: Recreate foreign keys
        print("\n📋 Step 6: Recreating foreign keys...")
        
        # Add sender_id foreign key
        print("  ➕ Adding sender_id foreign key...")
        cursor.execute("""
            ALTER TABLE api_message 
            ADD CONSTRAINT api_message_sender_id_fk 
            FOREIGN KEY (sender_id) 
            REFERENCES accounts_customuser(id)
            ON DELETE CASCADE
        """)
        print("  ✅ Added sender_id foreign key")
        
        # Add receiver_id foreign key
        print("  ➕ Adding receiver_id foreign key...")
        cursor.execute("""
            ALTER TABLE api_message 
            ADD CONSTRAINT api_message_receiver_id_fk 
            FOREIGN KEY (receiver_id) 
            REFERENCES accounts_customuser(id)
            ON DELETE CASCADE
        """)
        print("  ✅ Added receiver_id foreign key")
        
        connection.commit()
        
        print("\n" + "="*60)
        print("✅ Database update completed successfully!")
        print("="*60)
        
        # Show final structure
        print("\n📊 Final table structure:")
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
        
        print("\n🎉 You can now restart the server and test the chat system!")
        
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("Rolling back changes...")
    connection.rollback()
    import traceback
    traceback.print_exc()
finally:
    connection.close()
    print("\n🔌 Database connection closed")
