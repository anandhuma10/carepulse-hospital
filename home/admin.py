from django.contrib import admin
from .models import Department, Doctor, ContactInquiry

admin.site.register(Department)
admin.site.register(Doctor)

@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "subject", "created_at")
    search_fields = ("name", "email", "subject")
    list_filter = ("subject", "created_at")
    ordering = ("-created_at",)