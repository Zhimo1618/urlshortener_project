from django.db import models
from django.contrib.auth.models import User


class UrlData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='urls')
    url = models.URLField(max_length=2048)
    create_time = models.DateTimeField(auto_now_add=True)
    slug = models.CharField(max_length=15, unique=True, db_index=True)  # 因為要做比對要indexing
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.slug} ({self.user.username})"
    # TODO 要不要多開meta


class UrlClick(models.Model):
    url = models.ForeignKey(UrlData, on_delete=models.CASCADE, related_name='clicks')
    click_time = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    user_browser = models.CharField(blank=True)
    user_os = models.CharField(blank=True)
    user_device = models.CharField(blank=True)
    user_is_mobile = models.BooleanField()

    def __str__(self):
        return f"{self.url.slug} clicked at {self.click_time}"
