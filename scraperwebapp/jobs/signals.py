from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Keyword
from scraper.jobs_scraper import get_jobs, insert_jobs_to_db

@receiver(post_save, sender=Keyword)
def keyword_saved(sender, instance, created, **kwargs):
    if created:
        print(f"Keyword '{instance.keyword}' for user '{instance.user}' has been saved.")
        jobs = get_jobs(instance.keyword, num_jobs=20, verbose=True)
        insert_jobs_to_db(jobs)

