from django.urls import path
from .views import UserKeywordsView, JobListingsByKeywordView

urlpatterns = [
    path('user/keywords/', UserKeywordsView.as_view(), name='user-keywords'),
    path('jobs/<str:keyword>/', JobListingsByKeywordView.as_view(), name='job-listings-by-keyword'),
]
