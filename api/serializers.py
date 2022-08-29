from collections import OrderedDict
from rest_framework import serializers
from api.models import Order, Product



class MyProductField(serializers.RelatedField):
    def to_representation(self, value):
        result = {
            "id": value.pk,
            "title": value.title,
            "price": float(value.price)
        }
        return result

    def get_choices(self, cutoff=None):
        queryset = self.get_queryset()
        if queryset is None:
            return {}

        if cutoff is not None:
            queryset = queryset[:cutoff]

        return OrderedDict([
            (
                item.pk,
                self.display_value(item)
            )
            for item in queryset
        ])

    def to_internal_value(self, data):
        model = self.queryset.model
        return model.objects.get(id=data)


class StatsSerializer(serializers.Serializer):
    month = serializers.SerializerMethodField()
    value = serializers.SerializerMethodField()

    def get_value(self, obj):
        metric = self.context['metric']
        date_start = self.context['date_start']
        date_end = self.context['date_end']
        queryset = Order.objects.filter(date__range=[date_start, date_end]).distinct()

        if metric == "price":
            result = sum([prod.price for order in queryset for prod in order.products.all()])
            return result
        elif metric == "count":
            result = [order.products.count() for order in queryset]
            return sum(result)

    def get_month(self, obj):
        return obj.short_date()

    class Meta:
        model = Order
        fields = ()


class OrderSerializer(serializers.ModelSerializer):
    products = MyProductField(many=True, queryset=Product.objects.all())

    class Meta:
        model = Order
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'