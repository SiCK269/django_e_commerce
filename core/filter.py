import django_filters
from django_filters import DateFilter
from django.forms.widgets import TextInput

from .models import *


class DayRangeFilter(django_filters.FilterSet):
    start_date = DateFilter(
        label='From ', field_name="last_visit", lookup_expr='gte', widget=TextInput(attrs={'placeholder': 'From', 'style': 'text-align:center;'}))
    end_date = DateFilter(
        label='Until ', field_name="last_visit", lookup_expr='lte', widget=TextInput(attrs={'placeholder': 'Until', 'style': 'text-align:center;'}))

    class Meta:
        model = Analysis
        fields = '__all__'
        exclude = ['item', 'visited_by', 'anonymous', 'visits']
