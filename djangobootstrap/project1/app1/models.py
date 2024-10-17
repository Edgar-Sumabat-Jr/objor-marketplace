from django.db import models

class JewelryCategory(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='jewelry_images/')

    def __str__(self):
        return self.name