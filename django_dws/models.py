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

    def __str__(self):
        return self.customer_name


class Location(models.Model):
    location_id = models.CharField(max_length=255, primary_key=True)
    location_name = models.CharField(max_length=255)
    tax_rate = models.FloatField(null=True)
    opened_date = models.DateTimeField(null=True)

    class Meta:
        db_table = 'locations'


    def __str__(self):
        return self.location_name
