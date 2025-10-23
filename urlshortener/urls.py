from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('shortener.urls')),
    ]

handler404 = 'shortener.views.custom_404_view'