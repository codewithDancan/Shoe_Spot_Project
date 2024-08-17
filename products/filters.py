import django_filters
from .models import Shoe
from django_filters import fields

class ShoesFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")
    price_gt = django_filters.NumberFilter(field_name="price", lookup_expr='gt')
    price_lt = django_filters.NumberFilter(field_name="price", lookup_expr='lt')
    class Meta:
        model = Shoe
        fields = {
            'name'
        }