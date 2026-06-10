from django.shortcuts import render

# Create your views here.
<<<<<<< HEAD
def home(request):
    return render(request, 'index.html')
=======
def index(request):
    return render(request, 'index.html')   

def about(request):
    return render(request, 'about.html')
>>>>>>> feature/about
