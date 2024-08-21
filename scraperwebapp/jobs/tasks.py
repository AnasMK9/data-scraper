from scraperwebapp.celery import app
from scraper.jobs_scraper import get_jobs, insert_jobs_to_db

@app.task
def process_keyword(keyword, num_jobs=20):
    jobs = get_jobs(keyword, num_jobs=num_jobs, verbose=True)
    insert_jobs_to_db(jobs)
