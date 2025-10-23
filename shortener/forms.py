from django import forms
from django.utils.crypto import get_random_string
from django.conf import settings
from urllib.parse import urlparse

from .models import UrlData

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
        return url

    def save(self, commit=True, user=None):
        instance = super().save(commit=False)  # 創建一個尚未commit的資料
        instance.slug = ''.join(get_random_string(length=6))
        if user:
            instance.user = user
        if commit:
            instance.save()
        return instance
