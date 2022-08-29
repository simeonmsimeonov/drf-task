from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from api.models import Order, Product
from api.serializers import OrderSerializer, ProductSerializer, StatsSerializer
from django_filters import DateTimeFilter, ChoiceFilter, FilterSet
from rest_framework.pagination import PageNumberPagination


FILTER_CHOICES = (
    ('price', 'price'),
    ('count', 'count')
)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 1000


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = StandardResultsSetPagination


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = StandardResultsSetPagination


class StatsFilter(FilterSet):
    date_start = DateTimeFilter(field_name='date', lookup_expr='gte', label="date_start")
    date_end = DateTimeFilter(field_name='date', lookup_expr='lte', label="date_end")
    metric = ChoiceFilter(field_name='value', choices=FILTER_CHOICES, label="metric", method="filter_metric")

    def filter_metric(self, queryset, name, value):
        return self.queryset

    class Meta:
        model = Order
        fields = ()


class StatsViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = StatsSerializer
    filterset_class = StatsFilter
    filter_backends = [DjangoFilterBackend]


    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['metric'] = self.request.query_params.get('metric')
        context['date_start'] = self.request.query_params.get('date_start')
        context['date_end'] = self.request.query_params.get('date_end')
        return context

    def get_queryset(self):
        date_start = self.request.query_params.get('date_start')
        date_end = self.request.query_params.get('date_end')
        queryset = Order.objects.filter(date__range=[date_start, date_end])
        return queryset






