from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegistrationForm

def home_view(request):
    return render(request, 'home.html')

def login_view(request):
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            if password == confirm_password:
                user.set_password(password)
                user.save()
                login(request, user)
                return redirect('home')  # Redirect to home page after registration
            else:
                form.add_error('confirm_password', 'Passwords do not match')
    else:
        form = RegistrationForm()
    
    return render(request, 'register.html', {'form': form})
