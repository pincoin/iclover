from django.shortcuts import render, HttpResponseRedirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from mptt.querysets import TreeQuerySet
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from . import models as design_model
from member import models as member_model
from managing import models as managing_model
import logging
from . import forms

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
            user = member_model.Profile.objects.select_related('user').filter(user=user_id)
            for i in user:
                context['user'] = i.user
                if i.company:
                    context['company'] = i.company
                else:
                    context['company'] = i.user
                context['staff'] = i.user.is_staff
            session = self.request.session
            context['session'] = session
        return context


class HomeView(ProfileMixin, generic.ListView):
    template_name = 'design/home.html'
    def get_queryset(self):
        return

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        return context

class ProductView(ProfileMixin, generic.ListView):
    template_name = 'design/product.html'
    context_object_name = 'sample_list'

    def get_queryset(self):
        return managing_model.Sample.objects.select_related( 'sectors_category__parent')

    def get_context_data(self, **kwargs):
        context = super(ProductView, self).get_context_data(**kwargs)
        # context['menu_slug']= self.kwargs['menu_slug']
        # context['sector_slug'] = self.kwargs['sector_slug']
        return context

class CartView(generic.TemplateView):
    template_name = 'design/cart.html'

class CheckoutView(generic.TemplateView):
    template_name = 'design/checkout.html'

class OrdersView(ProfileMixin, generic.ListView):
    template_name = 'design/orders.html'

    def get_context_data(self, **kwargs):
        context = super(OrdersView, self).get_context_data(**kwargs)
        return context
#
class ProfileView(ProfileMixin,generic.TemplateView):
    template_name = 'design/profile.html'

class FaqView(ProfileMixin,generic.TemplateView):
    template_name = 'design/faq.html'

class NewsView(ProfileMixin,generic.TemplateView):
    template_name = 'design/news.html'

class OrderListView(ProfileMixin, generic.ListView):
    template_name = 'design/order_list.html'
    context_object_name = 'order_list'
    form_class =forms.LoginForm

    def post(self, *args, **kwargs):
        if self.request.POST:
            form = forms.LoginForm(self.request.POST)
            username = self.request.POST['login']
            password = self.request.POST['password']
        return form

    def get_queryset(self):
        user = self.request.user.id
        return design_model.OrderList.objects.filter(order_info__user__id= user).select_related('order_info__user','order_info__user').order_by('-created')

    def get_context_data(self, **kwargs):
        form = forms.LoginForm()
        context = super(OrderListView, self).get_context_data(**kwargs)
        print(form)
        context['form'] = form
        return context

class MyPageView(ProfileMixin, generic.TemplateView):
    template_name = 'design/my_page.html'
    context_object_name = 'my_list'
    form_class = forms.ProfileForm

    def get_queryset(self):
        user = self.request.user.id
        return design_model.OrderList.objects.filter(order_info__user__id= user).select_related('order_info__user','order_info__user').order_by('-created')

    def get_context_data(self, **kwargs):
        pk = self.request.user.id
        form = forms.ProfileForm()
        context = super(MyPageView, self).get_context_data(**kwargs)
        print(form)
        context['form'] = form
        return context

