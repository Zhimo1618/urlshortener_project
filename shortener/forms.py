import random, string

from django import forms

from .models import UrlData

class UrlForm(forms.ModelForm):
    class Meta:
        model = UrlData
        fields = ['url']

    def save(self, commit=True, user=None):
        instance = super().save(commit=False)
        instance.slug = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        if user:
            instance.user = user
        if commit:
            instance.save()
        return instance
