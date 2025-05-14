

# API credentials
#app_id = "30bfac43"
#app_key = "f33f13d8719600112c6b0f25f967b612"
import requests
import pandas as pd
from datetime import timedelta

# API creds


def fetch_jobs():
    app_id = "30bfac43"
    app_key = "f33f13d8719600112c6b0f25f967b612"
    

# API URL + params
    api_url = "https://api.adzuna.com/v1/api/jobs/in/search/1"
    params = {
        "app_id": app_id,
        "app_key": app_key,
        "results_per_page": 60,
        "content-type": "application/json",
    }

    # Fetch response
    response = requests.get(api_url, params=params)
    data = response.json()

    if "results" in data:
        jobs = data["results"]
        
        # Extract selected fields
        job_data = []
        for job in jobs:
            job_data.append({
                "job_title": job.get("title", "N/A"),
                "company": job.get("company", {}).get("display_name", "N/A"),
                "location": job.get("location", {}).get("display_name", "N/A"),
                "date_posted": job.get("created")
            })

        # DataFrame
        jobs_df = pd.DataFrame(job_data)

        # Convert 'created' to datetime with UTC
        jobs_df["date_posted"] = pd.to_datetime(jobs_df["date_posted"], utc=True)

        # Current UTC time (already UTC)
        now = pd.Timestamp.utcnow()

        # Freshness in days
        jobs_df["freshness"] = (now - jobs_df["date_posted"]).dt.days

        # Categorize into 'Trending' and 'Past'
        jobs_df["age_category"] = jobs_df["freshness"].apply(
            lambda x: "Trending" if x <= 30 else "Past"
        )

        # Show results
        print(jobs_df.head(100))

    else:
        print("API issue:", data)
    
    return jobs_df

df = fetch_jobs()
#df.rename(columns={'title': 'job_title', 'region': 'location'}, inplace=True)
print(df.columns)

