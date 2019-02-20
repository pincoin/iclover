from django.shortcuts import render
from django.views.generic import TemplateView

class Main(TemplateView):
    template_name = 'managing/main.html'

class Customer(TemplateView):
    template_name = 'managing/customer.html'

class Product(TemplateView):
    template_name = 'managing/product.html'

