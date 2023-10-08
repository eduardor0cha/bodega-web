from django.contrib import admin

# Register your models here.

from .models import Address, Product

admin.site.register(Product)
admin.site.register(Address)
