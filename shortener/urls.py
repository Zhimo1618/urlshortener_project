from django.urls import path

from . import views

urlpatterns = [
    path('', views.my_urls, name='my_urls'),
    path('create/', views.create_short_url, name='create_short_url'),
    path('stats/<slug:slug>/', views.url_stats, name='url_stats'),
    path('u/<slug:slug>/', views.url_redirect, name='url_redirect'),
    path('delete/<int:url_id>/', views.delete_url, name='delete_url'),
    ]
