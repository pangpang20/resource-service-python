from django.contrib import admin
from .models import Customer, Location,OrderItem,Order,Product,Supply

admin.site.register(Customer)
admin.site.register(Location)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Product)
admin.site.register(Supply)
