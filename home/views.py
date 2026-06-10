from django.shortcuts import render

# Create your views here.
def doctors(request):
    return render(request, 'doctors.html')