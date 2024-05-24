from django.urls import path


from . import views

app_name = 'account'
urlpatterns = [
    path('register/', views.register, name='register'), # 注册
    path('login/', views.user_login, name='login')
]