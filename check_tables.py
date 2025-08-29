import psycopg2

connection = psycopg2.connect(
    host="aws-1-eu-north-1.pooler.supabase.com",
    database="postgres",
    user="postgres.uoouexfczqhdqjrvtsjn",
    password="zSDUjdsAZT4xmwEh",
    port=5432
)

with connection.cursor() as cursor:
    # Check tokens table structure
    cursor.execute("""
        SELECT column_name, data_type, is_nullable 
        FROM information_schema.columns 
        WHERE table_name = 'tokens'
    """)
    print("TOKENS TABLE:")
    for row in cursor.fetchall():
        print(f"  {row[0]} - {row[1]} - nullable: {row[2]}")
    
    # Check moves table structure  
    cursor.execute("""
        SELECT column_name, data_type, is_nullable 
        FROM information_schema.columns 
        WHERE table_name = 'moves'
    """)
    print("\nMOVES TABLE:")
    for row in cursor.fetchall():
        print(f"  {row[0]} - {row[1]} - nullable: {row[2]}")

connection.close()