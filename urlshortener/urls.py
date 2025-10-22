from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('shortener.urls')),
    path('login/', views.custom_login, name="login"),
    path('logout/', views.custom_logout, name="logout"),
    ]
