import django_filters as filters

from .models import Advertisement


class AdvertisementFilter(filters.FilterSet):
    """Фильтры для объявлений."""

    created_at = filters.DateFromToRangeFilter()
    status = filters.CharFilter(field_name="status")

    class Meta:
        model = Advertisement
        fields = ["created_at", "status"]