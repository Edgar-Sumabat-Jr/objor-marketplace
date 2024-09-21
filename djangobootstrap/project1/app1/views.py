from django.shortcuts import render, redirect
# from django.http import HttpResponse

def home_view(request):
    return render(request, 'home.html')
    
def login_view(request):
    return render(request, 'login.html')