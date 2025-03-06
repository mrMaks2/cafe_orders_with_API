from django.db.models import Sum
from django.db.transaction import commit
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Order
from .forms import *

def order_list(request):
    orders = Order.objects.all()
    return render(request, 'order_list.html', {'orders': orders})

def add_order(request):
    """Создает новый заказ."""
    if request.method == 'POST':
        table_number = request.POST['table_number']
        items = request.POST.get('items')
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
            return redirect('orders:add_order.html')
    form = OrderAddForm()
    return render(request, 'add_order.html', {'form': form})

def delete_order(request):
    if request.method == 'POST':
        order_id = request.POST['order']
        order = Order.objects.get(id = order_id)
        order.delete()
        messages.success(request,'Заказ успешно удален')
        return redirect('orders:order_list')
    form = OrderDeleteForm()
    return render(request, 'delete_order.html', {'form': form})

def search_order(request):
    if request.method == 'POST':
        query = request.POST['order']
        if query.isdigit():
            orders = Order.objects.filter(table_number = query)
            return render(request, 'order_list.html', {'orders': orders})
        else:
            orders = Order.objects.filter(status = query)
            return render(request, 'order_list.html', {'orders': orders})
    form = OrderSearchForm()
    return render(request, 'search_order.html', {'form': form})


def change_status(request):
    if request.method == 'POST':
        order_id = request.POST['order']
        order = Order.objects.get(id=order_id)
        order.status = request.POST['new_status']
        if order:
            order.save()
            messages.success(request,'Статус заказа успешно изменен')
            return redirect('orders:order_list')
        else:
            messages.error(request, 'Такого заказа не существует')
            return redirect('orders:change_status.html')
    form = OrderChangeStatusForm()
    return render(request, 'change_status.html', {'form': form})

def revenue_report(request):
    total_revenue = Order.objects.filter(status='paid').aggregate(Sum('total_price'))['total_price__sum'] or 0
    return render(request, 'revenue_report.html', {'total_revenue': total_revenue})