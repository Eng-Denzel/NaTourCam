"""
URL routing for DDD-based tourism views
These are new endpoints that use the DDD architecture
"""
from django.urls import path
from . import views_ddd

urlpatterns = [
    # Destination endpoints
    path('ddd/destinations/', views_ddd.list_destinations_ddd, name='ddd-destinations-list'),
    path('ddd/destinations/<int:destination_id>/', views_ddd.get_destination_ddd, name='ddd-destination-detail'),
    path('ddd/destinations/create/', views_ddd.create_destination_ddd, name='ddd-destination-create'),
    path('ddd/destinations/<int:destination_id>/update/', views_ddd.update_destination_ddd, name='ddd-destination-update'),
    path('ddd/destinations/<int:destination_id>/activate/', views_ddd.activate_destination_ddd, name='ddd-destination-activate'),
    path('ddd/destinations/<int:destination_id>/deactivate/', views_ddd.deactivate_destination_ddd, name='ddd-destination-deactivate'),
    path('ddd/destinations/search/', views_ddd.search_destinations_ddd, name='ddd-destinations-search'),
    
    # Region endpoints
    path('ddd/regions/', views_ddd.list_regions_ddd, name='ddd-regions-list'),
]
