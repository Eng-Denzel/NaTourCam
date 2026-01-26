import django_filters
from .models import Tour

class TourFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    start_date = django_filters.DateFilter(field_name='start_date', lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name='end_date', lookup_expr='lte')
    difficulty_level = django_filters.ChoiceFilter(choices=[
        ('easy', 'Easy'),
        ('moderate', 'Moderate'),
        ('challenging', 'Challenging'),
        ('difficult', 'Difficult')
    ])
    duration_days = django_filters.NumberFilter(field_name='duration_days')
    
    class Meta:
        model = Tour
        fields = {
            'title': ['icontains'],
            'start_location': ['icontains'],
            'end_location': ['icontains'],
            'is_active': ['exact'],
        }