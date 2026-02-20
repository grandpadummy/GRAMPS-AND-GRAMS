from django.contrib import admin

from .models import OrderItem, ShippingAddress, Order
from django.contrib.auth.models import User

# Register the model on the admin section

admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)

# Create an OrderItem Inline

class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0

# Extend our OrderModel

class OrderAdmin(admin.ModelAdmin):
    model = Order
    readonly_fields = ['date_ordered']
    fields = ['user', 'full_name', 'email', 'shipping_address1', 'amount_paid', 'date_ordered', 'shipped', 'date_shipped']
    inlines = [OrderItemInline]

# Unregister Order Model
admin.site.unregister(Order)

# Reregister Order And OrderAdmin

admin.site.register(Order, OrderAdmin)


