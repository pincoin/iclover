from django.urls import path
from .views import Main, Customer, Product

urlpatterns = [
    path('', Main.as_view(), name='main'),
    path('customer', Customer.as_view(), name='customer'),
    path('product', Product.as_view(), name='product'),

]