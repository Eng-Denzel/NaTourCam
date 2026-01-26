from django.urls import path
from . import views

urlpatterns = [
    path('', views.TourListView.as_view(), name='tour-list'),
    path('<int:pk>/', views.TourDetailView.as_view(), name='tour-detail'),
    path('create/', views.TourCreateView.as_view(), name='tour-create'),
    path('<int:tour_id>/itinerary/', views.TourItineraryListView.as_view(), name='tour-itinerary'),
    path('itinerary/create/', views.TourItineraryCreateView.as_view(), name='tour-itinerary-create'),
    path('<int:tour_id>/availability/', views.TourAvailabilityListView.as_view(), name='tour-availability'),
    path('availability/create/', views.TourAvailabilityCreateView.as_view(), name='tour-availability-create'),
]