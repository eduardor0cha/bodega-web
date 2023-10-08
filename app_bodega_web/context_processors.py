from app_bodega_web.models import Product


def addVariableToContext(request):
    return {
        'productCategories': Product.CATEGORY_CHOICES,
        'loggedUser': request.user if (request.user.is_authenticated) else None
    }
