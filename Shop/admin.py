from django.contrib import admin
from .models import Product ,Order, Cart


admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Cart)



class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'total_amount', 'payment_type', 'status']

