from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('crypto_Prices/', views.crypto_Prices, name="crypto_Prices"),
]