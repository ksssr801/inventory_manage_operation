from django.urls import include, path, re_path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('orders/new/', views.create_purchase_order, name='new-purchase-order'),
    path('orders/', views.get_all_purchase_orders, name='purchase-orders'),
    path('orders/<int:order_number>/', views.get_purchase_order_details, name='single-purchase-order'),
    path('orders/<int:order_number>/edit/', views.edit_purchase_order, name='edit-purchase-order'),
    path('orders/<int:order_number>/delete/', views.delete_purchase_order, name='delete-purchase-order'),
    
]