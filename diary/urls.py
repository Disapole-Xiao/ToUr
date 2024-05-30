from django.urls import path

from . import views

app_name = "diary"
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:diary_id>/", views.detail, name="detail"),
    path("<int:diary_id>/rate/", views.rate, name="rate"),
    path('add_diary/', views.add_diary, name='add_diary'),
    path('search_location/', views.search_location, name='search_location'),
]