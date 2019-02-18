from django.urls import path
from .views import Home, Product, Cart
from .views import Checkout,  Checkout2, Checkout3,  Checkout4, Checkout5
urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('product/', Product.as_view(), name='product'),
    path('cart/', Cart.as_view(), name='cart'),
    path('cart/checkout/', Checkout.as_view(), name='checkout'),
    path('cart/checkout2/', Checkout2.as_view(), name='checkout2'),
    path('cart/checkout3/', Checkout3.as_view(), name='checkout3'),
    path('cart/checkout4/', Checkout4.as_view(), name='checkout4'),
    path('cart/checkout5/', Checkout5.as_view(), name='checkout5'),
]