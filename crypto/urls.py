from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('crypto_Prices/', views.crypto_Prices, name="crypto_Prices"),
    path('all_marketcap/', views.all_marketcap, name="all_marketcap"),
    path('block_list/', views.block_list, name="block_list"),
    path('all_news/', views.all_news, name="all_news"),
    path('block_explorer/', views.block_explorer, name="block_explorer"),
    path('block_trans/', views.block_trans, name="block_trans"),
]