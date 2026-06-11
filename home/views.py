from django.shortcuts import render
from django.http import HttpResponse
from .models import Department

def department_list(request):
    departments = Department.objects.all()
    # ⚠️ Double check that 'department.html' matches your exact file name
    return render(request, 'department.html', {'departments': departments})

# Create your views here.

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def department(request):
    return render(request, 'department.html')

def doctors(request):
    return render(request, 'doctors.html')

def contact(request):
    return render(request, 'contact.html')

def booking(request):
    return render(request, 'booking.html')
