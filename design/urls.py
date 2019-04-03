from django.urls import path
from .views import Home, Product, Cart, Checkout, Orders, Profile, testpage


urlpatterns = [
    path('', Home.as_view(), name='design/home'),
    path('product/', Product.as_view(), name='design/product'),
    path('cart/', Cart.as_view(), name='design/cart'),
    path('cart/checkout/', Checkout.as_view(), name='design/checkout'),
    path('orders/', Orders.as_view(), name='design/orders'),
    path('profile/', Profile.as_view(), name='design/profile'),
    path('testpage', testpage, name='testpage'),
]