import requests
from bs4 import BeautifulSoup
import csv


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36"
}

response = requests.get("https://remoteok.com/remote-backend-jobs",headers=headers)

web_page = response.text

soup = BeautifulSoup(web_page,'html.parser')

#print(soup.prettify())


jobs = soup.select("tr.job")

with open("remote_jobs.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "Company", "Job URL", "Location", "Salary", "Tags", "Date Posted"])


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
    except Exception as e:
        print(f"Error parsing a job: {e}")
    with open("remote_jobs.csv", mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            title,
            company,
            job_url,
            location,
            salary,
            ", ".join(tags),
            date_posted
        ])
