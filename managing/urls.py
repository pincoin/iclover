from django.urls import path
from .views import Main, Customer, Product, Sample, Category, Discount, Deal_list

urlpatterns = [
    path('', Main.as_view(), name='managing/main'),
    path('customer', Customer.as_view(), name='managing/customer'),
    path('product', Product.as_view(), name='managing/product'),
    path('sample', Sample.as_view(), name='managing/sample'),
    path('category', Category.as_view(), name='managing/category'),
    path('discount', Discount.as_view(), name='managing/discount'),
    path('deal_list', Deal_list.as_view(), name='managing/deal_list'),
]