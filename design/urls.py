from django.urls import path
from .views import Home, Product, Cart, Checkout, Orders, Profile

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('product/', Product.as_view(), name='product'),
    path('cart/', Cart.as_view(), name='cart'),
    path('cart/checkout/', Checkout.as_view(), name='checkout'),
    path('orders/', Orders.as_view(), name='orders'),
    path('profile/', Profile.as_view(), name='profile'),
]