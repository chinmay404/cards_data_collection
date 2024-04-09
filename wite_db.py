import json
import psycopg2  
import streamlit as st



@st.cache_data
def write_to_db(data):
    try:
        with open('config.json') as f:
            config = json.load(f)

        conn = psycopg2.connect(**config['database'])
        cur = conn.cursor()
        sql = f"""INSERT INTO {config['table']['name']} (
            name, company_name, job_title, website, email, phone_number,
            office_phone_number, address, additional_info
        ) VALUES (
            %(name)s, %(company_name)s, %(job_title)s, %(website)s, %(email)s, %(phone_number)s,
            %(office_phone_number)s, %(address)s, %(additional_info)s
        )"""
        cur.execute(sql, data)
        conn.commit()
        

    except Exception as e:
        st.error(f"Databse error : {e}")
        print("Error:", e)

    finally:
        st.success('Added To database succesfully', icon="✅")
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()



def fetch_data():
    try:
        with open('config.json') as f:
            config = json.load(f)
        conn = psycopg2.connect(**config['database'])
        cur = conn.cursor()
        sql = f"SELECT * FROM {config['table']['name']}"
        cur.execute(sql)
        rows = cur.fetchall()
        print(rows)
        return rows

    except Exception as e:
        print("Error:", e)

    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()