from django.shortcuts import render
from marketplace.models import Product


# Create your views here.
def index(request):
    products = Product.objects.all().order_by("-created_at")

    print(products)
    return render(request, "marketplace/index.html", {"products": products})
