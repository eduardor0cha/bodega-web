from django.urls import path
from app_bodega_web import views

urlpatterns = [
    path("", views.home, name="home")
]
