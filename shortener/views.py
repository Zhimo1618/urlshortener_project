from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.conf import settings
from django.db.models import Count

from .models import UrlData, UrlClick
from .forms import UrlForm


def get_client_ip(request):  # 收集點擊短網址用戶的資料
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


@login_required
def create_short_url(request):  # 創建新的短網址
    if request.method == 'POST':
        form = UrlForm(request.POST)
        if form.is_valid():
            form.save(user=request.user)
            return redirect('my_urls')
    else:
        form = UrlForm()
    return render(request, 'shortener/create.html', {'form': form})


@login_required
def list_user_urls(request):  # 列出用戶創建的短網址列表  # TODO 確認要用甚麼邏輯
    urls = UrlData.objects.filter(
        user=request.user,
        is_deleted=False
    ).annotate(
        total_clicks=Count('clicks')
    ).order_by('id')
    return render(request, 'shortener/my_urls.html', {'urls': urls})


def redirect_url(request, slug):  # 處理短網址跳轉的邏輯
    url_obj = get_object_or_404(UrlData, slug=slug, is_deleted=False)
    ip = get_client_ip(request)
    ua = request.META.get('HTTP_USER_AGENT', '')

    UrlClick.objects.create(url=url_obj, ip_address=ip, user_agent=ua)
    return redirect(url_obj.url, permanent=False)


def handle_404_view(request, exception):  # 處理如果404的狀況將其回到首頁(登入頁/用戶短網址列表)
    if settings.APPEND_SLASH and not request.path.endswith('/'):
        return redirect(request.path + '/')
    messages.warning(request, "您想連線的網址不存在或無權限，已導向首頁")
    return redirect('/')


@login_required
def get_url_stats(request, slug):  # 列出單一短網址的點擊資料(次數，紀錄等)
    url_obj = get_object_or_404(UrlData, slug=slug, user=request.user, is_deleted=False)
    clicks = url_obj.clicks.all().order_by('-click_time')
    return render(request, 'shortener/url_stats.html', {'url': url_obj, 'clicks': clicks})


@login_required
@require_http_methods(["DELETE"])
def delete_url(request, url_id):  # 將用戶創建的短網址軟刪除(不會出現在列表內)
    try:
        url = UrlData.objects.get(id=url_id, user=request.user)
        url.is_deleted = True
        url.save()
        return JsonResponse({'success': True})
    except UrlData.DoesNotExist:
        return JsonResponse({'success': False}, status=404)
