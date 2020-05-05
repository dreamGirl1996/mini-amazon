from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class AmazonUser(models.Model):
    person = models.OneToOneField(User, on_delete=models.CASCADE)
    ups_name = models.IntegerField( null=True, blank=True,help_text="Ups username")#tracking num
    ups_pass = models.CharField(max_length=50, null=True, blank=True,help_text="Ups password")#paswword

    def __str__(self):
        return self.person.username



class Warehouse(models.Model):
    wh_id = models.AutoField(primary_key=True)
    wh_x = models.IntegerField(help_text='Warehouse address X', validators=[MinValueValidator(0), MaxValueValidator(360)],
                            null=True, blank=False)
    wh_y = models.IntegerField(help_text="Warehouse_address Y", validators=[MinValueValidator(0), MaxValueValidator(360)],
                            null=True, blank=False)

class AmazonProduct(models.Model):
    prod_id = models.AutoField(primary_key=True)
    product_name = models.CharField(help_text="Product name", max_length=50, null=True, blank=False)
    product_desc = models.CharField(help_text="Product description", max_length=50, null=True, blank=True)

    def __str__(self):
        return self.product_name

    class Meta:
        ordering = ['product_name']


class Order(models.Model):
    ship_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order_user', null=True, blank=True)#1 order to 1 user, 1 user has many orders
    #item_id = models.ForeignKey(AmazonProduct, on_delete=models.SET_NULL, related_name='order_item', null=True, blank=True)
    product_name = models.CharField(help_text="Product name", max_length=50, null=True, blank=False)#no shopping chart
    packed_wh = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='packed_wh', null=True,
                                blank=True)  # 1 order to 1 user, 1 user has many orders
    ups_id = models.CharField(help_text='Ups account',max_length=30, null=True, blank=True)
    truck_id = models.IntegerField(help_text='truck this shipment goes on', null=True, blank=True)
    buyer_x = models.IntegerField(help_text='User address X', validators=[MinValueValidator(0), MaxValueValidator(360)],
                            null=True, blank=False)
    buyer_y = models.IntegerField(help_text='User address Y', validators=[MinValueValidator(0), MaxValueValidator(360)],
                            null=True, blank=False)
    order_created_time = models.DateTimeField(help_text='Order created time', default=timezone.now, null=True, blank=True)
    product_num= models.IntegerField(help_text='How many products you want to buy?', default=1, null=True, blank=False,validators=[MinValueValidator(0)])
    STATUS = (
        ('await_valid','await_valid'),
        ('val_req_sent','val_req_sent'),
        ('invalid','invalid'),
        ('pending', 'pending'),
        ('to pack', 'to pack'),
        ("ready", "ready"),
        ("request_pickup","request_pickup"),
        ("request_noted","request_noted"),
        ("load", "load"),
        ("loaded", "loaded"),
        ("delivering", "delivering"),
        ("delivered", "delivered"),
    )

    status = models.CharField(max_length=20, choices=STATUS, default='pending',help_text='Order status')
    def __str__(self):
        return self.user_id.username



class WarehouseContents(models.Model):
    wh_id = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='warehouse',
                                     null=True, blank=True, default=1)
    prod_id = models.ForeignKey(AmazonProduct, on_delete=models.CASCADE, related_name='product',
                              null=True, blank=True, default=1)
    product_quantity = models.IntegerField(help_text="Quantity", validators=[MinValueValidator(0)],
                                   default=1, null=True, blank=False)
