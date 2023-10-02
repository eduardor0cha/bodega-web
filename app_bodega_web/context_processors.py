from app_bodega_web.models import Product


def addVariableToContext(request):
    return {
        'productCategories': Product.CATEGORY_CHOICES,
    }
