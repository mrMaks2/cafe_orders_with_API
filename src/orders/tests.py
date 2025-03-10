from django.test import TestCase
from .models import Order

class OrderModelTest(TestCase):
    def setUp(self):
        self.order = Order.objects.create(table_number=1, items=[{'name': 'Чай', 'price': 50}],
                                          status=Order.Status.PENDING)

    def test_order_creation(self):
        self.assertTrue(isinstance(self.order, Order))
        self.assertEqual(self.order.__str__(), f"Заказ под номером ID {self.order.pk}")

    def test_calculate_total_price(self):
        self.assertEqual(self.order.total_price, 50)
        self.order.items.append({'name': 'Кофе', 'price': 100})
        self.order.save()
        self.assertEqual(self.order.total_price, 150)

    def test_get_revenue_for_status(self):
        paid_order = Order.objects.create(table_number=2, items=[{'name': 'Пицца', 'price': 500}],
                                          status=Order.Status.PAID)
        revenue = sum([price.total_price for price in Order.objects.filter(status=Order.Status.PAID)])
        self.assertEqual(revenue, 500)