from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('users/me/', views.UserDetailView.as_view(), name='user-detail'),
    path('users/<int:user_id>/update/', views.admin_update_user, name='admin-update-user'),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
]