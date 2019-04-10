from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import TemplateView,ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from mptt.querysets import TreeQuerySet
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from . import models
import logging

# class PageableMixin(object):
#     logger = logging.getLogger(__name__)
#
#     def get_context_data(self, **kwargs):
#         context = super(PageableMixin, self).get_context_data(**kwargs)
#
#         start_index = int((context['page_obj'].number - 1) / self.block_size) * self.block_size
#         end_index = min(start_index + self.block_size, len(context['paginator'].page_range))
#
#         context['page_range'] = context['paginator'].page_range[start_index:end_index]
#         return context
#
#     def get_paginate_by(self, queryset):
#         return self.chunk_size

class ProfileMixin(object):

    def get_context_data(self, **kwargs):
        context = super(ProfileMixin, self).get_context_data(**kwargs)
        user_id = self.request.user.id
        if user_id:
            user = models.Profile.objects.select_related('user').filter(user=user_id)
            for i in user:
                context['user'] = i.user
                if i.company:
                    context['company'] = i.company
                else:
                    context['company'] = i.user
                context['staff'] = i.user.is_staff
            session = self.request.session
            context['session'] = session
        print('ProfileMixin')
        return context


class HomeView(ProfileMixin, ListView):
    template_name = 'design/home.html'
    def get_queryset(self):
        return

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        return context

class ProductView(ProfileMixin, ListView):
    template_name = 'design/product.html'
    context_object_name = 'sample_list'

    def get_queryset(self):
        return models.Sample.objects.select_related( 'employees__user','sectors_category__parent')


    def get_context_data(self, **kwargs):
        context = super(ProductView, self).get_context_data(**kwargs)
        context['menu_slug']= self.kwargs['menu_slug']
        context['sector_slug'] = self.kwargs['sector_slug']


        return context

class CartView(TemplateView):
    template_name = 'design/cart.html'

class CheckoutView(TemplateView):
    template_name = 'design/checkout.html'

class OrdersView(ProfileMixin, TemplateView):
    template_name = 'design/orders.html'

    def get_context_data(self, **kwargs):
        context = super(OrdersView, self).get_context_data(**kwargs)
        return context
#
class ProfileView(TemplateView):
    template_name = 'design/profile.html'



def testpage(request):
    profile = models.OrderImg.objects.select_related('order_list__order_info__profile__user','order_list__order_info__employees__user').order_by('id')
    # profile = ([i for i in profile])
    # category = Category.objects.all()
    # category = TreeQuerySet(model=Category)
    # i = '<br>'.join([ i.title for i in category])
    context = {'profile':profile}
    return render(request, 'design/test.html',context)
