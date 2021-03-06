from django.urls import path
from . import views
app_name = 'design'

urlpatterns = [

    path('', views.HomeView.as_view(), name='home'),
    path('home_image/', views.HomeImageAPI.as_view(), name='home_image'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.logout, name='logout'),
    path('password_change/', views.change_password, name='change_password'),
    path('product/', views.ProductView.as_view(), name='product'),
    path('cart/', views.CartProductView.as_view(), name='cart'),
    path('product/get_price/', views.AjaxPriceView.as_view(), name='get_price'),
    path('product_sample/', views.ProductSampleView.as_view(), name='product_sample'),
    path('product_confirm/', views.ProductConfirmView.as_view(), name='product_confirm'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('join/', views.JoinView.as_view(), name='join'),
    path('sample/', views.SampleListView.as_view(), name='sample'),
    path('sample_api/', views.SampleAPIView.as_view(), name='sample_api'),
    path('faq/', views.FaqView.as_view(), name='faq'),
    path('notice/', views.NewsView.as_view(), name='news'),
    path('order_list/', views.OrderListView.as_view(), name='order_list'),
    path('order_list/detail/', views.CustomerOrderListView.as_view(), name='order_list_detail'),
    path('my_page/', views.MyPageView.as_view(), name='my_page'),

]