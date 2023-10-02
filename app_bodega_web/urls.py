from django.urls import path
from app_bodega_web import views

urlpatterns = [
    path("", views.home, name="home"),
    path("produto/<str:id>", views.productPage, name="product-page"),
    path("comprar/<str:id>", views.buyProduct, name="buy-product"),
    path("finalizar-compra/<str:id>", views.finalizeThePurchase,
         name="finalize-the-purchase")
]
