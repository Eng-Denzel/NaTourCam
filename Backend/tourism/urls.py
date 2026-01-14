from django.urls import path
from . import views

urlpatterns = [
    path('sites/', views.TouristSiteListView.as_view(), name='site-list'),
    path('sites/<int:pk>/', views.TouristSiteDetailView.as_view(), name='site-detail'),
    # path('sites/nearby/', views.sites_near_location, name='sites-nearby'),
    path('content/', views.BilingualContentView.as_view(), name='content-list'),
    path('regions/', views.RegionListView.as_view(), name='region-list'),
]