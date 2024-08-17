from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

from jobs.models import JobListing, Keyword

def get_jobs(keyword, num_jobs, verbose):
    '''Gathers jobs as a dataframe, scraped from Glassdoor'''

    # Initializing the webdriver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  #
    options.add_argument('--no-sandbox')  
    options.add_argument('--disable-dev-shm-usage')  
    options.add_argument('--disable-gpu')  
    options.add_argument('--window-size=1920x1080')  
    options.binary_location = "/usr/bin/chromium"  

    service = Service(executable_path='/usr/bin/chromedriver')

    driver = webdriver.Chrome(service=service, options=options)
    driver.set_window_size(1920, 1080)

    url = f'https://www.glassdoor.com/Job/jobs.htm?sc.keyword="{keyword}"&sc.locationSeoString=Riyadh+%28Saudi+Arabia%29&locId=3110290&locT=C'
    driver.get(url)
    jobs = []

    while len(jobs) < num_jobs:  # If true, should be still looking for new jobs.

        time.sleep(4)  # Let the page load

        # Test for the "Sign Up" prompt and get rid of it.
        try:
            driver.find_element(By.CLASS_NAME, "selected").click()
        except:
            pass

        try:
            driver.find_element(By.CLASS_NAME, "ModalStyle__xBtn___29PT9").click()  # Close the sign-up modal
        except:
            pass

        # Going through each job in this page
        job_cards = driver.find_elements(By.CLASS_NAME, "jobCard")  # Updated to match the current HTML structure
        
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
                salary_estimate = None

            try:
                rating = job_card.find_element(By.CLASS_NAME, "EmployerProfile_ratingContainer__ul0Ef").text
            except NoSuchElementException:
                rating = None

            # Printing for debugging
            if verbose:
                print(f"Job Title: {job_title}")
                print(f"Salary Estimate: {salary_estimate}")
                print(f"Job Description: {job_description[:500]}")
                print(f"Rating: {rating}")
                print(f"Company Name: {company_name}")
                print(f"Location: {location}")

            jobs.append({
                "job_title": job_title,
                "salary_estimate": salary_estimate,
                "job_description": job_description,
                "rating": rating,
                "company_name": company_name,
                "location": location
            })

        # Clicking on the "next page" button
        try:
            driver.find_element(By.XPATH, './/li[@class="next"]//a').click()
        except NoSuchElementException:
            print(f"Scraping terminated before reaching target number of jobs. Needed {num_jobs}, got {len(jobs)}.")
            break

    driver.quit()
    return jobs

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

