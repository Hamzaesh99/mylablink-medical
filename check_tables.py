import pymysql

conn = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='root',
    database='mylablink_db'
)

cursor = conn.cursor()
cursor.execute('SHOW TABLES')
tables = cursor.fetchall()

print("Tables in database:")
for table in tables:
    print(f"  - {table[0]}")

# Check for api_* tables specifically
api_tables = [t[0] for t in tables if t[0].startswith('api_')]
print("\nAPI tables:")
for table in api_tables:
    print(f"  - {table}")

cursor.close()
conn.close()
