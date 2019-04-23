from django.urls import path
from . import views

app_name = 'managing'

urlpatterns = [
    path('', views.Main.as_view(), name='main'),
    path('customer/', views.CustomerView.as_view(), name='customer'),
    path('customer/create/', views.CustomerCreateView.as_view(), name='customer_create'),
    path('customer/<int:pk>/update/', views.CustomerUpdateView.as_view(), name='customer_update'),
    path('product/', views.ProductView.as_view(), name='product'),
    path('product/create/', views.ProdcutCreateView.as_view(), name='product_create'),
    path('product/<int:pk>/update/', views.ProductUpdateView.as_view(), name='product_update'),
    path('sample/', views.SampleView.as_view(), name='sample'),
    path('category/', views.CategoryView.as_view(), name='category'),
    path('discount/', views.DiscountView.as_view(), name='discount'),
    path('deal_list/', views.Deal_listView.as_view(), name='deal_list'),
    path('demand/', views.DemandView.as_view(), name='demand'),


]