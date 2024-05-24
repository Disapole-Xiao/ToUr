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
# def login(request,user):
#     context = {}
#     return render(request, 'account/login.html', context)



from django.contrib.auth import get_user_model
from django.shortcuts import render
from .models import CustomUser

def index(request):
    # 获取用户模型
    User = get_user_model()
    # 使用自定义用户模型创建用户
    custom_user = CustomUser.objects.create_user(username='custom_user', password='password', user_interest=25)
    # 使用默认用户模型创建用户
    default_user = User.objects.create_user(username='default_user', password='password')

    return render(request, 'index.html')

# views.py

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .form import CustomUserCreationForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)  # 使用自定义的 authenticate 和 login 函数
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)  
        if user is not None:
            login(request, user)  
            return redirect('index')
        else:
            return render(request, 'login.html', {'error_message': 'Invalid username or password.'})
    return render(request, 'login.html', {})
