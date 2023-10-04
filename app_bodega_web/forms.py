from django import forms

from app_bodega_web.models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "value", "discount",
                  "description", "category", "imageUrl", "stock"]
