import requests
from bs4 import BeautifulSoup
from app import create_app
from models import db, Jobs

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36"
}

response = requests.get("https://remoteok.com/remote-backend-jobs", headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')
jobs = soup.select("tr.job")

app = create_app()

with app.app_context():
    for job in jobs:
        try:
            job_anchor = job.select_one("a[itemprop='url']")
            title = job_anchor.select_one("h2[itemprop='title']").text.strip()
            company = job.get("data-company")
            job_url = "https://remoteok.com" + job.get("data-href")
            location = job.find("div", class_="location").text.strip()
            salary = job.find_all("div", class_="location")[1].text.strip()
            tags = [tag.text.strip() for tag in job.select("td.tags h3")]
            date_posted = job.find("time")["datetime"]

            # Check for duplicates
            job_exists = db.session.execute(
                db.select(Jobs).where(Jobs.job_url == job_url)
            ).scalar()

            if not job_exists:
                new_job = Jobs(
                    title=title,
                    company=company,
                    location=location,
                    job_url=job_url,
                    tags=", ".join(tags),
                    posted=date_posted
                )
                db.session.add(new_job)
                db.session.commit()

        except Exception as e:
            print(f"Error parsing a job: {e}")
