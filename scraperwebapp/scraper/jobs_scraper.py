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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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

    wait = WebDriverWait(driver, 10)  # 10 seconds wait
    while len(jobs) < num_jobs:  # If true, should be still looking for new jobs.
        try:
            driver.find_element(By.CLASS_NAME, "selected").click()
        except:
            pass

        try:
            driver.find_element(By.CLASS_NAME, "ModalStyle__xBtn___29PT9").click()  # Close the sign-up modal
        except:
            pass

        # Going through each job in this page
        job_cards = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "jobCard")))

        
        for job_card in job_cards:  
            print(f"Progress: {len(jobs)}/{num_jobs}")
            if len(jobs) >= num_jobs:
                break

            try:
                job_title = job_card.find_element(By.CLASS_NAME, "JobCard_jobTitle___7I6y").text
                company_name = job_card.find_element(By.CLASS_NAME, "EmployerProfile_compactEmployerName__LE242").text
                location = job_card.find_element(By.CLASS_NAME, "JobCard_location__rCz3x").text
                job_description = job_card.find_element(By.CLASS_NAME, "JobCard_jobDescriptionSnippet__yWW8q").text
            except Exception as e:
                print(f"Failed to collect job data: {e}")
                continue

            try:
                salary_estimate = job_card.find_element(By.CLASS_NAME, "JobCard_salaryEstimate__arV5J").text
            except NoSuchElementException:
                salary_estimate = -1

            try:
                rating = job_card.find_element(By.CLASS_NAME, "EmployerProfile_ratingContainer__ul0Ef").text
            except NoSuchElementException:
                rating = -1

            # Printing for debugging
            if verbose:
                print(f"Job Title: {job_title}")
                print(f"Salary Estimate: {salary_estimate}")
                print(f"Job Description: {job_description[:500]}")
                print(f"Rating: {rating}")
                print(f"Company Name: {company_name}")
                print(f"Location: {location}")

            jobs.append({
                "Job Title": job_title,
                "Salary Estimate": salary_estimate,
                "Job Description": job_description,
                "Rating": rating,
                "Company Name": company_name,
                "Location": location
            })

    print(f"Finished scraping {len(jobs)} jobs")

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

