from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('', include("django.contrib.auth.urls")),
    path('cart/', views.cart_view, name='cart'),
    path('bracelet/', views.bracelet_view, name='bracelet'),
    path('rings/', views.rings_view, name='rings'),
    path('earrings/', views.earrings_view, name='earrings'),
    path('necklace/', views.necklace_view, name='necklace'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
     path('remove-from-cart/', views.remove_from_cart, name='remove_from_cart'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)