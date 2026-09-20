import requests
import os


RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

def search_jobs(keyword, location="Pakistan"):

    url = "https://jsearch.p.rapidapi.com/search-v2"

    querystring = {
        "query": f"{keyword} in {location}",
        "page": "1",
        "num_pages": "1",
        "country": "pk"
    }

    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }

    response = requests.get(
        url,
        headers=headers,
        params=querystring
    )

  
    print("STATUS:", response.status_code)
    print("RESPONSE:", response.text)

    response.raise_for_status()

    return response.json()


if __name__ == "__main__":

    data = search_jobs("web developer", "Pakistan")

    jobs = data.get("data", {}).get("jobs", [])

    print("Total jobs:", len(jobs))

    for job in jobs:

        print("Title:", job.get("job_title"))
        print("Company:", job.get("employer_name"))
        print("Location:", job.get("job_city"))
        print("Country:", job.get("job_country"))
        print("URL:", job.get("job_apply_link"))

        print("-" * 50)