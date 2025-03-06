from django.core.validators import MinValueValidator
from django.db import models

class Order(models.Model):

    table_number = models.IntegerField(verbose_name='Номер стола')
    items = models.TextField(verbose_name='Список блюд')
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.00)],
        verbose_name='Общая стоимость',
        default=0.00
    )
    status = models.CharField(
        max_length=10,
        default='В ожидании',
        verbose_name='Статус заказа'
    )

    def save(self, *args, **kwargs):
        self.total_price = sum(item['price'] for item in self.items)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Заказ под номером ID {self.id}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'