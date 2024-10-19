from . import views
from django.urls import path

app_name = "marketplace"

urlpatterns = [path("index", views.index, name="index")]