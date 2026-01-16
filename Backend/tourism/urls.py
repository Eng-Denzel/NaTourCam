from django.urls import path
from . import views

urlpatterns = [
    path('sites/', views.TouristSiteListView.as_view(), name='site-list'),
    path('sites/<int:pk>/', views.TouristSiteDetailView.as_view(), name='site-detail'),
    path('sites/create/', views.admin_create_site, name='admin-create-site'),
    path('sites/<int:site_id>/update/', views.admin_update_site, name='admin-update-site'),
    path('sites/<int:site_id>/images/upload/', views.admin_upload_site_image, name='admin-upload-site-image'),
    path('images/<int:image_id>/delete/', views.admin_delete_site_image, name='admin-delete-site-image'),
    path('images/<int:image_id>/set-primary/', views.admin_set_primary_image, name='admin-set-primary-image'),
    # path('sites/nearby/', views.sites_near_location, name='sites-nearby'),
    path('content/', views.BilingualContentView.as_view(), name='content-list'),
    path('regions/', views.RegionListView.as_view(), name='region-list'),
]