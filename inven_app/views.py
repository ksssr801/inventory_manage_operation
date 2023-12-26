from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from django.forms.models import model_to_dict
from rest_framework import status
from rest_framework.response import Response
from drf_spectacular.utils import (
    extend_schema,
)
from drf_spectacular.types import OpenApiTypes
import json

from .models import *
from .serializers import *


@extend_schema(
    request=PurchaseOrderSerializer,
    description="This endpoint is used to add purchase order.",
    summary="Add a new purchase order.",
    responses=OpenApiTypes.OBJECT,
)
@api_view(("POST",))
def create_purchase_order(request):
    try:
        print ("## create_purchase_order function ##")
        supplier_name = str(request.POST.get('supplier_name', ''))
        supplier_email = str(request.POST.get('supplier_email', ''))
        line_items = json.loads(request.POST.get('line_item_data', []))
        
        new_supplier_obj = None
        new_purchase_order_obj = None
        new_line_item_obj = None
        
        try:
            new_supplier_obj = Supplier(**{
                'name': supplier_name, 
                'email': supplier_email
                })
            new_supplier_obj.save()
        except Exception as e:
            print ("Error in creating new supplier: " + str(e))
            
        
        try:
            new_purchase_order_obj = PurchaseOrder(**{
                'supplier': new_supplier_obj,
                'total_quantity': 1,
                'total_amount': 10.50,
                'total_tax': 0.50
                })
            new_purchase_order_obj.save()
        except Exception as e:
            print ("Error in creating new purchase order: " + str(e))
        
        try:
            for line_item in line_items: 
                price_without_tax = float(line_item.get('price_without_tax', 0))
                tax_amount = float(line_item.get('tax_amount', 0))
                new_line_item_obj = LineItem(**{
                    'purchase_order': new_purchase_order_obj, 
                    'item_name': str(line_item.get('item_name', '')),
                    'quantity': int(line_item.get('quantity', '')),
                    'tax_name': str(line_item.get('tax_name', '')),
                    'price_without_tax': price_without_tax,
                    'tax_amount': tax_amount,
                    'line_total': price_without_tax + tax_amount,
                    })
                print ("new_line_item_obj : ", new_line_item_obj)
                new_line_item_obj.save()
        except Exception as e:
            print ("Error in creating new line item: " + str(e))
        
        return redirect('/purchase/orders/')
    except Exception as e:
        print ("e : ", e)
    
def get_add_purchase_order_form(request):
    try:
        print ("## get_add_purchase_order_form function ##")        
        return render(request, 'create_purchase_order.html', context={ 'msg': '' })
    except Exception as e:
        pass

def get_all_purchase_order_template(request):
    try:
        print ("## get_all_purchase_order_template ##")
        purchase_orders = PurchaseOrder.objects.filter(is_deleted=False).select_related('supplier').prefetch_related('purchase_order_ref').all()
        
        result = [] 
        for order in purchase_orders:
            purchase_order_dict = model_to_dict(order)
            purchase_order_dict['supplier'] = model_to_dict(order.supplier)

            line_item_dict_list = []
            for line_item in order.purchase_order_ref.all():
                line_item_dict = model_to_dict(line_item)
                line_item_dict_list.append(line_item_dict)
                
            purchase_order_dict['line_items'] = line_item_dict_list
            result.append(purchase_order_dict)
            
        return render(request, 'get_all_purchase_orders.html', context={ 'msg': '', 'purchase_orders': purchase_orders })
    except Exception as e:
        print ("e : ", e)
        return render(request, 'get_all_purchase_orders.html', context={ 'msg': 'Some error occured.' })

@extend_schema(
    request=PurchaseOrderSerializer,    
    description="This endpoint is used to get all purchase orders.",
    summary="List all purchase orders.",
    responses=OpenApiTypes.OBJECT,    
)
@api_view(("GET",))
def get_all_purchase_response(request):
    try:
        print ("## get_all_purchase_response ##")
        purchase_orders = PurchaseOrder.objects.filter(is_deleted=False).select_related('supplier').prefetch_related('purchase_order_ref').all()
        
        result = [] 
        for order in purchase_orders:
            purchase_order_dict = model_to_dict(order)
            purchase_order_dict['supplier'] = model_to_dict(order.supplier)

            line_item_dict_list = []
            for line_item in order.purchase_order_ref.all():
                line_item_dict = model_to_dict(line_item)
                line_item_dict_list.append(line_item_dict)
                
            purchase_order_dict['line_items'] = line_item_dict_list
            result.append(purchase_order_dict)
            
        return Response(result, status=status.HTTP_200_OK)
    except Exception as e:
        print ("e : ", e)
        return Response([], status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def get_purchase_order_details(request, order_number=None):
    try:
        print ("## get_purchase_order_details ##", order_number)
        purchase_order = single_purchase_order_details(order_number)
                        
        return render(request, 'get_purchase_order_details.html', context={ 'msg': '', 'purchase_order': purchase_order })
    except Exception as e:
        print ("e : ", e)
        return render(request, 'get_purchase_order_details.html', context={ 'msg': 'Some error occured.' })

def edit_purchase_order(request, order_number=None):
    try:
        print ("## edit_purchase_order ##", order_number)
        purchase_order = single_purchase_order_details(order_number)
        if request.method == 'POST':
            supplier_name = str(request.POST.get('supplier_name', ''))
            supplier_email = str(request.POST.get('supplier_email', ''))
            line_items = json.loads(request.POST.get('line_item_data', []))
            
            existing_purchase_order = PurchaseOrder.objects.get(order_number=order_number)
            try:
                Supplier.objects.filter(id=existing_purchase_order.supplier.id).update(
                    **{ 'name': supplier_name,
                    'email': supplier_email
                    }
                )
            except Exception as e:
                print ("Error in updating supplier details: ", e)
            
            try:
                LineItem.objects.filter(purchase_order=order_number).all().delete()
                for line_item in line_items: 
                    price_without_tax = float(line_item.get('price_without_tax', 0))
                    tax_amount = float(line_item.get('tax_amount', 0))
                    new_line_item_obj = LineItem(**{
                        'purchase_order': existing_purchase_order, 
                        'item_name': str(line_item.get('item_name', '')),
                        'quantity': int(line_item.get('quantity', '')),
                        'tax_name': str(line_item.get('tax_name', '')),
                        'price_without_tax': price_without_tax,
                        'tax_amount': tax_amount,
                        'line_total': price_without_tax + tax_amount,
                        })
                    new_line_item_obj.save()
                
            except Exception as e:
                print ("Error occurred while updating line item data : " + str(e))
            return redirect('/purchase/orders/%s' % order_number)
                                    
        return render(request, 'edit_purchase_order_details.html', context={ 'msg': '', 'purchase_order': purchase_order })
    except Exception as e:
        print ("e : ", e)
        return render(request, 'edit_purchase_order_details.html', context={ 'msg': 'Some error occured.' })

def delete_purchase_order(request, order_number=None):
    try:
        print ("## delete_purchase_order ##", order_number)
        purchase_order_obj = PurchaseOrder.objects.get(order_number=order_number, is_deleted=False)
        purchase_order_obj.is_deleted = True
        try:
            purchase_order_obj.save()
        except Exception as e:
            return render(request, 'get_all_purchase_orders.html', context={ 'msg': 'Some error occured.' })        
        return redirect('/purchase/orders/')
    except Exception as e:
        print ("e : ", e)
        return render(request, 'get_all_purchase_orders.html', context={ 'msg': 'Some error occured.' })

def single_purchase_order_details(order_number):
    purchase_orders = PurchaseOrder.objects.filter(order_number=order_number).select_related('supplier').prefetch_related('purchase_order_ref').all()
    
    purchase_order = {}
    if purchase_orders and purchase_orders != -1: 
        order_obj = purchase_orders[0]
        purchase_order = model_to_dict(purchase_orders[0])
        
    purchase_order['supplier'] = model_to_dict(order_obj.supplier)

    line_item_dict_list = []
    for line_item in order_obj.purchase_order_ref.all():
        line_item_dict = model_to_dict(line_item)
        line_item_dict_list.append(line_item_dict)
        
    purchase_order['line_items'] = line_item_dict_list
    return purchase_order
    