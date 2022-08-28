
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
    products = MyProductField(many=True, queryset=Product.objects.all())

    class Meta:
        model = Order
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    products = MyProductField(many=True, queryset=Product.objects.all())

    class Meta:
        model = Order
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'