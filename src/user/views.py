from django.shortcuts import render, redirect

from django.contrib.auth import login, logout
from .forms import CustomUserLoginForm


def user_login(request):
    if request.method == 'POST':
        form = CustomUserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('article:post_list')
    else:
        form = CustomUserLoginForm()

    context = {
        "title": "Login",
        "form": form
    }

    return render(request, 'user/login.html', context=context)


def logout_view(request):
    logout(request)
    return redirect('article:post_list')
