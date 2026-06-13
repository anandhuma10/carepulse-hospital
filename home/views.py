from django.shortcuts import render
from django.http import HttpResponse
from .models import Department
from .models import Doctor



# Create your views here.

def department(request):
    departments = Department.objects.all()
    return render(request, 'department.html', {
        'departments': departments
    })

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def doctors(request):
    doctors_list = Doctor.objects.all()
    return render(request, 'doctors.html', {
        'doctors': doctors_list
    })

def contact(request):
    return render(request, 'contact.html')

def booking(request):
    return render(request, 'booking.html')
