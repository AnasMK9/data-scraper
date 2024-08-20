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
    raw_id_fields = ('user', 'job_listings')


# class KeywordInline(admin.TabularInline):
#     model = Keyword
#     extra = 1


# class UserAdmin(admin.ModelAdmin):
#     inlines = [KeywordInline]


# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)