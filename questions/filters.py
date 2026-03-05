import django_filters
from django.db.models import Q
from .models import Question

class QuestionFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='search_filter', label='Search')
    tag = django_filters.CharFilter(field_name='tags__name', lookup_expr='iexact')
    sort = django_filters.OrderingFilter(
        fields=(
            ('created_at', 'oldest'),
            ('-created_at', 'newest'),
        ),
        label='Sort'
    )

    class Meta:
        model = Question
        fields = ['q', 'tag', 'sort']

    def search_filter(self, queryset, name, value):
        return queryset.filter(
            Q(title__icontains=value) | 
            Q(description__icontains=value) |
            Q(tags__name__icontains=value)
        ).distinct()
