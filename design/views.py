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

class Checkout2(TemplateView):
    template_name = 'design/checkout2.html'

class Checkout3(TemplateView):
    template_name = 'design/checkout3.html'

class Checkout4(TemplateView):
    template_name = 'design/checkout4.html'

class Checkout5(TemplateView):
    template_name = 'design/checkout5.html'
