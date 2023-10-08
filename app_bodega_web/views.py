import json
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from app_bodega_web.forms import CustomUserCreationForm, LoginForm, ProductForm, RegisterForm
from django.contrib.auth import logout, login as djangoLogin, authenticate
from django.contrib import messages
from django.contrib.auth.models import User


from app_bodega_web.models import Address, Product

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


def signin(request):
    if (request.method == "POST"):
        form = RegisterForm(request.POST)

        userAlreadyExists = User.objects.filter(
            email=form.data["email"]).exists()

        if not userAlreadyExists:
            if (form.is_valid()):
                createUserForm = CustomUserCreationForm({
                    "username": form.data["username"],
                    "email": form.data["email"],
                    "password1": form.data["password1"],
                    "password2": form.data["password2"]
                })

                if (createUserForm.is_valid()):
                    user = createUserForm.save()

                    address = Address(user=user, state=form.data["state"], city=form.data["city"],
                                      district=form.data["district"], street=form.data["street"], number=form.data["number"])
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
        return render(request, "user/signin.html", {"form": form})
    else:
        if (request.user.is_authenticated):
            return redirect("/")

        form = RegisterForm()

        return render(request, "user/signin.html", {"form": form})


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
            products = sorted(products, key=lambda x: x.value *
                              x.discount, reverse=True)

        return render(request, "user/home.html", {"products": products, "searchFor": searchFor or "", "selectedCategory": selectedCategory, "selectedCategoryLabel": selectedCategoryLabel, "isCategoryValid": isCategoryValid})


def productPage(request, slug):
    try:
        product = Product.objects.get(slug=slug)
        return render(request, "user/product.html", {"product": product})
    except:
        return render(request, "user/product.html", {"product": None})


# --- Views exclusivas para usuários logados

def cartPage(request):
    if not (request.user.is_authenticated):
        return redirect("/login")

    return render(request, "user/cart.html")


def buyProduct(request):
    if not (request.user.is_authenticated):
        return redirect("/login")

    if (request.method == "POST"):
        body = json.loads(request.body)

    try:
        return render(request, "user/buy.html", {"product": None})
    except:
        return render(request, "user/buy.html", {"product": None})


def finalizeThePurchase(request):
    if not (request.user.is_authenticated):
        return redirect("/login")

    return HttpResponseRedirect("/carrinho")

# --- Views privadas ---


def homeManagement(request):
    if not (request.user.is_staff):
        return redirect("/")

    searchFor = request.GET.get('buscar-por')

    products = []

    if (searchFor == None):
        products = Product.objects.all().order_by("name").values()
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
