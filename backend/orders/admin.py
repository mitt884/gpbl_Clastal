from django.contrib import admin
from orders.models import Order, OrderItems

admin.site.register(Order)
admin.site.register(OrderItems)
