from django.shortcuts import render
from .models import Department

def department_list(request):
    departments = Department.objects.all()
    # ⚠️ Double check that 'department.html' matches your exact file name
    return render(request, 'department.html', {'departments': departments})