from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from api.models import Order, Product
from api.serializers import OrderSerializer, ProductSerializer, StatsSerializer
from django_filters import FilterSet, DateTimeFilter
from django_filters import FilterSet, AllValuesFilter
from django_filters import DateTimeFilter, NumberFilter


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer



class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class StatsFilter(FilterSet):
    date_start = DateTimeFilter(field_name='date', lookup_expr='gte', label="date_start")
    date_end = DateTimeFilter(field_name='date', lookup_expr='lte', label="date_end")
    # metric = ChoiceFilter(choices=FILTER_CHOICES, label='metric')


    class Meta:
        model = Order
        fields = ()


class StatsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filterset_class = StatsFilter
    # filterset_fields = ['date']
    filter_backends = [DjangoFilterBackend]
    # filter_backends = [DjangoFilterBackend]


