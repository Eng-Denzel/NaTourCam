from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('tour-operator/', views.TourOperatorView.as_view(), name='tour-operator'),
    path('tour-operator/create/', views.TourOperatorCreateView.as_view(), name='tour-operator-create'),
    path('check-auth/', views.CheckAuthView.as_view(), name='check-auth'),
]