from django.contrib.auth.models import User

from django.db import models

class JobListing(models.Model):
    job_title = models.CharField(max_length=255)
    salary_estimate = models.CharField(max_length=255, blank=True, null=True)
    job_description = models.TextField()
    rating = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    company_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)

    class Meta:
        indexes = [
            models.Index(fields=['job_title', 'company_name', 'location']),
        ]

    def __str__(self):
        return f"{self.job_title} at {self.company_name}"


class Keyword(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=255)
    scheduled_on = models.TimeField()
    job_listings = models.ManyToManyField('JobListing', related_name='keywords', blank=True)

    def __str__(self):
        return self.keyword
    
