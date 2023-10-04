import json
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from app_bodega_web.forms import ProductForm

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
        products = Product.objects.all()
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


def cartPage(request):
    return render(request, "user/cart.html")


def buyProduct(request):
    if (request.method == "POST"):
        body = json.loads(request.body)
        print(body)

    try:
        return render(request, "user/buy.html", {"product": None})
    except:
        return render(request, "user/buy.html", {"product": None})


def finalizeThePurchase(request):

    return HttpResponseRedirect("/carrinho")


def homeManagement(request):
    searchFor = request.GET.get('buscar-por')

    products = []

    if (searchFor == None):
        products = Product.objects.all().order_by("name").values()
    else:
        products = Product.objects.filter(
            name__icontains=searchFor).order_by("name").values()

    return render(request, "management/home.html", {"products": products, "searchFor": searchFor or ""})


def deleteProduct(request, id):
    Product.objects.get(id=id).delete()

    return HttpResponseRedirect("/gerenciamento")


def editProduct(request, id):
    product = Product.objects.get(id=id)

    if (request.method == "GET"):
        form = ProductForm(instance=product)

        return render(request, "management/edit-product.html", {"product": product, "form": form})
    elif (request.method == "POST"):
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()

        return HttpResponseRedirect("/gerenciamento")


def createProduct(request):
    if (request.method == "GET"):
        form = ProductForm()

        return render(request, "management/add-product.html", {"form": form})
    elif (request.method == "POST"):
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()

        return HttpResponseRedirect("/gerenciamento")


def getProducts(request):
    if (request.method == "POST"):
        products = []
        body = json.loads(request.body.decode('utf-8'))
        for productId in body["productIds"]:
            try:
                product = Product.objects.get(pk=productId)
                products.append({
                    "id": product.id,
                    "name": product.name,
                    "value": product.value,
                    "discount": product.discount,
                    "stock": product.stock,
                    "description": product.description,
                    "category": product.category,
                    "imageUrl": product.imageUrl,
                    "createdAt": product.createdAt,
                    "updatedAt": product.updatedAt
                })
            except:
                pass

        return JsonResponse({"products": products})
