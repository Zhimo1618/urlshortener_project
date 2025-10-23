from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse

from .models import UrlData, UrlClick
from .forms import UrlForm

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')

@login_required
def create_short_url(request):
    if request.method == 'POST':
        form = UrlForm(request.POST)
        if form.is_valid():
            form.save(user=request.user)
            return redirect('my_urls')
    else:
        form = UrlForm()
    return render(request, 'shortener/create.html', {'form': form})

@login_required
def my_urls(request):
    urls = UrlData.objects.filter(user=request.user, is_deleted=False)
    return render(request, 'shortener/my_urls.html', {'urls': urls})

def url_redirect(request, slug):
    url_obj = get_object_or_404(UrlData, slug=slug, is_deleted=False)
    ip = get_client_ip(request)
    ua = request.META.get('HTTP_USER_AGENT', '')

    UrlClick.objects.create(url=url_obj, ip_address=ip, user_agent=ua)
    url_obj.click_count += 1
    url_obj.save(update_fields=['click_count'])
    return redirect(url_obj.url)

def custom_404_view(request, exception):
    messages.warning(request, "您訪問的頁面不存在，已導向首頁")
    return redirect('/')

@login_required
def url_stats(request, slug):
    url_obj = get_object_or_404(UrlData, slug=slug, user=request.user, is_deleted=False)
    clicks = url_obj.clicks.all().order_by('-click_time')
    return render(request, 'shortener/url_stats.html', {'url': url_obj, 'clicks': clicks})

@login_required
@require_http_methods(["DELETE"])
def delete_url(request, url_id):
    try:
        url = UrlData.objects.get(id=url_id, user=request.user)
        url.is_deleted = True
        url.save()
        return JsonResponse({'success': True})
    except UrlData.DoesNotExist:
        return JsonResponse({'success': False}, status=404)
