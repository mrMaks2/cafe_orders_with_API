from django import forms
from .models import Order

class OrderAddForm(forms.Form):
    '''
    Форма для добавления заказа
    '''
    table_number = forms.IntegerField(label='Номер стола',
                                      widget=forms.NumberInput(attrs={
                                          'min': '1',
                                          'class': 'form-control',
                                          'placeholder': 'Выберите номер стола'
                                      }))
    items = forms.CharField(label='Блюда',
                            widget=forms.TextInput(attrs={
                                'class': 'form-control',
                                'placeholder': 'Введите список блюд в формате "Имя блюда":"Цена" через пробел'
                            }))


class OrderDeleteForm(forms.Form):
    '''
    Форма для удаления заказа
    '''
    order = forms.ModelChoiceField(label='Удаление заказа',
                                   queryset=Order.objects.all(),
                                   widget=forms.Select(attrs={
                                       'class': 'form-control js-example-basic-multiple'
                                   }))


class OrderSearchForm(forms.Form):
    '''
    Форма для поиска заказа
    '''
    order = forms.CharField(label='Поиск заказа',
                            widget=forms.TextInput(attrs={
                                'class': 'form-control',
                                'placeholder': 'Введите номер стола или статус заказа в формате “В ожидании”, “Готово” или “Оплачено”'
                            }))


class OrderChangeStatusForm(forms.Form):
    '''
    Форма для изменения статуса заказа
    '''
    order = forms.ModelChoiceField(label='Изменение статуса заказа',
                                   queryset=Order.objects.all(),
                                   widget=forms.Select(attrs={
                                       'class': 'form-control js-example-basic-multiple'
                                   }))


    new_status = forms.ChoiceField(choices=Order.Status.choices,
                                 widget=forms.Select(attrs={
                                    'class': 'form-control'
                                 }))