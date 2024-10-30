from django.db import models
from django.templatetags.static import static

class ProductCategory(models.Model):
    name = models.CharField(max_length=100)
    image = models.CharField(max_length=255)  # Path to category image

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='products')
    image = models.CharField(max_length=255)  # Path to product image

    def __str__(self):
        return self.name

    def get_image_url(self):
        return static(self.image)  # Helper to get full static URL
