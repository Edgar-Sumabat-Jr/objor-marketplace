from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.contrib import messages
from django.templatetags.static import static
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Product, ProductCategory  # Updated import


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
    categories = ProductCategory.objects.all()
    #print(categories)  # Debugging line to check if categories are fetched
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

def add_to_cart(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        image = request.POST.get('image')
        description = request.POST.get('description')

        # Create a cart item dictionary
        cart_item = {
            'name': name,
            'price': price,
            'image': image,
            'description': description,
        }

        # Initialize cart in session if it doesn't exist
        if 'cart_items' not in request.session:
            request.session['cart_items'] = []

        # Add the new item to the cart
        request.session['cart_items'].append(cart_item)
        request.session.modified = True  # Mark the session as modified

        return redirect('cart')  # Redirect to the cart page

    return JsonResponse({'status': 'error'}, status=400)

def cart_view(request):
    cart_items = request.session.get('cart_items', [])
    
    return render(request, 'cart.html', {'cart_items': cart_items})

def remove_from_cart(request):
    if request.method == 'POST':
        index = int(request.POST.get('index'))
        
        # Retrieve the cart items from the session
        cart_items = request.session.get('cart_items', [])
        
        # Remove the item at the specified index
        if 0 <= index < len(cart_items):
            cart_items.pop(index)
        
        # Save the updated cart back to the session
        request.session['cart_items'] = cart_items
        request.session.modified = True  # Mark the session as modified

        return redirect('cart')  # Redirect back to the cart page

    return JsonResponse({'status': 'error'}, status=400)

def category_detail(request, category_id):
    category = get_object_or_404(ProductCategory, id=category_id)
    products = category.products.all()  # This fetches products related to the category
    return render(request, 'category_detail.html', {'category': category, 'products': products})
    

def shop_view(request):
    product_id = request.GET.get('id')
    product = None
    similar_products = []

    if product_id:
        product = get_object_or_404(Product, id=product_id)
        similar_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]  # Get similar products

    return render(request, 'shop.html', {
        'product': product,
        'similar_products': similar_products,
    })