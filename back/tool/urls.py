from django import views
from django.urls import path
from . import views 
urlpatterns = [
    path('fileupload/', views.fileupload),
    path('display/',views.display),
    path('datacl/',views.data_clean),
    path('datacl2/',views.data_clean2),
    path('datacl3/',views.data_clean3),
    path('ml1/',views.ml1),
    path('cateml/',views.cateml),
    path('cateml1/',views.accur),
]   