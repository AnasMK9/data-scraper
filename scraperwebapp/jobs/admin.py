from django.contrib import admin
from .models import JobListing, Keyword
from django.contrib.auth.models import User

@admin.register(JobListing)
class JobListingAdmin(admin.ModelAdmin):
    list_display = ('job_title', 'company_name', 'location', 'rating')
    search_fields = ('job_title', 'company_name', 'location')
    raw_id_fields = ('keywords',)

@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    list_display = ('keyword', 'scheduled_on')
    search_fields = ('keyword', 'job_listings__title')
    raw_id_fields = ('job_listings',)

    def get_readonly_fields(self, request, obj=None):
        # Make 'job_listings' readonly when editing an existing object
        if obj:  
            return ['user', 'job_listings']
        return ['user']

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if obj:
            # Customize fields for the object detail view
            fields = ['keyword', 'scheduled_on', 'job_listings']
        return fields

    def save_model(self, request, obj, form, change):
        if not change:  # If creating a new object
            obj.user = request.user  # Automatically set the current user
        super().save_model(request, obj, form, change)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

      
        return form

    def get_queryset(self, request):
        # Customize the queryset to filter by the current user if needed
        qs = super().get_queryset(request)
        return qs.filter(user=request.user)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "job_listings":
            kwargs["queryset"] = JobListing.objects.filter(keywords__user=request.user)
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def job_listings(self, obj):
        # Custom method to display related job listings in the details view
        return ", ".join([listing.title for listing in obj.job_listings.all()])

    job_listings.short_description = 'Related Job Listings'
