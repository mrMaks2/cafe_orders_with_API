from django.urls import path
from . import views
from .views import OrderListAPIView, OrderDetailAPIView

app_name = 'orders'

urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('add_order/', views.add_order, name='add_order'),
    path('delete_order/', views.delete_order, name='delete_order'),
    path('search_order/', views.search_order, name='search_order'),
    path('change_status', views.change_status, name='change_status'),
    path('revenue_report/', views.revenue_report, name='revenue_report'),
    path('api/orders/', OrderListAPIView.as_view(), name='order-list-api'),
    path('api/orders/<int:pk>/', OrderDetailAPIView.as_view(), name='order-detail-api'),
]
