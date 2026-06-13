
from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
     path('department/', views.department, name='department'),
    path('doctors/', views.doctors, name='doctors'),
    path('contact/', views.contact, name='contact'),
    path('booking/', views.booking, name='booking'),
    

]