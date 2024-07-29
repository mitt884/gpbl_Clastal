from django.contrib import admin
from .models import ShippingAddress
from accounts.models import User
from orders.models import Order, OrderItems
# Register your models here.

admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItems)

#Create an OrderItem Inline for admin view
class OrderItemInline(admin.StackedInline):
    model = OrderItems
    extra = 0
    
#Extend the Order model
class OrderAdmin(admin.ModelAdmin):
    model = Order
    readonly_fields = ["date_ordered"]
    inlines = [OrderItemInline]

admin.site.unregister(Order)

admin.site.register(Order, OrderAdmin)
