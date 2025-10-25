from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),  # 登入邏輯用allauth做處理
    path('', include('shortener.urls')),  # 網址邏輯在shortener內處理
]

handler404 = 'shortener.views.handle_404_view'
