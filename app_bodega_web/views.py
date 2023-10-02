from django.http import HttpResponseRedirect
from django.shortcuts import render

from app_bodega_web.models import Product

# Create your views here.


def home(request):
    searchFor = request.GET.get('buscar-por')
    selectedCategory = request.GET.get('categoria')

    selectedCategory = "" if (selectedCategory == None) else selectedCategory

    selectedCategoryLabel = ""
    isCategoryValid = True
    if not (selectedCategory in (c[0] for c in Product.CATEGORY_CHOICES)) and (selectedCategory != ""):
        isCategoryValid = False
    elif selectedCategory != "":
        for c in Product.CATEGORY_CHOICES:
            if (c[0] == selectedCategory):
                selectedCategoryLabel = c[1]
                break

    products = []

    if (searchFor == None):
        products = Product.objects.filter(discount__gt=0)
    else:
        products = Product.objects.filter(name__icontains=searchFor)

    if (selectedCategory != ""):
        products = products.filter(
            category__exact=selectedCategory)

    if (len(products) != 0):
        products = sorted(products, key=lambda x: x.value *
                          x.discount, reverse=True)

    return render(request, "user/home.html", {"products": products, "searchFor": searchFor or "", "selectedCategory": selectedCategory, "selectedCategoryLabel": selectedCategoryLabel, "isCategoryValid": isCategoryValid})


def productPage(request, id):
    try:
        product = Product.objects.get(id=id)
        return render(request, "user/product.html", {"product": product})
    except:
        return render(request, "user/product.html", {"product": None})


def buyProduct(request, id):
    try:
        product = Product.objects.get(id=id)
        return render(request, "user/buy.html", {"product": product})
    except:
        return render(request, "user/buy.html", {"product": None})


def finalizeThePurchase(request, id):
    try:
        product = Product.objects.get(id=id)

        if (product.stock != 0):
            product.stock -= 1

        print(product)

        product.save()

        return HttpResponseRedirect("/compra-finalizada")
    except:
        return HttpResponseRedirect("/compra-finalizada")
