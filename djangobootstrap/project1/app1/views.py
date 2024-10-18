from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.contrib import messages
from .models import JewelryCategory
from django.templatetags.static import static


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
    categories = JewelryCategory.objects.all()
    return render(request, 'home.html', {'categories': categories})


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


def cart_view(request):
    trending_products = [
        {
            'name': 'Sparkling Heart Ring',
            'price': '$55.00',
            'description': 'A delicate heart-shaped ring adorned with sparkling stones.',
            'image': static('images/rings.jpg')  # Use the static helper
        },
        {
            'name': 'Classic Pandora Bracelet',
            'price': '$65.00',
            'description': 'A timeless silver bracelet, perfect for your charms.',
            'image': static('images/bracelets.jpg')  # Use the static helper
        },
        {
            'name': 'Rose Gold Pendant Necklace',
            'price': '$75.00',
            'description': 'An elegant necklace featuring a rose gold pendant.',
            'image': static('images/necklaces.jpg')  # Use the static helper
        }
    ]
    
    return render(request, 'cart.html', {'trending_products': trending_products})

def bracelet_view(request):
    return render(request, 'bracelet.html')

def rings_view(request):
    return render(request, 'rings.html')

def earrings_view(request):
    return render(request, 'earrings.html')

def necklace_view(request):
    return render(request, 'necklace.html')