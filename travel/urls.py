from django.urls import path

from . import views
 
app_name = 'travel'
urlpatterns = [
    path('', views.index, name='index'),
    path("<int:dest_id>/", views.detail, name="detail"),
    path("map/<int:dest_id>/", views.map, name="map"),
    path("map/<int:dest_id>/plan_route/", views.plan_route, name="plan_route"),
    path('map/<int:dest_id>/search_amenity/', views.search_amenity, name='search_amenity'),

]