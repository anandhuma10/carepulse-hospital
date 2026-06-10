from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
     path('department/', views.department, name='department'),
    path('doctors/', views.doctors, name='doctors'),
]
