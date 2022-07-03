from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('contact/', views.contact),
    path('about/', views.dis),
    path('about/ss/', views.dis1),
    path('about/ss2/', views.dis2),
    path('about/ss3/', views.dis3),
    path('about/ss4/', views.dis4),
    path('about/ss5/', views.dis5),
]