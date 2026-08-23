from rest_framework import viewsets
from .permissions import AppointmentPermission, DepartmentPermission,DoctorPermission
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import DepartmentSerializer,DoctorSerializer,AppointmentSerializer
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from .models import Department, Doctor, ContactInquiry, AppointmentBooking, Appointment # 🆕 Ensure this is included
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings # <-- CRITICAL FIX: Missing settings import added
from django.views.decorators.http import require_POST
from rest_framework.permissions import IsAuthenticated
from .ai_service import get_recommended_doctors
from .serializers import AIRecommendationSerializer

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
    # Fetch data records from both tables
    inquiries = ContactInquiry.objects.all().order_by('-created_at')
    appointments = AppointmentBooking.objects.all().order_by('-created_at') # 🆕 Fetch appointments
    
    context = {
        'inquiries': inquiries,
        'appointments': appointments, # 🆕 Send to dashboard template context
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


def booking_view(request):
    if request.method == 'POST':
        patient_name = request.POST.get('patient_name', 'Patient')
        patient_email = request.POST.get('email')
        appointment_date = request.POST.get('appointment_date', 'Upcoming Date')
        time_slot = request.POST.get('time_slot', 'Selected Slot')
        department = request.POST.get('department', 'General Medicine')
        doctor_name = request.POST.get('doctor', 'Any Available Doctor')
        
        # 💾 🆕 SAVE TO DATABASE SO STAFF CAN SEE IT
        AppointmentBooking.objects.create(
            patient_name=patient_name,
            patient_email=patient_email,
            # 🚀 FIXED: Added the missing comma right after this function call line
            patient_phone=request.POST.get('phone', ''),
            appointment_date=appointment_date,
            time_slot=time_slot,
            department=department,
            doctor_name=doctor_name
        )
        
        # === Email generation logic remains completely untouched here ===
        subject = f'Appointment Booked Successfully - {patient_name}'
        message = (
            f"Dear {patient_name},\n\n"
            f"Thank you for scheduling your visit with CarePulse Hospital.\n\n"
            f"=== APPOINTMENT DETAILS ===\n"
            f"📍 Department: {department}\n"
            f"👨‍⚕️ Specialist: {doctor_name}\n"
            f"📅 Date: {appointment_date}\n"
            f"⏰ Preferred Slot: {time_slot}\n\n"
            f"Warm regards,\n"
            f"CarePulse Hospital Operations Team"
        )
        
        if patient_email:
            try:
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [patient_email], fail_silently=False)
            except Exception as e:
                print(f"Brevo SMTP Execution Error: {e}")
        
        return redirect('appointment_success')

    return render(request, 'booking_form.html')


def appointment_success_view(request):
    # CRITICAL FIX: Ensure this renders your full HTML template file
    return render(request, 'appointment_success.html')

@staff_member_required
@require_POST
def delete_appointment(request, pk):
    get_object_or_404(AppointmentBooking, pk=pk).delete()
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

@api_view(["POST"])
def ai_doctor_recommendation(request):

    serializer = AIRecommendationSerializer(
        data=request.data
    )

    serializer.is_valid(raise_exception=True)

    symptom = serializer.validated_data["symptom"]

    result = get_recommended_doctors(symptom)

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