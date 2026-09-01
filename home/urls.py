from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import patient_portal_view


router = DefaultRouter()
router.register('api/departments', views.DepartmentViewSet, basename='department')
router.register('api/doctors', views.DoctorViewSet, basename='doctor')
router.register('api/appointments',views.AppointmentViewSet,basename='appointment')  # 🆕 Added AppointmentViewSet for API routing


urlpatterns = [
    # Main Navigation
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('department/', views.department, name='department'),
    path('doctors/', views.doctors, name='doctors'),
    path('contact/', views.contact, name='contact'),

    # Booking
    path('booking/', views.booking_view, name='booking'),
    path('success/', views.appointment_success_view, name='appointment_success'),
    path('staff/appointments/<int:pk>/confirm/',
    views.confirm_appointment,
    name='confirm_appointment'),
    path(
    'staff/appointments/<int:pk>/cancel/',
    views.cancel_appointment,
    name='cancel_appointment'),

    # Patient Portal
    path('portal/', patient_portal_view, name='patient_portal'),

    # Department Dynamic Routing
    path(
        'department/<int:dept_id>/doctors/',
        views.doctors,
        name='department_doctors'
    ),

    # Staff / Admin Dashboard
    path(
        'staff/inquiries/',
        views.enquiry_dashboard,
        name='inquiry_dashboard'
    ),
    path(
        'staff/inquiries/<int:pk>/',
        views.enquiry_detail,
        name='inquiry_detail'
    ),
    path(
        'staff/inquiries/<int:pk>/delete/',
        views.delete_enquiry,
        name='delete_enquiry'
    ),
    path(
        'staff/appointments/<int:pk>/delete/',
        views.delete_appointment,
        name='delete_appointment'
    ),

    # Available appointment slots
    path(
        'api/appointments/available-slots/',
        views.available_slots,
        name='available_slots',
    ),

    # DRF API
    path('', include(router.urls)),

    # AI
    path(
        'ai-doctor/',
        views.ai_doctor_page,
        name='ai-doctor-page'
    ),
    path(
        'api/ai/recommend-doctor/',
        views.ai_doctor_recommendation,
        name='ai-doctor-recommendation'
    ),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("staff/login/", views.staff_login_view, name="staff_login"),
    path("doctor/login/", views.doctor_login_view, name="doctor_login"),
    path(
    "doctor/portal/",
    views.doctor_portal_view,
    name="doctor_portal",
),
]