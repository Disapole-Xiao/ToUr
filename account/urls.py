from django.urls import path


from . import views

appname = 'account'
urlpatterns = [
    path('register/', views.register, name='register'), # 注册
    path('login/', views.login, name='login')
]