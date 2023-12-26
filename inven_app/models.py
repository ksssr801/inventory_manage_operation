from django.db import models
from sumtracker_proj.base_models import BaseModel
from django.db.models.deletion import CASCADE

class Supplier(BaseModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=254, default="")
    email = models.EmailField(max_length=100, blank=False, default=None)
    
    class Meta:
        db_table = 'tbl_supplier'
    
class PurchaseOrder(BaseModel):
    order_number = models.AutoField(primary_key=True)
    supplier = models.ForeignKey(Supplier, db_column='supplier_id', related_name='supplier_ref',on_delete=CASCADE, default=None)
    order_time = models.DateTimeField(auto_now_add=True)
    total_quantity = models.IntegerField()
    total_amount = models.DecimalField(max_digits=20, decimal_places=4)
    total_tax = models.DecimalField(max_digits=20, decimal_places=4)

    class Meta:
        db_table = 'tbl_purchase_order'
    
class LineItem(BaseModel):
    id = models.AutoField(primary_key=True)
    item_name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    price_without_tax = models.DecimalField(max_digits=20, decimal_places=4)
    tax_name = models.CharField(max_length=255)
    tax_amount = models.DecimalField(max_digits=20, decimal_places=4)
    line_total = models.DecimalField(max_digits=20, decimal_places=4)
    purchase_order = models.ForeignKey(PurchaseOrder, db_column='purchase_order_id', related_name='purchase_order_ref', on_delete=CASCADE, default=None)

    class Meta:
        db_table = 'tbl_line_items'
