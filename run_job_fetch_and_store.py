# run_job_fetch_and_store.py

# from API_Call import fetch_jobs
# from Database_connection import store_data_into_postgresql

# def main():
#     df = fetch_jobs()  # df is created here
#     if not df.empty:
#         store_data_into_postgresql(df)  # df is passed here
#     else:
#         print("No data fetched from API.")
from API_Call import fetch_jobs
from Database_connection import store_data_into_postgresql

def main():
    df = fetch_jobs()  # df is created here
    if not df.empty:
        store_data_into_postgresql(df)  # df is passed here
    else:
        print("No data fetched from API.")
if __name__ == "__main__":
    main()
