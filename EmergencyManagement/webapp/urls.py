from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('', views.map, name='map'),
    path('list/', views.buildingsList, name='building-list'),
    path('building/<uuid:building_id>', views.buildingDetails, name='building-detail'),
    path('results/', views.results, name='results'),
    path('buildings/', views.BuildingViewSet.as_view({'get': 'list', 'post': 'create','put': 'update'}), name='buildings'),
    path('buildings/<uuid:pk>/', views.BuildingViewSet.as_view({'get': 'list', 'post': 'create','put': 'update'}), name='buildings'),
    path('polls/', views.EmergencyPollResultViewSet.as_view({'get': 'list', 'post': 'create'}), name='polls'),
    path('device/', views.DeviceCountViewSet.as_view({'get': 'list', 'post': 'create'}), name='device'),
    path('emergencyindicator/', views.EmergencyModeIndicatorViewSet.as_view({'get': 'list', 'post': 'create','put': 'update'}), name='emergencyindicator'),
    # path('map/', views.map, name='map'),
    path('form/', views.upload_file, name='upload_file'),
    path('alert/', views.alert, name='alert'),
    path('getDeviceCountJSON/<uuid:building_id>/<int:weekday>', views.getDeviceCountJSON, name='getDeviceCountJSON'),
    path('getEmergencyPollJSON/', views.getEmergencyPollJSON, name='getEmergencyPollJSON'),
    path('getBuildingFilterJSON/', views.getBuildingFilterJSON, name='getBuildingFilterJSON'),
    path('addBuilding/', views.addBuilding, name='addBuilding'),
    path('getBuildingSearchJSON/', views.getBuildingSearchJSON, name='getBuildingSearchJSON'),
    path('map/search/', views.getSearchJSON, name='getSearchJSON'),
    path('toggle_emergency_indicator/', views.toggle_emergency_indicator, name='toggle_emergency_indicator'),
    path('about/', views.index, name='index')
]

urlpatterns += staticfiles_urlpatterns()