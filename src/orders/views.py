from django.db.models import Sum
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Order
from .forms import *
from rest_framework import generics
from .serializers import OrderSerializer
from rest_framework import filters

def order_list(request):
    '''
    Отображает список всех заказов.

    Извлекает все заказы из базы данных и отображает их на странице
    списка заказов с использованием шаблона «order_list.html».
    '''
    orders = Order.objects.all()
    for order in orders:
        order.items = eval(order.items)
        orders.order = order
    return render(request, 'order_list.html', {'orders': orders})


def add_order(request):
    """
    Создает новый заказ.

    Если метод запроса — POST, проверяет данные формы и создает
    новый объект Order и выводит сообщение об успешном проведении операции.
    Перенаправляет на страницу списка заказов при успешном создании.
    Если форма не валидна, то выводит сообщение об ошибке.
    Если GET, отображает форму для добавления нового заказа.
    """
    if request.method == 'POST':
        form = OrderAddForm(request.POST)
        if form.is_valid():
            table_number = request.POST['table_number']
            items = request.POST.get('items')
            if ':' in items:
                items = items.split(' ')
                items_with_prices = [
                    {
                        'name': item.split(':')[0],
                        'price': float(item.split(':')[1])
                    } for item in items
                ]
                order = Order(table_number=table_number, items=items_with_prices)
                if order:
                    order.save()
                    messages.success(request, "Заказ успешно создан.")
                    return redirect('orders:order_list')
                else:
                    messages.error(request, "Ошибка при создании заказа. Пожалуйста, исправьте ошибки в форме.")
            else:
                messages.error(request, "Ошибка при создании заказа. Пожалуйста, исправьте ошибки в форме.")
    form = OrderAddForm()
    return render(request, 'add_order.html', {'form': form})


def delete_order(request):
    '''
    Удаляет выбранные заказ из системы.

    Если метод запроса — POST, извлекает заказ по идентификатору и удаляет его из базы данных.
    При успешном удалении выводит сообщение об этом.
    Перенаправляет на страницу списка заказов после удаления.
    Если GET, отображает форму для удаления заказа.
    '''
    if request.method == 'POST':
        order_id = request.POST['order']
        order = Order.objects.get(id = order_id)
        order.delete()
        messages.success(request,'Заказ успешно удален')
        return redirect('orders:order_list')
    form = OrderDeleteForm()
    return render(request, 'delete_order.html', {'form': form})


def search_order(request):
    '''
    Ищет заказы по номеру стола или по статусу заказа.

    Если метод запроса — POST, извлекает заказы из базы данных и отображает их на странице
    списка заказов с использованием шаблона «order_list.html».
    Проверяет каким объектом Python являются введенные данные.
    Если цифра, то проверяет на наличие заказа с таким номером стола.
    Если строка, то проверяет на корректность написанного статуса.
    Если GET, отображает форму для поиска заказа.
    '''
    if request.method == 'POST':
        query = request.POST['order']
        if query.isdigit() and Order.objects.filter(table_number = query):
            orders = Order.objects.filter(table_number = query)
            for order in orders:
                order.items = eval(order.items)
                orders.order = order
            return render(request, 'order_list.html', {'orders': orders})
        elif query in str(Order.Status.choices) and all([ord(char) in range(1040, 1104) or ord(char) == 32 for char in query]):
            orders = Order.objects.filter(status = query)
            for order in orders:
                order.items = eval(order.items)
                orders.order = order
            return render(request, 'order_list.html', {'orders': orders})
        else:
            messages.error(request, 'Ошибка при поиске заказов. Пожалуйста, исправьте ошибки в форме.')
    form = OrderSearchForm()
    return render(request, 'search_order.html', {'form': form})


def change_status(request):
    '''
    Меняет статус заказа.

    Если метод запроса — POST, извлекает заказ из базы данных,
    проверяет данные формы, меняет его статус и выводит сообщение
    об успешном изменении.
    Если GET, отображает форму для изменения статуса заказа.
    '''
    if request.method == 'POST':
        order_id = request.POST['order']
        order = Order.objects.get(id=order_id)
        form = OrderChangeStatusForm(request.POST)
        if form.is_valid():
            order.status = request.POST['new_status']
            order.items = eval(order.items)
            order.save()
            messages.success(request,'Статус заказа успешно изменен')
            return redirect('orders:change_status')
    form = OrderChangeStatusForm()
    return render(request, 'change_status.html', {'form': form})


def revenue_report(request):
    '''
    Выводит общую выручку за заказы, у которых статус 'Оплачено'.
    '''
    total_revenue = Order.objects.filter(status='Оплачено').aggregate(Sum('total_price'))['total_price__sum'] or 0
    return render(request, 'revenue_report.html', {'total_revenue': total_revenue})


class OrderListAPIView(generics.ListCreateAPIView):
    '''
    Набор представлений для управления заказами через REST API.

    Представляет GET и POST действия для заказов.
    В том числе возможность поиска заказа по номеру стола или статуса заказа.
    '''
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['table_number', 'status']


class OrderDetailAPIView(generics.RetrieveDestroyAPIView):
    '''
    Набор представлений для управления заказами через REST API.

    Представляет GET и DELETE действия для заказов.
    '''
    queryset = Order.objects.all()
    serializer_class = OrderSerializer