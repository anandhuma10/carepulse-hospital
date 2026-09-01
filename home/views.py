from datetime import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST

from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import PatientRegistrationForm
from django.views.decorators.http import require_POST
from .ai_service import get_recommended_doctors
from .models import (
    Department,
    Doctor,
    ContactInquiry,
    Appointment,
    PatientProfile,
)
from .permissions import (
    AppointmentPermission,
    DepartmentPermission,
    DoctorPermission,
)
from .serializers import (
    DepartmentSerializer,
    DoctorSerializer,
    AppointmentSerializer,
    AIRecommendationSerializer,
)

# Create your views here.

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def department(request):
    # Clean & simple: Just show all departments on this page
    departments = Department.objects.all()
    return render(request, 'department.html', {
        'departments': departments
    })

def doctors(request, dept_id=None):
    if dept_id:
        # If clicked from a specific department card, filter the list
        active_department = get_object_or_404(Department, id=dept_id)
        doctors_list = Doctor.objects.filter(department=active_department)
        banner_title = f"Specialists in {active_department.name}"
    else:
        # If clicked from the top main navbar link, show everyone
        doctors_list = Doctor.objects.all()
        banner_title = "Meet Our Specialists"

    return render(request, 'doctors.html', {
        'doctors': doctors_list,
        'banner_title': banner_title
    })

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message_body = request.POST.get('message')

        ContactInquiry.objects.create(
            name=name,
            email=email,
            phone=phone,
            subject=subject,
            message=message_body
        )

        messages.success(
            request,
            f"Thank you, {name}! Your inquiry about '{subject}' has been submitted."
        )

        return redirect('contact')

    return render(request, 'contact.html')

@staff_member_required
def enquiry_dashboard(request):
    inquiries = ContactInquiry.objects.all().order_by('-created_at')

    appointments = Appointment.objects.all().select_related(
        'patient',
        'doctor',
        'department',
    ).order_by('-created_at')

    context = {
        'inquiries': inquiries,
        'appointments': appointments,
    }

    return render(request, 'dashboard/inquiry_list.html', context)


@staff_member_required
def enquiry_detail(request, pk):
    # 1. FIXED: Changed ContactEnquiry to ContactInquiry
    inquiry = get_object_or_404(ContactInquiry, pk=pk)
    
    # 2. FIXED: Changed template key to 'inquiry' to match your HTML template fields
    return render(request, 'dashboard/inquiry_detail.html', {'inquiry': inquiry})


@staff_member_required
@require_POST  # Security check: ensures this can only be triggered via a button form submission
def delete_enquiry(request, pk):
    inquiry = get_object_or_404(ContactInquiry, pk=pk)
    inquiry.delete()
    messages.success(request, "The inquiry has been successfully removed.")
    return redirect('inquiry_dashboard')


@login_required
def booking_view(request):
    departments = Department.objects.all().order_by("name")

    doctors_data = list(
        Doctor.objects.all().values(
            "id",
            "name",
            "department_id",
            "working_days",
            "available_from",
            "available_until",
        )
    )

    profile, _ = PatientProfile.objects.get_or_create(
        user=request.user
    )

    context = {
        "departments": departments,
        "doctors_data": doctors_data,
        "profile": profile,
    }

    if request.method == "POST":
        department_id = request.POST.get("department")
        doctor_id = request.POST.get("doctor")
        appointment_date = request.POST.get("appointment_date")
        time_slot = request.POST.get("time_slot")
        phone = request.POST.get("phone", "").strip()
        dob = request.POST.get("dob", "").strip()
        symptoms = request.POST.get("symptoms", "").strip()

        # -----------------------------
        # Required fields
        # -----------------------------
        if not all([
            department_id,
            doctor_id,
            appointment_date,
            time_slot,
            phone,
            dob,
            symptoms,
        ]):
            messages.error(
                request,
                "Please complete all required appointment and patient details."
            )
            return render(
                request,
                "booking_form.html",
                context,
            )

        # -----------------------------
        # Department
        # -----------------------------
        try:
            department = Department.objects.get(pk=department_id)
        except Department.DoesNotExist:
            messages.error(
                request,
                "Selected department does not exist."
            )
            return render(
                request,
                "booking_form.html",
                context,
            )

        # -----------------------------
        # Doctor
        # -----------------------------
        try:
            doctor = Doctor.objects.select_related("department").get(
                pk=doctor_id
            )
        except Doctor.DoesNotExist:
            messages.error(
                request,
                "Selected doctor does not exist."
            )
            return render(
                request,
                "booking_form.html",
                context,
            )

        # -----------------------------
        # Doctor belongs to department
        # -----------------------------
        if doctor.department_id != department.id:
            messages.error(
                request,
                "The selected doctor does not belong to the selected department."
            )
            return render(
                request,
                "booking_form.html",
                context,
            )

        # -----------------------------
        # Parse date, time and DOB
        # -----------------------------
        try:
            appointment_date_obj = datetime.strptime(
                appointment_date,
                "%Y-%m-%d",
            ).date()

            time_slot_obj = datetime.strptime(
                time_slot,
                "%H:%M",
            ).time()

            dob_obj = datetime.strptime(
                dob,
                "%Y-%m-%d",
            ).date()

        except ValueError:
            messages.error(
                request,
                "Please enter a valid date, date of birth, and appointment time."
            )
            return render(
                request,
                "booking_form.html",
                context,
            )

        # -----------------------------
        # 30-minute slot validation
        # -----------------------------
        if time_slot_obj.minute not in (0, 30):
            messages.error(
                request,
                "Please select a valid 30-minute appointment slot."
            )
            return render(
                request,
                "booking_form.html",
                context,
            )

        # -----------------------------
        # Prevent past appointment dates
        # -----------------------------
        from django.utils import timezone

        today = timezone.localdate()

        if appointment_date_obj < today:
            messages.error(
                request,
                "Appointment date cannot be in the past."
            )
            return render(
                request,
                "booking_form.html",
                context,
            )

        # -----------------------------
        # Doctor working day
        # -----------------------------
        appointment_day = appointment_date_obj.strftime("%A")

        working_days = [
            day.strip()
            for day in doctor.working_days.split(",")
            if day.strip()
        ]

        if appointment_day not in working_days:
            messages.error(
                request,
                f"Dr. {doctor.name} is not available on {appointment_day}."
            )
            return render(
                request,
                "booking_form.html",
                context,
            )

        # -----------------------------
        # Doctor working hours
        # -----------------------------
        if not (
            doctor.available_from
            <= time_slot_obj
            < doctor.available_until
        ):
            messages.error(
                request,
                f"Dr. {doctor.name} is available between "
                f"{doctor.available_from.strftime('%I:%M %p')} and "
                f"{doctor.available_until.strftime('%I:%M %p')}."
            )
            return render(
                request,
                "booking_form.html",
                context,
            )

        # -----------------------------
        # Save/update patient profile
        # -----------------------------
        profile.phone = phone
        profile.date_of_birth = dob_obj
        profile.save()

        # -----------------------------
        # Create appointment
        # -----------------------------
        try:
            appointment = Appointment.objects.create(
                patient=request.user,
                doctor=doctor,
                department=department,
                appointment_date=appointment_date_obj,
                time_slot=time_slot_obj,
                symptoms=symptoms,
                status="pending",
            )

        except IntegrityError:
            messages.error(
                request,
                "This doctor is already booked for that date and time. "
                "Please select another time slot."
            )
            return render(
                request,
                "booking_form.html",
                context,
            )

        # -----------------------------
        # Confirmation email
        # -----------------------------
        patient_name = (
            request.user.get_full_name()
            or request.user.username
        )

        patient_email = request.user.email

        subject = (
            f"Appointment Booked Successfully - {patient_name}"
        )

        message = (
            f"Dear {patient_name},\n\n"
            f"Your CarePulse appointment has been booked successfully.\n\n"
            f"=== APPOINTMENT DETAILS ===\n"
            f"Appointment ID: {appointment.id}\n"
            f"Department: {department.name}\n"
            f"Doctor: Dr. {doctor.name}\n"
            f"Date: {appointment.appointment_date.strftime('%d %B %Y')}\n"
            f"Time: {appointment.time_slot.strftime('%I:%M %p')}\n"
            f"Status: {appointment.get_status_display()}\n\n"
            f"Warm regards,\n"
            f"CarePulse Hospital Operations Team"
        )

        if patient_email:
            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [patient_email],
                    fail_silently=False,
                )
            except Exception as e:
                print(f"Brevo SMTP Execution Error: {e}")

        return redirect("appointment_success")

    return render(
        request,
        "booking_form.html",
        context,
    )

@login_required
def available_slots(request):
    doctor_id = request.GET.get("doctor")
    appointment_date = request.GET.get("date")

    if not doctor_id or not appointment_date:
        return JsonResponse(
            {"available_slots": []},
            status=400,
        )

    # Get doctor
    try:
        doctor = Doctor.objects.get(pk=doctor_id)
    except Doctor.DoesNotExist:
        return JsonResponse(
            {"available_slots": []},
            status=404,
        )

    # Parse date
    try:
        appointment_date_obj = datetime.strptime(
            appointment_date,
            "%Y-%m-%d",
        ).date()
    except ValueError:
        return JsonResponse(
            {"available_slots": []},
            status=400,
        )

    # Prevent past dates
    today = timezone.localdate()

    if appointment_date_obj < today:
        return JsonResponse({
            "available_slots": []
        })

    # Check doctor's working day
    appointment_day = appointment_date_obj.strftime("%A")

    working_days = [
        day.strip()
        for day in doctor.working_days.split(",")
        if day.strip()
    ]

    if appointment_day not in working_days:
        return JsonResponse({
            "available_slots": []
        })

    # Get booked slots
    booked_slots = Appointment.objects.filter(
        doctor=doctor,
        appointment_date=appointment_date_obj,
        status__in=["pending", "confirmed"],
    ).values_list(
        "time_slot",
        flat=True,
    )

    booked_slots = {
        slot.strftime("%H:%M")
        for slot in booked_slots
    }

    # Generate 30-minute slots
    from datetime import timedelta

    current_datetime = datetime.combine(
        appointment_date_obj,
        doctor.available_from,
    )

    end_datetime = datetime.combine(
        appointment_date_obj,
        doctor.available_until,
    )

    available_slots = []

    while current_datetime < end_datetime:

        current_time = current_datetime.time()

        # If booking today, hide slots that have already passed
        if appointment_date_obj == today:
            current_time_now = timezone.localtime().time()

            if current_time <= current_time_now:
                current_datetime += timedelta(minutes=30)
                continue

        slot_value = current_time.strftime("%H:%M")

        if slot_value not in booked_slots:
            available_slots.append(slot_value)

        current_datetime += timedelta(minutes=30)

    return JsonResponse({
        "available_slots": available_slots
    })

def appointment_success_view(request):
    # CRITICAL FIX: Ensure this renders your full HTML template file
    return render(request, 'appointment_success.html')

@staff_member_required
@require_POST
def delete_appointment(request, pk):
    get_object_or_404(Appointment, pk=pk).delete()
    messages.success(request, "Appointment successfully removed.")
    return redirect('inquiry_dashboard')




class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [DepartmentPermission]

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [DoctorPermission]

class AppointmentViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    permission_classes = [AppointmentPermission]

    def get_queryset(self):
        user = self.request.user

        # Admin and Reception can see all appointments
        if user.is_superuser or user.groups.filter(name="Reception").exists():
            return Appointment.objects.all()

        # Patients can see only their own appointments
        return Appointment.objects.filter(patient=user)

    def perform_create(self, serializer):
        serializer.save(patient=self.request.user)

def ai_doctor_page(request):
    return render(request, 'ai_doctor.html')

@api_view(["POST"])
def ai_doctor_recommendation(request):

    print("AI REQUEST DATA:", request.data)

    serializer = AIRecommendationSerializer(
        data=request.data
    )

    serializer.is_valid(raise_exception=True)

    print("VALIDATED DATA:", serializer.validated_data)

    symptom = serializer.validated_data["symptom"]
    body_area = serializer.validated_data["body_area"]

    result = get_recommended_doctors(
        symptom,
        body_area
    )

    doctors = [
        {
            "id": doctor.id,
            "name": doctor.name,
        }
        for doctor in result["doctors"]
    ]

    return Response({
        "department": result["department"],
        "reason": result["reason"],
        "doctors": doctors,
    })


@login_required
def patient_portal_view(request):
    profile, created = PatientProfile.objects.get_or_create(user=request.user)

    appointments = Appointment.objects.filter(patient=request.user).order_by('-appointment_date','-time_slot')

    context = {
    'profile': profile,
    'appointments': appointments,
    }

    return render(request,'patient_portal.html',context)

def register_view(request):
    if request.method == "POST":
        form = PatientRegistrationForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Account created successfully. Please log in."
            )

            return redirect("login")

    else:
        form = PatientRegistrationForm()

    return render(
        request,
        "register.html",
        {"form": form},
    )


def login_view(request):
    if request.user.is_authenticated:
        return redirect("patient_portal")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user is not None:
            login(request, user)

            next_url = request.GET.get("next")

            if next_url:
                return redirect(next_url)

            return redirect("patient_portal")

        messages.error(
            request,
            "Invalid username or password."
        )

    return render(request, "login.html")


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("login")

@staff_member_required
@require_POST
def confirm_appointment(request, pk):
    appointment = get_object_or_404(
        Appointment.objects.select_related(
            "patient",
            "doctor",
            "department",
        ),
        pk=pk,
    )

    if appointment.status != "pending":
        messages.error(
            request,
            "Only pending appointments can be confirmed."
        )
        return redirect("inquiry_dashboard")

    appointment.status = "confirmed"
    appointment.save(update_fields=["status"])

    patient = appointment.patient
    patient_email = patient.email

    if patient_email:
        patient_name = (
            patient.get_full_name()
            or patient.username
        )

        subject = "Appointment Confirmed - CarePulse Hospital"

        message = (
            f"Dear {patient_name},\n\n"
            f"Your CarePulse appointment has been confirmed.\n\n"
            f"=== APPOINTMENT DETAILS ===\n"
            f"Appointment ID: {appointment.id}\n"
            f"Department: {appointment.department.name}\n"
            f"Doctor: Dr. {appointment.doctor.name}\n"
            f"Date: {appointment.appointment_date.strftime('%d %B %Y')}\n"
            f"Time: {appointment.time_slot.strftime('%I:%M %p')}\n"
            f"Status: Confirmed\n\n"
            f"Please arrive on time for your appointment.\n\n"
            f"Warm regards,\n"
            f"CarePulse Hospital Operations Team"
        )

        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [patient_email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Confirmation email error: {e}")

    messages.success(
        request,
        "Appointment confirmed successfully."
    )

    return redirect("inquiry_dashboard")


@staff_member_required
@require_POST
def cancel_appointment(request, pk):
    appointment = get_object_or_404(
        Appointment.objects.select_related(
            "patient",
            "doctor",
            "department",
        ),
        pk=pk,
    )

    if appointment.status != "pending":
        messages.error(
            request,
            "Only pending appointments can be cancelled."
        )
        return redirect("inquiry_dashboard")

    appointment.status = "cancelled"
    appointment.save(update_fields=["status"])

    patient = appointment.patient
    patient_email = patient.email

    if patient_email:
        patient_name = (
            patient.get_full_name()
            or patient.username
        )

        subject = "Appointment Cancelled - CarePulse Hospital"

        message = (
            f"Dear {patient_name},\n\n"
            f"Your CarePulse appointment has been cancelled.\n\n"
            f"=== APPOINTMENT DETAILS ===\n"
            f"Appointment ID: {appointment.id}\n"
            f"Department: {appointment.department.name}\n"
            f"Doctor: Dr. {appointment.doctor.name}\n"
            f"Date: {appointment.appointment_date.strftime('%d %B %Y')}\n"
            f"Time: {appointment.time_slot.strftime('%I:%M %p')}\n"
            f"Status: Cancelled\n\n"
            f"Please contact CarePulse Hospital if you need assistance.\n\n"
            f"Warm regards,\n"
            f"CarePulse Hospital Operations Team"
        )

        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [patient_email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Cancellation email error: {e}")

    messages.success(
        request,
        "Appointment cancelled successfully."
    )

    return redirect("inquiry_dashboard")