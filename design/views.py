from django.shortcuts import render
from django.views.generic import TemplateView

class Home(TemplateView):
    template_name = 'design/home.html'

class Product(TemplateView):
    template_name = 'design/product.html'

class Cart(TemplateView):
    template_name = 'design/cart.html'

class Checkout(TemplateView):
    template_name = 'design/checkout.html'

class Orders(TemplateView):
    template_name = 'design/orders.html'

class Profile(TemplateView):
    template_name = 'design/profile.html'