from connection import engine

try:
    connection = engine.connect()
    print("✅ Successfully connected to PostgreSQL!")
    connection.close()

except Exception as e:
    print("❌ Connection Failed!")
    print(e)