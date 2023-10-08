from django.urls import path
from app_bodega_web import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login, name="login-page"),
    path("cadastrar/", views.signin, name="signin-page"),
    path("produto/<str:slug>", views.productPage, name="product-page"),
    path("carrinho/", views.cartPage, name="cart-page"),
    path("comprar/", views.buyProduct, name="buy-product"),
    path("finalizar-compra/", views.finalizeThePurchase,
         name="finalize-the-purchase"),
    path("gerenciamento/", views.homeManagement, name="management"),
    path("gerenciamento/deletar-produto/<str:id>",
         views.deleteProduct, name="delete-product"),
    path("gerenciamento/editar-produto/<str:id>",
         views.editProduct, name="edit-product"),
    path("gerenciamento/criar-produto/",
         views.createProduct, name="create-product"),
]
