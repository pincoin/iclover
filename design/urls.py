from django.urls import path
from .views import HomeView, ProductView, CartView, CheckoutView, OrdersView, ProfileView, \
    FaqView , NewsView, OrderListView, MyPageView
app_name = 'design'

urlpatterns = [

    path('', HomeView.as_view(), name='home'),
    path('product/', ProductView.as_view(), name='product'),
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/checkout/', CheckoutView.as_view(), name='checkout'),
    path('orders/', OrdersView.as_view(), name='orders'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('faq/', FaqView.as_view(), name='faq'),
    path('notice/', NewsView.as_view(), name='news'),
    path('order_list/', OrderListView.as_view(), name='order_list'),
    path('my_page/', MyPageView.as_view(), name='my_page'),
]