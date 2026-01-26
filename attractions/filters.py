import django_filters
from .models import Attraction, AttractionCategory

class AttractionFilter(django_filters.FilterSet):
    category = django_filters.ModelChoiceFilter(queryset=AttractionCategory.objects.all())
    min_rating = django_filters.NumberFilter(method='filter_by_min_rating')
    city = django_filters.CharFilter(lookup_expr='icontains')
    country = django_filters.CharFilter(lookup_expr='icontains')
    
    class Meta:
        model = Attraction
        fields = {
            'name': ['icontains'],
            'is_active': ['exact'],
        }
    
    def filter_by_min_rating(self, queryset, name, value):
        # Filter attractions with average rating >= min_rating
        return queryset.filter(reviews__rating__gte=value).distinct()