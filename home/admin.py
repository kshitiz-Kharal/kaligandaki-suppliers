from django.contrib import admin
from home.models import Contact, Product, OrderUpdate, Order
# Register your models here.

admin.site.register(Contact)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderUpdate)
