from django.shortcuts import render
from django.shortcuts import render , HttpResponseRedirect , HttpResponse

# Create your views here.
 
def contact(request):
    return render(request , 'home_page/contact.html')
 
def home(request):
    return render(request,'home_page/h.html')

def dis(request): # main page
    return render(request,'home_page/about_card.html')

def dis1(request): #1 
    return render(request,'home_page/introduction.html')

def dis2(request):
    return render(request,'home_page/symptoms.html')

def dis3(request):
    return render(request,'home_page/cause.html')

def dis4(request):
    return render(request,'home_page/risk_factor.html')

def dis5(request):
    return render(request,'home_page/treatment.html')