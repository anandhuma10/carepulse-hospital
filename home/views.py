from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'index.html')   

def about(request):
    return render(request, 'about.html')

def department(request):
    return render(request, 'department.html')