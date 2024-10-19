from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.contrib import messages


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

def home_view(request):
    return render(request, 'home.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)  # Adjust based on your user model

        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to your desired page
        else:
            messages.error(request, 'Incorrect email or password.')
            return render(request, 'login.html')

    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Specify the backend when logging in
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')  # Ensure the backend is set
            return redirect('home')  # Redirect to home page after registration
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'register.html', {'form': form})
