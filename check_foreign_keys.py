import pymysql

conn = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='root',
    database='mylablink_db'
)

cursor = conn.cursor()

# Check if accounts_user exists
cursor.execute("SHOW TABLES LIKE 'accounts_user'")
accounts_user = cursor.fetchone()

# Check if accounts_customuser exists
cursor.execute("SHOW TABLES LIKE 'accounts_customuser'")
accounts_customuser = cursor.fetchone()

print("Table Status:")
print(f"  accounts_user exists: {accounts_user is not None}")
print(f"  accounts_customuser exists: {accounts_customuser is not None}")

# Check foreign keys on django_admin_log
cursor.execute("""
    SELECT 
        CONSTRAINT_NAME,
        COLUMN_NAME,
        REFERENCED_TABLE_NAME,
        REFERENCED_COLUMN_NAME
    FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
    WHERE TABLE_SCHEMA = 'mylablink_db'
    AND TABLE_NAME = 'django_admin_log'
    AND REFERENCED_TABLE_NAME IS NOT NULL
""")

fks = cursor.fetchall()
print("\nForeign Keys on django_admin_log:")
for fk in fks:
    print(f"  {fk[0]}: {fk[1]} -> {fk[2]}.{fk[3]}")

cursor.close()
conn.close()
