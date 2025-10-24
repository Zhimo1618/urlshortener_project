from django.contrib import admin

from .models import UrlData, UrlClick


@admin.register(UrlData)
class UrlDataAdmin(admin.ModelAdmin):
    list_display = ('slug', 'url', 'user')
    search_fields = ('slug', 'url', 'user__username')

@admin.register(UrlClick)
class UrlClickAdmin(admin.ModelAdmin):
    list_display = ('url', 'click_time', 'ip_address')
    list_filter = ('click_time',)
