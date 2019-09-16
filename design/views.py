from django.contrib.auth import authenticate, login as django_login, logout as django_logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.views import generic, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from mptt.querysets import TreeQuerySet
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework import status
from design import serializers
from . import models as design_model
from member import models as member_model
from managing import models as managing_model
import logging
from . import forms
from managing import forms as managing_forms
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class Login(generic.FormView):
    template_name = 'design/login.html'
    form_class = managing_forms.LoginForm

    def form_valid(self, form):
        redirect_to = self.request.GET.get('next', '')
        if not redirect_to:
            redirect_to = 'design:home'
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user:
            django_login(self.request, user)
            return redirect(redirect_to)
        else:
            messages.error(self.request, 'ID 또는 암호를 다시 확인해주세요')
            return redirect('design:login')


    def get_context_data(self, **kwargs):
        context = super(Login, self).get_context_data(**kwargs)
        return context


def logout(request):
    django_logout(request)
    return redirect('design:home')


def change_password(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)  # Important!
                return redirect('design:my_page')
            else:
                messages.error(request, form.errors)
                pass
        else:
            form = PasswordChangeForm(request.user)
        return redirect('design:my_page')
    else:
        return redirect('design:login')


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

class ProductView(ProfileMixin, generic.FormView, generic.ListView):
    template_name = 'design/product.html'
    context_object_name = 'sample_list'
    form_class = forms.ProductForm

    def get_queryset(self):
        product_category = self.request.GET.get('item')
        sector_category = self.request.GET.get('sector')
        return managing_model.Sample.objects.select_related( 'sectors_category__parent').filter(state=True)

    def get_context_data(self, **kwargs):
        context = super(ProductView, self).get_context_data(**kwargs)
        product_category = self.request.GET.get('item')
        sector_category = self.request.GET.get('sector')
        dic_name = {"flyer":"전단지/족자","card":"명함","envelope":"봉투","banner":"배너"}
        if product_category in dic_name:
            context['item'] = dic_name[product_category]
        # context['menu_slug']= self.kwargs['menu_slug']
        # context['sector_slug'] = self.kwargs['sector_slug']
        return context

    def form_valid(self, form):
        print('forms',form)
        return self


class ProductSampleView(ProfileMixin, generic.FormView, generic.ListView):
    template_name = 'design/product_sample.html'
    context_object_name = 'sample_list'
    form_class = forms.ProductForm

    def get_queryset(self):
        product_category = self.request.GET.get('item')
        sector_category = self.request.GET.get('sector')
        return managing_model.Sample.objects.select_related( 'sectors_category__parent').filter(state=True)

    def get_context_data(self, **kwargs):
        context = super(ProductSampleView, self).get_context_data(**kwargs)
        product_category = self.request.GET.get('item')
        sector_category = self.request.GET.get('sector')
        context['item'] = product_category
        # context['menu_slug']= self.kwargs['menu_slug']
        # context['sector_slug'] = self.kwargs['sector_slug']
        return context

    def form_valid(self, form):
        print('forms',form)
        return self

class ProductConfirmView(ProfileMixin, generic.FormView, generic.ListView):
    template_name = 'design/product_confirm.html'
    context_object_name = 'confirm_list'
    form_class = forms.ProductForm

    def get_queryset(self):
        product_category = self.request.GET.get('item')
        sector_category = self.request.GET.get('sector')
        return managing_model.Sample.objects.select_related( 'sectors_category__parent').filter(state=True)

    def get_context_data(self, **kwargs):
        context = super(ProductConfirmView, self).get_context_data(**kwargs)
        product_category = self.request.GET.get('item')
        sector_category = self.request.GET.get('sector')
        context['item'] = product_category
        # context['menu_slug']= self.kwargs['menu_slug']
        # context['sector_slug'] = self.kwargs['sector_slug']
        return context

    def form_valid(self, form):
        print('forms',form)
        return self


class ProfileView(ProfileMixin,generic.TemplateView):
    template_name = 'design/profile.html'

class FaqView(ProfileMixin,generic.TemplateView):
    template_name = 'design/faq.html'

class NewsView(ProfileMixin,generic.TemplateView):
    template_name = 'design/news.html'

class JoinView(ProfileMixin, generic.FormView):
    template_name = 'design/join.html'
    form_class = forms.CreateUserForm
    success_url = "/design/join/"

    def form_valid(self, form):
        print(form.cleaned_data)
        response = super(JoinView, self).form_valid(form)
        return response

class MyPageView(ProfileMixin, generic.TemplateView):
    template_name = 'design/my_page.html'
    context_object_name = 'my_list'
    form_class = forms.ProfileForm

    def get_queryset(self):
        user = self.request.user.id
        return design_model.OrderList.objects.filter(order_info__user__id= user)\
            .select_related('order_info__user','order_info__user').order_by('-created')

    def get_context_data(self, **kwargs):
        context = super(MyPageView, self).get_context_data(**kwargs)
        pk = self.request.user.id
        form = forms.ProfileForm()
        if self.request.user:
            password_form = PasswordChangeForm(self.request.user)
            password_form.fields['old_password'].widget.attrs['class'] = 'form-control'
            password_form.fields['new_password1'].widget.attrs['class'] = 'form-control'
            password_form.fields['new_password2'].widget.attrs['class'] = 'form-control'
            context['password_form'] = password_form
        context['form'] = form
        return context

class AjaxPriceView(APIView):
    def post(self, request, format=None):
        serializer = serializers.PaymentSerializer(data=request.data)
        if serializer.is_valid():
            size= request.data['size']
            paper = request.data['paper']
            side = request.data['side']
            deal = request.data['deal']
            img_models = design_model.ProductImg.objects.all()
            size_img = img_models.filter(name__icontains = size)
            if size_img:
                size_img = [i.images.url for i in size_img]
            else:
                size_img = "default"

            back_dic = {
                'sell':'50,000',
                'size_img':size_img,
                'paper_img':'http://www.aceprinting.co.kr/skin/guide/images/goods/Goods_04_01_03.jpg'
            }
            return Response(back_dic)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
