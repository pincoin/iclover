from django.urls import path
from .views import HomeView, ProductView, CartView, CheckoutView, OrdersView, ProfileView, testpage
app_name = 'design'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('product/<slug:menu_slug>-<slug:sector_slug>/', ProductView.as_view(), name='product'),
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/checkout/', CheckoutView.as_view(), name='checkout'),
    path('orders/', OrdersView.as_view(), name='orders'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('testpage', testpage, name='testpage'),
]