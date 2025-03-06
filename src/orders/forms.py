from django import forms
from .models import Order

class OrderAddForm(forms.Form):
    table_number = forms.IntegerField(label='Номер стола',
                                      widget=forms.NumberInput(attrs={
                                          'class': 'form-control',
                                          'placeholder': 'Введите номер стола'
                                      }))
    items = forms.CharField(label='Блюда',
                            widget=forms.TextInput(attrs={
                                'class': 'form-control',
                                'placeholder': 'Введите список блюд в формате "Имя блюда":"Цена" через пробел'
                            }))

class OrderDeleteForm(forms.Form):
    order = forms.ModelChoiceField(label='Удаление заказа',
                                   queryset=Order.objects.only('id'),
                                   widget=forms.Select(attrs={
                                       'class': 'form-control js-example-basic-multiple'
                                   }))

class OrderSearchForm(forms.Form):
    order = forms.CharField(label='Поиск заказа',
                            widget=forms.TextInput(attrs={
                                'class': 'form-control',
                                'placeholder': 'Введите номер стола или статус заказа'
                            }))

class OrderChangeStatusForm(forms.Form):
    order = forms.ModelChoiceField(label='Изменение статуса заказа',
                                   queryset=Order.objects.only('id'),
                                   widget=forms.Select(attrs={
                                       'class': 'form-control js-example-basic-multiple'
                                   }))

    new_status = forms.CharField(label='Новый статус',
                                 widget=forms.TextInput(attrs={
                                    'class': 'form-control',
                                    'placeholder': 'Введите новый статус (“в ожидании”, “готово”, “оплачено”)'
                                 }))