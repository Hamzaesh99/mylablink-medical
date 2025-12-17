import pymysql

# Connect to MySQL (without selecting a database)
conn = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='root'
)

cursor = conn.cursor()

print("Dropping and recreating database...")
cursor.execute("DROP DATABASE IF EXISTS mylablink_db")
cursor.execute("CREATE DATABASE mylablink_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
print("✓ Database mylablink_db recreated successfully!")

cursor.close()
conn.close()
