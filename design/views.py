from django.shortcuts import render
from django.views.generic import TemplateView

class Home(TemplateView):
    template_name = 'design/home.html'

class Product(TemplateView):
    template_name = 'design/Product.html'
