import json
from django.forms import formset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from app_bodega_web.forms import CustomUserCreationForm, LoginForm, ProductAndAmountForm, ProductForm, RegisterForm
from django.contrib.auth import logout, login as djangoLogin, authenticate
from django.contrib import messages
from django.contrib.auth.models import User


from app_bodega_web.models import Address, CartItem, Product

# --- Views públicas ---


def login(request):
    if (request.method == "POST"):
        form = LoginForm(request.POST)

        if (form.is_valid()):
            user = authenticate(
                request, username=form.data["username"], password=form.data["password"])

            if (user != None):
                djangoLogin(request, user)
                return redirect("/")
            else:
                messages.warning(request, "Usuário ou senha incorreto(s).")
        else:
            messages.warning(request, "Formulário inválido.")

        return render(request, "user/login.html", {"form": form})
    else:
        if (request.user.is_authenticated):
            return redirect("/")

        form = LoginForm()

        return render(request, "user/login.html", {"form": form})


def signup(request):
    if (request.method == "POST"):
        form = RegisterForm(request.POST)

        userAlreadyExists = User.objects.filter(
            email=form.data["email"]).exists()

        if not userAlreadyExists:
            if (form.is_valid()):
                createUserForm = CustomUserCreationForm({
                    "username": form.cleaned_data["username"],
                    "email": form.cleaned_data["email"],
                    "password1": form.cleaned_data["password1"],
                    "password2": form.cleaned_data["password2"]
                })

                if (createUserForm.is_valid()):
                    user = createUserForm.save()

                    address = Address(user=user, state=form.cleaned_data["state"], city=form.cleaned_data["city"],
                                      district=form.cleaned_data["district"], street=form.cleaned_data["street"], number=form.cleaned_data["number"])
                    address.save()
                    messages.info(
                        request, "Cadastrado com sucesso! Realize o login.")
                    loginForm = LoginForm()

                    return render(request, "user/login.html", {"form": loginForm})
                else:
                    for error in createUserForm.errors.items():
                        for msg in error[1]:
                            messages.warning(request, msg)
            else:
                messages.warning(request, "Formulário inválido.")
        else:
            messages.warning(request, "Esse e-mail já está em uso.")
        return render(request, "user/signup.html", {"form": form})
    else:
        if (request.user.is_authenticated):
            return redirect("/")

        form = RegisterForm()

        return render(request, "user/signup.html", {"form": form})


def home(request):
    if (request.method == "POST"):
        logout(request)
        return redirect('/')
    else:
        searchFor = request.GET.get('buscar-por')
        selectedCategory = request.GET.get('categoria')

        selectedCategory = "" if (
            selectedCategory == None) else selectedCategory

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
            list1 = list(filter(lambda x: (x.value * x.discount) !=
                         0, products))
            list1.sort(key=lambda x: x.value * x.discount, reverse=True)
            list2 = list(filter(lambda x: (x.value * x.discount) ==
                         0, products))
            list2.sort(key=lambda x: x.name)
            products = list1 + list2

        return render(request, "user/home.html", {"products": products, "searchFor": searchFor or "", "selectedCategory": selectedCategory, "selectedCategoryLabel": selectedCategoryLabel, "isCategoryValid": isCategoryValid})


def productPage(request, slug):
    try:
        product = Product.objects.get(slug=slug)

        ProductAndAmountFormset = formset_factory(ProductAndAmountForm)

        formset = ProductAndAmountFormset(data={
            "form-TOTAL_FORMS": '1',
            'form-INITIAL_FORMS': '0',
            "form-0-productId": product.id,
            "form-0-amount": 1
        })

        return render(request, "user/product.html", {"product": product, "formset": formset})
    except:
        return render(request, "user/product.html", {"product": None})


# --- Views exclusivas para usuários logados

def cartPage(request):
    if not (request.user.is_authenticated):
        return redirect("/login")

    ProductAndAmountFormset = formset_factory(ProductAndAmountForm)

    cartItems = CartItem.objects.filter(user=request.user)

    data = {
        "form-TOTAL_FORMS": f'{len(cartItems)}',
        'form-INITIAL_FORMS': f'{len(cartItems)}',
    }

    for i, cartItem in enumerate(cartItems):
        data[f"form-{i}-productId"] = cartItem.product.id
        data[f"form-{i}-amount"] = cartItem.amount

    formset = ProductAndAmountFormset(data=data)

    if (formset.is_valid()):
        items = []
        for form in formset.forms:
            if (form.is_valid()):
                try:
                    product = Product.objects.get(
                        id=form.cleaned_data["productId"])
                    items.append({
                        "product": product,
                        "amount": form.cleaned_data["amount"]
                    })
                except:
                    pass

        total = sum((item["product"].value - (item["product"].value *
                    item["product"].discount)) * item["amount"] for item in items)

        return render(request, "user/cart.html", {"formset": formset, "items": items or [], "total": total})

    return redirect("/")


def buyProduct(request):
    if not (request.user.is_authenticated):
        return redirect("/login")

    if (request.method == "POST"):
        if ("buy-product" in request.POST):
            ProductAndAmountFormset = formset_factory(ProductAndAmountForm)

            formset = ProductAndAmountFormset(request.POST)

            if (formset.is_valid()):
                items = []
                for form in formset.forms:
                    if (form.is_valid()):
                        try:
                            product = Product.objects.get(
                                id=form.cleaned_data["productId"])

                            if (product.stock < form.cleaned_data["amount"]):
                                messages.warning(
                                    request, "Quantidade maior que o estoque.")
                                return redirect(f"/produto/{product.slug}")

                            items.append({
                                "product": product,
                                "amount": form.cleaned_data["amount"]
                            })
                        except:
                            pass

                address = {}
                try:
                    address = Address.objects.get(user=request.user)
                except:
                    pass

                total = sum((item["product"].value - (item["product"].value *
                            item["product"].discount)) * item["amount"] for item in items)

                return render(request, "user/buy.html", {"formset": formset, "items": items, "address": address, "total": total, "formset": formset})
        else:
            ProductAndAmountFormset = formset_factory(ProductAndAmountForm)

            formset = ProductAndAmountFormset(request.POST)

            if (formset.is_valid()):
                for form in formset.forms:
                    if (form.is_valid()):
                        try:
                            product = Product.objects.get(
                                id=form.cleaned_data["productId"])

                            if (product.stock < form.cleaned_data["amount"]):
                                messages.warning(
                                    request, "Quantidade maior que o estoque.")
                                return redirect(f"/produto/{product.slug}")

                            cartItem = CartItem.objects.filter(
                                product=product, user=request.user)
                            cartItem.delete()

                            cartItem = CartItem(
                                user=request.user, product=product, amount=form.cleaned_data["amount"])
                            cartItem.save()
                        except:
                            pass

                return redirect("/carrinho")
    else:
        return redirect("/")


def cartRemove(request):
    if not (request.user.is_authenticated):
        return redirect("/login")

    if (request.method == "POST"):
        product = Product.objects.get(
            id=request.POST["productId"])

        cartItem = CartItem.objects.filter(
            product=product, user=request.user)
        cartItem.delete()

    return redirect("/carrinho")


def finalizeThePurchase(request):
    if not (request.user.is_authenticated):
        return redirect("/login")

    if (request.method == "POST"):
        ProductAndAmountFormset = formset_factory(ProductAndAmountForm)

        formset = ProductAndAmountFormset(request.POST)

        if (formset.is_valid()):
            for form in formset.forms:
                if (form.is_valid()):
                    try:
                        product = Product.objects.get(
                            id=form.cleaned_data["productId"])

                        if (product.stock < form.cleaned_data["amount"]):
                            messages.warning(
                                request, "Quantidade maior que o estoque.")
                            return redirect(f"/produto/{product.slug}")

                        product.stock -= form.cleaned_data["amount"]
                        product.save()

                        cartItem = CartItem.objects.get(
                            product=product, user=request.user)
                        cartItem.delete()
                    except:
                        return render(request, "user/failed-purchase.html")

            return render(request, "user/finalized-purchase.html")
        else:
            return redirect("/")
    else:
        return redirect("/")

# --- Views privadas ---


def homeManagement(request):
    if not (request.user.is_staff):
        return redirect("/")

    searchFor = request.GET.get('buscar-por')

    products = []

    if (searchFor == None):
        products = Product.objects.all().order_by("stock").values()
    else:
        products = Product.objects.filter(
            name__icontains=searchFor).order_by("name").values()

    return render(request, "management/home.html", {"products": products, "searchFor": searchFor or ""})


def deleteProduct(request, id):
    if not (request.user.is_staff):
        return redirect("/")

    Product.objects.get(id=id).delete()

    return HttpResponseRedirect("/gerenciamento")


def editProduct(request, id):
    if not (request.user.is_staff):
        return redirect("/")

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
    if not (request.user.is_staff):
        return redirect("/")

    if (request.method == "GET"):
        form = ProductForm()

        return render(request, "management/add-product.html", {"form": form})
    elif (request.method == "POST"):
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()

        return HttpResponseRedirect("/gerenciamento")
