from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from .forms import CustomUserCreationForm, CustomUserChangeForm, CustomPasswordChangeForm
from travel.models import Category
from diary.models import Diary

User = get_user_model()

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)  # 确保处理文件上传
        if form.is_valid():
            user = form.save()
            return redirect('/travel/')  # 重定向到您的主页
    else:
        form = CustomUserCreationForm()
    categories = Category.objects.all()  # 查询所有兴趣标签
    return render(request, 'account/register.html', {'form': form, 'categories': categories})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/travel/')  # 重定向到您的主页
            else:
                error_message = 'Invalid username or password.'
                return render(request, 'account/login.html', {'error_message': error_message})
    else:
        form = AuthenticationForm()
    return render(request, 'account/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('/')  # 重定向到登录页面或其他合适的页面

@login_required
def profile_view(request):
    user = request.user
    if request.method == 'POST':
        profile_form = CustomUserChangeForm(request.POST, request.FILES, instance=user)
        password_form = CustomPasswordChangeForm(user, request.POST)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('account:profile')
        elif password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)
            return redirect('account:profile')
    else:
        profile_form = CustomUserChangeForm(instance=user)
        password_form = CustomPasswordChangeForm(user)

    user_diaries = Diary.objects.filter(author=user)
    context = {
        'profile_form': profile_form,
        'password_form': password_form,
        'user_diaries': user_diaries,
    }
    return render(request, 'account/profile.html', context)