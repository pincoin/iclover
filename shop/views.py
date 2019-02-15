from django.views.generic import TemplateView


class Home(TemplateView):
    template_name = 'shop/home.html'

class Product(TemplateView):
    template_name = 'shop/product.html'
