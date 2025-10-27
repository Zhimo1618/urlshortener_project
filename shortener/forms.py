from django import forms
from django.utils.crypto import get_random_string
from django.conf import settings
from urllib.parse import urlparse

from .models import UrlData

ALLOWED_CHARS = 'abcdefghijkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789'


class UrlForm(forms.ModelForm):
    class Meta:
        model = UrlData
        fields = ['url']

    def clean_url(self):  # 確認網址本身是否為短網址
        url = self.cleaned_data['url']
        domain = settings.SHORTENER_DOMAIN.replace("https://", "").replace("http://", "")

        parsed = urlparse(url)
        if parsed.netloc == domain and parsed.path.startswith('/u/'):
            raise forms.ValidationError("這個網址已經是短網址了，不能再縮一次！")
        hostname = parsed.hostname
        if hostname:
            hostname_lower = hostname.lower()

            # 封鎖 localhost
            if hostname_lower in ['localhost', '127.0.0.1', '0.0.0.0', '::1']:
                raise forms.ValidationError("不允許使用本機 URL")

        return url

    def save(self, commit=True, user=None):
        instance = super().save(commit=False)  # 創建一個尚未commit的資料
        slug = get_random_string(length=6, allowed_chars=ALLOWED_CHARS)  # 把 0/O/1/l/I 給去除 避免短網址混淆
        while UrlData.objects.filter(slug=slug).exists():  # 去查這個 slug 是否有碰撞，有的話產一個新的
            slug = get_random_string(length=6, allowed_chars=ALLOWED_CHARS)
        instance.slug = slug
        if user:
            instance.user = user
        if commit:
            instance.save()
        return instance
