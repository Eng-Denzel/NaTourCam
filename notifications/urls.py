from django.urls import path
from . import views

urlpatterns = [
    path('', views.NotificationListView.as_view(), name='notification-list'),
    path('<int:pk>/', views.NotificationDetailView.as_view(), name='notification-detail'),
    path('unread-count/', views.UnreadNotificationCountView.as_view(), name='unread-notification-count'),
    path('mark-all-read/', views.MarkAllNotificationsReadView.as_view(), name='mark-all-read'),
    path('preferences/', views.NotificationPreferenceView.as_view(), name='notification-preferences'),
]