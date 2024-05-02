from django.urls import path

from . import views

app_name = "diary"
urlpatterns = [
    path("", views.diary, name="diary"),
    path("<int:diary_id>/", views.detail, name="detail"),
]