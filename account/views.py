from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate

# 注册
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/travel/')  # 重定向到您的主页
    else:
        form = UserCreationForm()
    return render(request, 'account/register.html', {'form': form})

# 可以编写其他视图函数，如登录、注销等

# 登录
def login(request):
    context = {}
    return render(request, 'account/login.html', context)