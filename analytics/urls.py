from django.urls import path
from . import views

urlpatterns = [
    path('user/', views.UserAnalyticsView.as_view(), name='user-analytics'),
    path('attraction/<int:attraction_id>/', views.AttractionAnalyticsView.as_view(), name='attraction-analytics'),
    path('tour/<int:tour_id>/', views.TourAnalyticsView.as_view(), name='tour-analytics'),
    path('admin/dashboard/', views.AdminDashboardView.as_view(), name='admin-dashboard'),
]