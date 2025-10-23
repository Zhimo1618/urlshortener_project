from django.urls import path

from . import views

urlpatterns = [
    path('', views.list_user_urls, name='my_urls'),
    path('create/', views.create_short_url, name='create_short_url'),
    path('stats/<slug:slug>/', views.get_url_stats, name='url_stats'),
    path('u/<slug:slug>/', views.redirect_url, name='url_redirect'),
    path('delete/<int:url_id>/', views.delete_url, name='delete_url'),
    ]
