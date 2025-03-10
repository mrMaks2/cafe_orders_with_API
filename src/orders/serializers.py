from rest_framework import serializers
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    """
    Сериализатор для преобразования объектов Order в JSON формат и обратно.

    Предоставляет функции проверки и преобразования для модели Order.
    """
    class Meta:
        model = Order
        fields = '__all__'