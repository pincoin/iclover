from django.urls import path
from . import views
app_name = 'design'

urlpatterns = [

    path('', views.HomeView.as_view(), name='home'),
    path('product/', views.ProductView.as_view(), name='product'),
    path('product/get_price/', views.AjaxPriceView.as_view(), name='get_price'),
    path('product_sample/', views.ProductSampleView.as_view(), name='product_sample'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('cart/checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('orders/', views.OrdersView.as_view(), name='orders'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('faq/', views.FaqView.as_view(), name='faq'),
    path('notice/', views.NewsView.as_view(), name='news'),
    path('order_list/', views.OrderListView.as_view(), name='order_list'),
    path('my_page/', views.MyPageView.as_view(), name='my_page'),

]