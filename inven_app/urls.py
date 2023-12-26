from django.urls import path
from . import views

urlpatterns = [
    path('orders/save/', views.create_purchase_order, name='new-purchase-order'),
    path('orders/new/', views.get_add_purchase_order_form, name='new-purchase-order-form'),
    path('orders/', views.get_all_purchase_order_template, name='purchase-orders'),
    path('order-list/', views.get_all_purchase_response, name='purchase-order-list'),
    path('orders/<int:order_number>/', views.get_purchase_order_details, name='single-purchase-order'),
    path('orders/<int:order_number>/edit/', views.edit_purchase_order, name='edit-purchase-order'),
    path('orders/<int:order_number>/delete/', views.delete_purchase_order, name='delete-purchase-order'),
    
]