from django.urls import path, re_path

from . import views
 
app_name = 'travel'
urlpatterns = [
    path('', views.index, name='index'),
    path('load_dests/', views.load_dests, name='load_dests'),
    path('<int:dest_id>/', views.detail, name='detail'),
    path('map/<int:dest_id>/', views.map, name='map'),
    path('map/<int:dest_id>/edit/', views.map, {'edit': True}, name='map_edit'),
    path('map/<int:dest_id>/edit/update_coord/', views.update_coord, name='update_coord'),
    re_path('^map/(?P<dest_id>\d+)/(edit/)?plan_route/$', views.plan_route, name='plan_route'),
    re_path('map/(?P<dest_id>\d+)/(edit/)?search_amenity/$', views.search_amenity, name='search_amenity'),
    re_path('map/(?P<dest_id>\d+)/(edit/)?search_restaurant/$', views.search_restaurant, name='search_restaurant'),
]

map_operations = [
    
]