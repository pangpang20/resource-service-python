from django.db import models


class Customer(models.Model):
    customer_id = models.CharField(max_length=255, primary_key=True)
    customer_name = models.CharField(max_length=255)
    count_lifetime_orders = models.BigIntegerField(null=True)
    first_ordered_at = models.DateTimeField(null=True)
    last_ordered_at = models.DateTimeField(null=True)
    lifetime_spend_pretax = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    lifetime_tax_paid = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    lifetime_spend = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    customer_type = models.CharField(max_length=255)

    class Meta:
        db_table = 'customers'


class Location(models.Model):
    location_id = models.CharField(max_length=255, primary_key=True)
    location_name = models.CharField(max_length=255)
    tax_rate = models.FloatField(null=True)
    opened_date = models.DateTimeField(null=True)

    class Meta:
        db_table = 'locations'



class OrderItem(models.Model):
    order_item_id = models.CharField(max_length=255, primary_key=True)
    order_id = models.CharField(max_length=255)
    product_id = models.CharField(max_length=255)
    ordered_at = models.DateTimeField()
    product_name = models.CharField(max_length=255)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_food_item = models.BooleanField()
    is_drink_item = models.BooleanField()
    supply_cost = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'order_items'

class Order(models.Model):
    order_id = models.CharField(max_length=255, primary_key=True)
    location_id = models.CharField(max_length=255)
    customer_id = models.CharField(max_length=255)
    subtotal_cents = models.IntegerField()
    tax_paid_cents = models.IntegerField()
    order_total_cents = models.IntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    tax_paid = models.DecimalField(max_digits=10, decimal_places=2)
    order_total = models.DecimalField(max_digits=10, decimal_places=2)
    ordered_at = models.DateTimeField()
    order_cost = models.DecimalField(max_digits=10, decimal_places=2)
    order_items_subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    count_food_items = models.BigIntegerField()
    count_drink_items = models.BigIntegerField()
    count_order_items = models.BigIntegerField()
    is_food_order = models.BooleanField()
    is_drink_order = models.BooleanField()
    customer_order_number = models.BigIntegerField()

    class Meta:
        db_table = 'orders'

class Product(models.Model):
    product_id = models.CharField(max_length=255, primary_key=True)
    product_name = models.CharField(max_length=255)
    product_type = models.CharField(max_length=255)
    product_description = models.TextField()
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_food_item = models.BooleanField()
    is_drink_item = models.BooleanField()

    class Meta:
        db_table = 'products'


class Supply(models.Model):
    supply_uuid = models.CharField(max_length=255, primary_key=True)
    supply_id = models.CharField(max_length=255)
    product_id = models.CharField(max_length=255)
    supply_name = models.CharField(max_length=255)
    supply_cost = models.DecimalField(max_digits=10, decimal_places=2)
    is_perishable_supply = models.BooleanField()

    class Meta:
        db_table = 'supplies'
