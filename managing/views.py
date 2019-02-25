from django.shortcuts import render
from django.views.generic import TemplateView

class Main(TemplateView):
    template_name = 'managing/main.html'

class Customer(TemplateView):
    template_name = 'managing/customer.html'

class Product(TemplateView):
    template_name = 'managing/product.html'

class Sample(TemplateView):
    template_name = 'managing/sample.html'

class Category(TemplateView):
    template_name = 'managing/category.html'

class Discount(TemplateView):
    template_name = 'managing/discount.html'

class Deal_list(TemplateView):
    template_name = 'managing/deal_list.html'

class Demand(TemplateView):
    template_name = 'managing/demand.html'