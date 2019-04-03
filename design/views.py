from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import TemplateView,ListView, View
from django.http import HttpResponse
from mptt.querysets import TreeQuerySet
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from . import models
import logging

class Home(ListView):
    template_name = 'design/home.html'
    def get_queryset(self):
        return models.Profile.objects.all()


    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['data'] = 'hihihihi'
        context['session'] = self.request.user.id
        return context





class Product(TemplateView):
    template_name = 'design/product.html'

class Cart(TemplateView):
    template_name = 'design/cart.html'

class Checkout(TemplateView):
    template_name = 'design/checkout.html'

class Orders(TemplateView):
    template_name = 'design/orders.html'
#
class Profile(TemplateView):
    template_name = 'design/profile.html'



def testpage(request):
    profile = OrderImg.objects.select_related('order_list__order_info__profile__user','order_list__order_info__employees__user').order_by('id')
    # profile = ([i for i in profile])
    # category = Category.objects.all()
    # category = TreeQuerySet(model=Category)
    # i = '<br>'.join([ i.title for i in category])
    context = {'profile':profile}
    return render(request, 'design/test.html',context)
