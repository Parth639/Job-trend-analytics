import streamlit as st
st.set_page_config(page_title="Job Market Analytics", layout="wide")
import pandas as pd
import sqlalchemy
import plotly.express as px
import plotly.graph_objects as go
from run_job_fetch_and_store import main
from db_connection import fetch_jobs_from_db

jobs_df = fetch_jobs_from_db()
# DB connection
db_uri = "postgresql://postgres.dcncknstzdtdvrbmjzzo:9gcybtcn203@aws-0-ap-south-1.pooler.supabase.com:5432/postgres"
engine = sqlalchemy.create_engine(db_uri)

# Load data from PostgreSQL
@st.cache_data(ttl=60)
def load_data():
    query = "SELECT * FROM jobs"
    df = pd.read_sql(query, engine)
    return df

df = load_data()

# Page Config

st.title("📊 Real Time Job Market Analytics")

# Sidebar Filters
st.sidebar.header("🔍 Filters")
freshness_filter = st.sidebar.slider("Freshness (in days)", 0, 30, 100)
companies = st.sidebar.multiselect("Select Companies", options=df["company"].unique())
locations = st.sidebar.multiselect("Select Locations", options=df["location"].unique())
keyword = st.sidebar.text_input("Search by Job Title Keyword")


# Apply filters
filtered_df = df[df["freshness"] <= freshness_filter]
if companies:
    filtered_df = filtered_df[filtered_df["company"].isin(companies)]
if locations:
    filtered_df = filtered_df[filtered_df["location"].isin(locations)]
if keyword:
    filtered_df = filtered_df[filtered_df["job_title"].str.contains(keyword)]

# KPIs
total_jobs = len(filtered_df)
trending_jobs = len(filtered_df[filtered_df["age_category"] == "Trending"])
past_jobs = len(filtered_df[filtered_df["age_category"] == "Past"])
top_company = filtered_df["company"].mode()[0] if not filtered_df.empty else "N/A"
top_location = filtered_df["location"].mode()[0] if not filtered_df.empty else "N/A"

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("📋 Total Jobs", total_jobs)
col2.metric("🔥 Trending Jobs", trending_jobs)
col3.metric("⏳ Past Jobs", past_jobs)
col4.metric("🏢 Top Company", top_company)
col5.metric("📍 Top Location", top_location)

st.markdown("---")

# Job Category Pie Chart
# Categorizing job titles
filtered_df["category"] = filtered_df["job_title"].apply(
    lambda x: "Data" if "Data" in x else ("AI" if "AI" in x else "Other")
)

# Counting job categories
category_dist = filtered_df["category"].value_counts().reset_index()
category_dist.columns = ['category', 'count']

# Pie chart
fig_pie = px.pie(category_dist, names="category", values="count", title="Job Category Distribution")
st.plotly_chart(fig_pie, use_container_width=True)

# Top Companies Bar Chart
company_counts = filtered_df["company"].value_counts().head(10).reset_index()
company_counts.columns = ['company', 'count'] 
fig_bar = px.bar(company_counts, x="index", y="company",
                 labels={"index": "Company", "company": "Number of Jobs"},
                 title="Top Hiring Companies")
st.plotly_chart(fig_bar, use_container_width=True)

# Freshness Trendline
trend_df = filtered_df.groupby(filtered_df["date_posted"].dt.date).size().reset_index(name="job_count")
fig_line = px.line(trend_df, x="date_posted", y="job_count", title="Jobs Posted Over Time")
st.plotly_chart(fig_line, use_container_width=True)

# Job Listings Table
st.subheader("📑 Job Listings")
st.dataframe(filtered_df)

# Refresh button
if st.button("🔄 Fetch Latest Data"):
    main()
    st.success("✅ Data updated successfully!")
    st.rerun()

st.markdown("---")
st.markdown("✅ Built with ❤️ by Parth Shah | Powered by Adzuna API, PostgreSQL, Streamlit")

