from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def custom_login(request):
    if (request.user.is_authenticated):
        return redirect("/")
    return render(request, "login.html")

@login_required
def custom_logout(request):
    logout(request)
    return redirect("/login/")