from django.contrib import admin
from .models import Department, Doctor, ContactInquiry, Appointment 

admin.site.register(Department)
@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "department",
        "user",
        "experience",
        "available_from",
        "available_until",
    )

    search_fields = (
        "name",
        "user__username",
        "department__name",
    )

    list_filter = (
        "department",
        "working_days",
    )

@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "subject", "created_at")
    search_fields = ("name", "email", "subject")
    list_filter = ("subject", "created_at")
    ordering = ("-created_at",)

# 🆕 Admin configuration for Patient Bookings
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        "patient",
        "doctor",
        "department",
        "appointment_date",
        "time_slot",
        "status",
        "created_at",
    )

    search_fields = (
        "patient__username",
        "doctor__name",
        "department__name",
    )

    list_filter = (
        "status",
        "appointment_date",
        "department",
    )

    ordering = ("-created_at",)