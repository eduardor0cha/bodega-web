from django.urls import path
from app_bodega_web import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login, name="login-page"),
    path("cadastrar/", views.signup, name="signup-page"),
    path("produto/<str:slug>", views.productPage, name="product-page"),
    path("carrinho/", views.cartPage, name="cart-page"),
    path("carrinho/remover", views.cartRemove, name="cart-remove"),
    path("comprar/", views.buyProduct, name="buy-product"),
    path("compra-finalizada/", views.finalizeThePurchase,
         name="finalized-purchase"),
    path("gerenciamento/", views.homeManagement, name="management"),
    path("gerenciamento/deletar-produto/<str:id>",
         views.deleteProduct, name="delete-product"),
    path("gerenciamento/editar-produto/<str:id>",
         views.editProduct, name="edit-product"),
    path("gerenciamento/criar-produto/",
         views.createProduct, name="create-product"),
]
