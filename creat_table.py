import psycopg2
import json

try:
    with open('config.json') as f:
        config = json.load(f)
    conn = psycopg2.connect(**config['database'])
    cur = conn.cursor()
    sql = f"""CREATE TABLE IF NOT EXISTS {config['table']['name']} (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255),
        company_name VARCHAR(255),
        job_title VARCHAR(255),
        website VARCHAR(255),
        email VARCHAR(255),
        phone_number VARCHAR(20),
        office_phone_number VARCHAR(20),
        address TEXT,
        additional_info TEXT
    )"""
    cur.execute(sql)
    conn.commit()
    print("Done")

except psycopg2.Error as e:
    print("Error:", e)

finally:
    if 'cur' in locals():
        cur.close()
    if 'conn' in locals():
        conn.close()
