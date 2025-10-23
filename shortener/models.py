from django.db import models
from django.contrib.auth.models import User


class UrlData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='urls')
    url = models.CharField(max_length=200)
    slug = models.CharField(max_length=15, unique=True, db_index=True)  # 因為要做比對要indexing
    click_count = models.PositiveIntegerField(default=0)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.slug} ({self.user.username})"


class UrlClick(models.Model):
    url = models.ForeignKey(UrlData, on_delete=models.CASCADE, related_name='clicks')
    click_time = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return f"{self.url.slug} clicked at {self.click_time}"
