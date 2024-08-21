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
    list_display = ('keyword', 'user', 'scheduled_on')
    search_fields = ('keyword', 'user__username')
    raw_id_fields = ('job_listings',)

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return ['user', 'job_listings']
        return []

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if obj:
            fields = ['keyword', 'scheduled_on']
        return fields

    def save_model(self, request, obj, form, change):
        if not change:  # If creating a new object
            obj.user = request.user  # Automatically set the current user
        super().save_model(request, obj, form, change)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not obj:
            form.base_fields['user'].initial = request.user
        return form
