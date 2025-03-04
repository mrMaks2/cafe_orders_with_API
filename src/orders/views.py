from django.shortcuts import render, redirect, get_object_or_404
from .models import Order

def order_list(request):
    orders = Order.objects.all()
    return render(request, 'orders/order_list.html', {'orders': orders})

def add_order(request):
    if request.method == 'POST':
        table_number = request.POST['table_number']
        items = request.POST.getlist('items')
        items_with_prices = [
            {
                'name': item.split(':')[0],
                'price': float(item.split(':')[1])
             } for item in items
        ]
        order = Order(table_number = table_number, items = items_with_prices)
        order.save()
        return redirect('order_list')
    return render(request, 'orders/add_order.html')

def delete_order(request, order_id=None):
    if request.method == 'POST':
        order = get_object_or_404(Order, id = order_id)
        order.delete()
        return redirect('order_list')
    return render(request, 'orders/delete_order.html')

def search_orders(request):
    query = request.GET.get('q')
    if query:
        orders = Order.objects.filter(table_number = query) | Order.objects.filter(status = query)
        return render(request, 'orders/order_list.html', {'orders': orders})
    return render(request, 'orders/search_order.html')


def change_status(request, order_id):
    order = Order.objects.get(id = order_id)
    if request.method == 'POST':
        order.status = request.POST['status']
        order.save()
        return redirect('order_list')
    return render(request, 'orders/change_status.html', {'order': order})