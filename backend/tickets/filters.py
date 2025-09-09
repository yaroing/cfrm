"""
Filtres pour l'API des tickets
"""
import django_filters
from django.db.models import Q
from .models import Ticket


class TicketFilter(django_filters.FilterSet):
    """Filtres pour les tickets"""
    
    # Filtres de base
    category = django_filters.CharFilter(field_name='category__name')
    priority = django_filters.CharFilter(field_name='priority__name')
    status = django_filters.CharFilter(field_name='status__name')
    channel = django_filters.CharFilter(field_name='channel__name')
    assigned_to = django_filters.NumberFilter(field_name='assigned_to__id')
    
    # Filtres de date
    created_after = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    updated_after = django_filters.DateTimeFilter(field_name='updated_at', lookup_expr='gte')
    updated_before = django_filters.DateTimeFilter(field_name='updated_at', lookup_expr='lte')
    
    # Filtres booléens
    is_anonymous = django_filters.BooleanFilter()
    is_psea = django_filters.BooleanFilter()
    is_overdue = django_filters.BooleanFilter(method='filter_overdue')
    
    # Filtres de recherche
    search = django_filters.CharFilter(method='filter_search')
    
    # Filtres de localisation
    has_location = django_filters.BooleanFilter(method='filter_has_location')
    
    class Meta:
        model = Ticket
        fields = [
            'category', 'priority', 'status', 'channel', 'assigned_to',
            'is_anonymous', 'is_psea', 'is_overdue',
            'created_after', 'created_before', 'updated_after', 'updated_before',
            'search', 'has_location'
        ]
    
    def filter_overdue(self, queryset, name, value):
        """Filtrer les tickets en retard"""
        if value:
            from django.utils import timezone
            return queryset.filter(
                sla_deadline__lt=timezone.now(),
                status__is_final=False
            )
        return queryset
    
    def filter_search(self, queryset, name, value):
        """Recherche textuelle dans les tickets"""
        if value:
            return queryset.filter(
                Q(title__icontains=value) |
                Q(content__icontains=value) |
                Q(submitter_name__icontains=value) |
                Q(submitter_phone__icontains=value) |
                Q(submitter_email__icontains=value)
            )
        return queryset
    
    def filter_has_location(self, queryset, name, value):
        """Filtrer les tickets avec ou sans localisation"""
        if value:
            return queryset.filter(
                latitude__isnull=False,
                longitude__isnull=False
            )
        else:
            return queryset.filter(
                Q(latitude__isnull=True) | Q(longitude__isnull=True)
            )
