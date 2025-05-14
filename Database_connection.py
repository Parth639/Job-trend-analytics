# import psycopg2
# import pandas as pd
# from API_Call import fetch_jobs

# # Function to store data into PostgreSQL
# def store_data_into_postgresql(df):
#     try:
#         # Connect to PostgreSQL
#         # conn = psycopg2.connect(
#         #     dbname="job_data",      # Your database name
#         #     user="postgres",       # Your PostgreSQL username
#         #     password="parth123", # Your PostgreSQL password
#         #     host="localhost",        # Change if you're using a different host
#         #     port="5432"              # Default PostgreSQL port
#         # )
#         conn = psycopg2.connect(
#             dbname="postgres",      # Your database name
#             user="postgres",       # Your PostgreSQL username
#             password="npg_N0hQBexPLUM6", # Your PostgreSQL password
#             host="db.dcncknstzdtdvrbmjzzo.supabase.co",        # Change if you're using a different host
#             port="5432"              # Default PostgreSQL port
#         )
#         cursor = conn.cursor()

#         # Iterate over the DataFrame rows and insert each record into the PostgreSQL table
#         for _, row in df.iterrows():
#            cursor.execute("""
#             INSERT INTO jobs (job_title, company, location, date_posted, freshness, age_category)
#             VALUES (%s, %s, %s, %s, %s, %s)
#             ON CONFLICT (job_title, company, date_posted) DO NOTHING;
#         """, (
#             row['job_title'],
#             row['company'],
#             row['location'],
#             row['date_posted'],
#             row['freshness'],
#             row['age_category']
#             ))

#         # Commit the transaction
#         conn.commit()

#     except Exception as e:
#         print(f"Error while inserting data into PostgreSQL: {e}")
#     finally:
#         cursor.close()
#         conn.close()


# # Assuming 'df' is your DataFrame containing the job data.
# # For example, 'df' could be the DataFrame you generated after fetching data from the API
# # store_data_into_postgresql(df)
import psycopg2
import pandas as pd
from API_Call import fetch_jobs

def store_data_into_postgresql(df):
    conn = None
    cursor = None
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres.dcncknstzdtdvrbmjzzo",
            password="9gcybtcn203",
            host="aws-0-ap-south-1.pooler.supabase.com",
            port="5432"
        )
        cursor = conn.cursor()

        # Iterate and insert rows
        for _, row in df.iterrows():
            cursor.execute("""
                INSERT INTO jobs (job_title, company, location, date_posted, freshness, age_category)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (job_title, company, date_posted) DO NOTHING;
            """, (
                row['job_title'],
                row['company'],
                row['location'],
                row['date_posted'],
                row['freshness'],
                row['age_category']
            ))

        conn.commit()
        print("✅ Data inserted successfully.")

    except Exception as e:
        print(f"❌ Error while inserting data into PostgreSQL: {e}")

    finally:
        cursor.close()
        conn.close()

