from django.urls import path
from . import views

urlpatterns = [
    path('', views.bmi_),
    path('prediction/', views.prediction),
]