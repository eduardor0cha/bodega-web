from django.contrib import admin

# Register your models here.

from .models import Address, CartItem, Product

admin.site.register(Product)
admin.site.register(Address)
admin.site.register(CartItem)
