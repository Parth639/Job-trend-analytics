from sqlalchemy import create_engine
from urllib.parse import quote_plus
import pandas as pd

def fetch_jobs_from_db():
    # Connection string — replace your credentials
    
    #db_url = "postgresql+psycopg2://postgres:parth123@localhost:5432/job_data"
    db_url = "postgresql://postgres.dcncknstzdtdvrbmjzzo:9gcybtcn203@aws-0-ap-south-1.pooler.supabase.com:5432/postgres"
    engine = create_engine(db_url)

    query = "SELECT job_title, company, location, date_posted, freshness, age_category FROM jobs ;"
    df = pd.read_sql(query, engine)

    return df
