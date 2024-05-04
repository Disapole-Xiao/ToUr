from django.urls import path

from . import views
 
app_name = 'travel'
urlpatterns = [
    path('', views.index, name='index'),
    path("<int:dest_id>/", views.detail, name="detail"),
    path("map/<int:dest_id>/", views.map, name="map"),
]