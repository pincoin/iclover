from django.urls import path
from .views import Home, Product

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('product/', Product.as_view(), name='product'),
]