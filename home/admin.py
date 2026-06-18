from django.contrib import admin
from .models import Department, Doctor, ContactInquiry, AppointmentBooking  # 🆕 Added AppointmentBooking model

admin.site.register(Department)
admin.site.register(Doctor)

@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "subject", "created_at")
    search_fields = ("name", "email", "subject")
    list_filter = ("subject", "created_at")
    ordering = ("-created_at",)

# 🆕 Admin configuration for Patient Bookings
@admin.register(AppointmentBooking)
class AppointmentBookingAdmin(admin.ModelAdmin):
    # Displays crucial appointment facts clearly to staff workers
    list_display = ("patient_name", "doctor_name", "department", "appointment_date", "time_slot", "created_at")
    
    # Allows receptionist staff to look up a booking by patient name or doctor instantly
    search_fields = ("patient_name", "patient_email", "doctor_name")
    
    # Enables easy right-sidebar filtering by scheduled date or medical department
    list_filter = ("appointment_date", "department")
    
    # Sorts the lists to show the absolute newest bookings at the top of the portal
    ordering = ("-created_at",)
