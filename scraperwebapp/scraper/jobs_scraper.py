import urllib.parse
import urllib.request
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
from selenium.webdriver.chrome.options import Options
import urllib
from jobs.models import JobListing, Keyword


def get_jobs(keyword, num_jobs=20, verbose=True):
    '''Gathers jobs as a dataframe, scraped from Glassdoor'''

    # Initializing the webdriver
    chrome_driver_path = "/usr/bin/chromedriver"
    chrome_service = Service(executable_path=chrome_driver_path)
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

    driver.set_window_size(1920, 1080)

    print(keyword)
    url = f'https://www.glassdoor.com/Job/jobs.htm?={urllib.parse.urlencode({"sc.keyword":keyword})}&sc.locationSeoString=Riyadh+%28Saudi+Arabia%29&locId=3110290&locT=C'
    print(url)
    driver.get(url)
    jobs = []

    while len(jobs) < num_jobs:
        time.sleep(3)  # Wait for the page to load

        # Try different strategies to locate job cards
        job_cards = driver.find_elements(By.XPATH, "//div[contains(@class, 'jobCard') or contains(@class, 'JobCard')]")

        for card in job_cards:
            try:
                # Job title
                job_title = card.find_element(By.XPATH, ".//a[contains(@class, 'jobTitle') or contains(@class, 'JobCard_jobTitle')]").text

                # Company name
                try:
                    company_name = card.find_element(By.XPATH, ".//div[contains(@class, 'Employer') or contains(@class, 'company')]").text
                except NoSuchElementException:
                    company_name = "Unknown"

                # Location
                try:
                    location = card.find_element(By.XPATH, ".//div[contains(@class, 'location') or contains(@class, 'JobCard_location')]").text
                except NoSuchElementException:
                    location = "Unknown"

                # Job description snippet
                try:
                    job_description = card.find_element(By.XPATH, ".//div[contains(@class, 'jobDescriptionSnippet') or contains(@class, 'JobCard_jobDescriptionSnippet')]").text
                except NoSuchElementException:
                    job_description = "No description available"

                # Date posted (listing age)
                try:
                    listing_age = card.find_element(By.XPATH, ".//div[contains(@class, 'listingAge') or contains(@class, 'JobCard_listingAge')]").text
                except NoSuchElementException:
                    listing_age = "Not specified"

                # Easy apply (if present)
                try:
                    easy_apply = card.find_element(By.XPATH, ".//span[contains(@class, 'easyApply') or contains(@class, 'JobCard_easyApply')]").text
                except NoSuchElementException:
                    easy_apply = "No"

                jobs.append({
                    "title": job_title,
                    "company": company_name,
                    "location": location,
                    "description": job_description,
                    "age": listing_age,
                    "easy_apply": easy_apply
                })

                if len(jobs) >= num_jobs:
                    break

            except NoSuchElementException as e:
                print(f"Element not found: {e}")
                continue

        try:
            # Click on the "Next" button to load more jobs
            next_button = driver.find_element(By.XPATH, "//button[contains(@class, 'PaginationFooter_nextButton') or contains(@class, 'nextButton')]")
            driver.execute_script("arguments[0].click();", next_button)
        except NoSuchElementException:
            print("No more pages available.")
            break

    driver.quit()

    
    df = pd.DataFrame(jobs)

    return df

def insert_jobs_to_db(jobs):
    # Insert each job into the Django model
    for job in jobs:
        JobListing.objects.get_or_create(
            job_title=job["job_title"],
            salary_estimate=job["salary_estimate"],
            job_description=job["job_description"],
            rating=job["rating"],
            company_name=job["company_name"],
            location=job["location"]
        )

