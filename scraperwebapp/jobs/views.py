from django.shortcuts import render

from rest_framework import generics
from .models import JobListing, Keyword
from .serializers import JobListingSerializer, KeywordSerializer
from rest_framework.permissions import IsAuthenticated

class UserKeywordsView(generics.ListAPIView):
    serializer_class = KeywordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Keyword.objects.filter(user=user)

class JobListingsByKeywordView(generics.ListAPIView):
    serializer_class = JobListingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        keyword = self.kwargs['keyword']
        return JobListing.objects.filter(job_title__icontains=keyword)
