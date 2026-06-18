from django.urls import path
from . import views

urlpatterns = [
    # Main Navigation
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('department/', views.department, name='department'),
    path('doctors/', views.doctors, name='doctors'),
    path('contact/', views.contact, name='contact'),
    
    # Booking & Form Actions
    path('booking/', views.booking_view, name='booking'),
    path('success/', views.appointment_success_view, name='appointment_success'),
    
    # Department Dynamic Routing
    path('department/<int:dept_id>/doctors/', views.doctors, name='department_doctors'),
 
    # Staff / Admin Dashboard Operations
    path('staff/inquiries/', views.enquiry_dashboard, name='inquiry_dashboard'),
    path('staff/inquiries/<int:pk>/', views.enquiry_detail, name='inquiry_detail'),
    path('staff/inquiries/<int:pk>/delete/', views.delete_enquiry, name='delete_enquiry'),
    path('staff/appointments/<int:pk>/delete/', views.delete_appointment, name='delete_appointment'),

]
