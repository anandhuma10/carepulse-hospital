from django.shortcuts import render

# Create your views here.
def department(request):
    return render(request, 'department.html')