from django.urls import path

from . import views
 
app_name = 'travel'
urlpatterns = [
    path('', views.index, name='index')
]