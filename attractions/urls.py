from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.AttractionCategoryListView.as_view(), name='attraction-categories'),
    path('', views.AttractionListView.as_view(), name='attraction-list'),
    path('<int:pk>/', views.AttractionDetailView.as_view(), name='attraction-detail'),
    path('create/', views.AttractionCreateView.as_view(), name='attraction-create'),
    path('<int:attraction_id>/reviews/', views.AttractionReviewListView.as_view(), name='attraction-reviews'),
    path('reviews/create/', views.AttractionReviewCreateView.as_view(), name='attraction-review-create'),
]