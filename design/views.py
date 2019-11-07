import json
import random
import re
import uuid as uuid_id
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
from managing import models as managing_model, viewmixin
import logging
from . import forms
from managing import forms as managing_forms
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

product_json_dic = {
    "flyer":"합판 전단지","card":"명함","envelope":"봉투","banner":"배너","ticket":"상품권","roll":"현수막/족자",
    "real":"실사 출력","octopus":"합판 문어발","moon":"문고리","sticker":"스티커", "ncr":"NCR지","ncr2":"양식지",
    "magnet":"종이자석","etc":"기타 인쇄","postit":"포스트잇/떡메모지","advertising":"판촉/홍보","bee":"비품"
 }

class Login(generic.FormView):
    template_name = 'design/login.html'
    form_class = managing_forms.LoginForm

    def form_valid(self, form):
        redirect_to = self.request.GET.get('next', '')
        if not redirect_to:
            redirect_to = self.request.META.get('HTTP_REFERER')
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user:
            django_login(self.request, user)
            if 'design/login/' in redirect_to:
                return redirect('design:home')
            return redirect(redirect_to)
        else:
            messages.error(self.request, 'ID 또는 암호를 다시 확인해주세요')
            return redirect('design:login')


    def get_context_data(self, **kwargs):
        context = super(Login, self).get_context_data(**kwargs)
        return context


def logout(request):
    django_logout(request)
    redirect_to = request.META.get('HTTP_REFERER')
    return redirect(redirect_to)


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
    model = design_model.MainImg
    def get_queryset(self):
        self.mod = design_model.MainImg.objects.filter(state_at=0)
        queryset = super().get_queryset().filter(state_at=1, name__icontains='전단지').order_by('-id')
        return queryset

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        try:
            num = random.randrange(0, 3)
            context['main_img'] = self.mod[num].banner_img.url
        except:
            pass
        return context

class HomeImageAPI(APIView):
    def get(self, request, format=None):
        keyword = request.GET.get('keyword')
        if keyword:
            back_dic = design_model.MainImg.objects.filter(state_at=1, kind=keyword).order_by('-id').values('name','banner_img','origin_url')
            print(back_dic)
            if back_dic:
                return Response(back_dic)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return  Response(status=status.HTTP_400_BAD_REQUEST)

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

        if product_category in product_json_dic:
            context['item'] = product_json_dic[product_category]

        return context

    def form_valid(self, form):
        print('forms',form)
        return self


class ProductSampleView(viewmixin.PageableMixin, ProfileMixin, generic.FormView, generic.ListView):
    template_name = 'design/product_sample.html'
    context_object_name = 'sample_list'
    paginate_by = 5
    form_class = forms.ProductForm

    def get_queryset(self):
        product_category = self.request.GET.get('item')
        sector_category = self.request.GET.get('sector')
        return managing_model.Sample.objects.select_related( 'sectors_category__parent').order_by( '-created').filter(state=True)

    def get_context_data(self, **kwargs):
        context = super(ProductSampleView, self).get_context_data(**kwargs)
        product_category = self.request.GET.get('item')
        sector_category = self.request.GET.get('sector')
        context['item'] = product_category
        if self.request.user.is_authenticated:
            cart = design_model.CartProduct.objects.filter(user=self.request.user)
            cart_button_list = []
            num = 0
            for i in cart:
                text = json.loads(i.json_text)
                name = text['title']+" "+ text['size']
                if '단면' in text['side']:
                    front = name + " 앞"
                    data = [num, front]
                    cart_button_list.append(data)
                elif '양면' in text['side']:
                    front = name + " 앞"
                    back = name + " 뒤"
                    data = [num, front]
                    cart_button_list.append(data)
                    num += 1
                    data = [num, back]
                    cart_button_list.append(data)
                num += 1
            context['cart_button_list'] = cart_button_list
        return context

    def form_valid(self, form):
        print('forms',form)
        return self

class ProductConfirmView(viewmixin.DeliveryMixin, ProfileMixin, generic.FormView, generic.ListView):
    template_name = 'design/product_confirm.html'
    context_object_name = 'confirm_list'
    form_class = forms.OrderProfileForm
    success_url = ''

    def get_queryset(self):
        product_category = self.request.GET.get('item')
        sector_category = self.request.GET.get('sector')
        return managing_model.Sample.objects.select_related( 'sectors_category__parent').filter(state=True)

    def get_context_data(self, **kwargs):
        context = super(ProductConfirmView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            customer_profile = member_model.CustomerProfile.objects.get(user=self.request.user)
            form = self.form_class(instance=customer_profile)  # get_or_create 는 신규 생성인지 boolean 튜플 제공
            context['form'] = form
        product_category = self.request.GET.get('item')
        sector_category = self.request.GET.get('sector')
        context['item'] = product_category
        # context['menu_slug']= self.kwargs['menu_slug']
        # context['sector_slug'] = self.kwargs['sector_slug']
        return context

    def form_valid(self, form):
        self.success_url = self.request.META.get('HTTP_REFERER')
        form.save(commit=False)
        # 금액 검수
        price_model = design_model.ProductPriceAPI.objects.all()
        i = design_model.CartProduct.objects.values('json_text')
        success_list = []
        error_list = []
        print(len(i))
        for i in i:
            d = json.loads(i['json_text'])
            model_model = price_model.filter(size=d['size'],paper=d['paper'],side=d['side'],deal=d['deal'])
            price = 0
            if not model_model:
                error_list.append(d)
            for i in model_model:
                price = i.sell
                d['buy_price'] = float(i.buy_price)
                if i.supplier:
                    d['supplier'] = i.supplier
                else:
                    d['supplier'] = ''
            price2 = float(d['price'])/float(d['amount'])
            if price2 == price:
                success_list.append(d)
            else:
                error_list.append(d)
                design_model.CartPriceProblem.objects.create(user=self.request.user,json_text=d)
        if error_list:
            messages.error(self.request, '예상 금액에 이상이 감지되었습니다. 관리자에게 문의주세요')
            return redirect(self.success_url)
        if not success_list:
            messages.error(self.request, '주문서가 비어있습니다.')
            return redirect(self.success_url)

        # order_info
        uuid = uuid_id.uuid4().hex[:10]
        user = self.request.user
        dic = form.cleaned_data
        dic['user'] = user
        dic['uuid'] = uuid
        if dic['address']:
            im_user = member_model.CustomerProfile.objects.filter(user=self.request.user, address__icontains= dic['address'])
            if not im_user:
                dic['address_confirm'] = False
        else:
            return redirect(self.success_url)

        data_model = design_model.CustomerOrderInfo.objects.create(**dic)
        # order_product
        for data in success_list:
            data['customer_order_info'] = data_model
            data['name'] = data['size'] + ' ' + data['paper'] + ' ' + data['deal']
            data['sell'] = float(data.pop('price'))/float(data['amount'])
            delivery = data.pop('delivery')
            design_model.CustomerOrderProduct.objects.create(**data)
            # 매입가 추가해야함
            if delivery:
                delivery_p, count, origin_delivery = self.check(self.request, data)
                delivery_dic = {'title': '선불택배비', 'kind': 'delivery', 'name': '선불택배비', 'sell': origin_delivery,
                                'buy_price': origin_delivery,'amount': count, 'customer_order_info': data_model,
                                'supplier':data['supplier'], 'size':'','paper':'','side':'','deal':''
                                }
                design_model.CustomerOrderProduct.objects.create(**delivery_dic)

        # clean_cart_product
        cart = design_model.CartProduct.objects.filter(user=self.request.user)
        cart.delete()

        return redirect('design:order_list')


class ProfileView(ProfileMixin,generic.TemplateView):
    template_name = 'design/profile.html'

class FaqView(ProfileMixin,generic.TemplateView):
    template_name = 'design/faq.html'

class NewsView(ProfileMixin,generic.TemplateView):
    template_name = 'design/news.html'

class OrderListView(viewmixin.PageableMixin,ProfileMixin, generic.ListView):
    template_name = 'design/order_list.html'
    model = design_model.CustomerOrderInfo
    context_object_name = 'order_list'
    paginate_by = 10

    def get_queryset(self):
        num = [6, 7, 8]
        print(self.request.user)
        if self.request.user.is_authenticated:
            queryset = super().get_queryset().prefetch_related('customer_order_product')\
                .filter(Q(user=self.request.user) & ~Q(state__in=num)).order_by('-joo_date','-id')
        else:
            queryset = ''
        return queryset

    def get_context_data(self, **kwargs):
        context = super(OrderListView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            for z in context['order_list']:
                data = z.customer_order_product.all()
                name = ''
                total = 0
                count = 0
                for x in data:
                    if count == 0:
                        if x.name:
                            name = x.name
                        else:
                            name = ''
                        z.title = x.title
                    pri =  x.sell * x.amount
                    if z.tax_bool:
                        total += round(pri + round(pri/10))
                    else:
                        total += pri
                    count += 1
                z.total = total
                if count == 0:
                    z.product = '내역이 없습니다.'
                elif count == 1:
                    z.product = name
                else:
                    z.product = name +' 외 '+ str(count-1)+' 건'
        return context

class JoinView(ProfileMixin, generic.FormView):
    template_name = 'design/join.html'
    form_class = forms.CreateUserForm
    success_url = "/design/join/"

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        user = User.objects.create_user(username=username, password=password)
        if user:
            django_login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('/design/my_page/')
        response = super(JoinView, self).form_valid(form)
        return response

class MyPageView(ProfileMixin, generic.FormView):
    template_name = 'design/my_page.html'
    context_object_name = 'my_list'
    form_class = forms.CustomerProfileForm

    def get_context_data(self, **kwargs):
        context = super(MyPageView, self).get_context_data(**kwargs)
        user = self.request.user.id
        if user:
            customer_profile = member_model.CustomerProfile.objects.get_or_create(user=self.request.user)
            managing_model.CustomerMemo.objects.get_or_create(customer=self.request.user)
            form = self.form_class(instance=customer_profile[0]) # get_or_create 는 신규 생성인지 boolean 튜플 제공
            context['form'] = form
            password_form = PasswordChangeForm(self.request.user)
            password_form.fields['old_password'].widget.attrs['class'] = 'form-control'
            password_form.fields['new_password1'].widget.attrs['class'] = 'form-control'
            password_form.fields['new_password2'].widget.attrs['class'] = 'form-control'
            context['password_form'] = password_form
        return context

    def form_valid(self, form):
        redirect_to = self.request.META.get('HTTP_REFERER')
        data = form.cleaned_data
        data_model = member_model.CustomerProfile.objects.get(user=self.request.user)
        for attr, value in data.items():
            setattr(data_model, attr, value)
        data_model.save()
        return redirect(redirect_to)

class AjaxPriceView(viewmixin.DeliveryMixin, APIView):

    def post(self, request, format=None):
        serializer = serializers.PaymentSerializer(data=request.data)
        if serializer.is_valid():
            size= str(serializer.data['size'])
            paper = str(serializer.data['paper'])
            side = str(serializer.data['side'])
            deal = str(serializer.data['deal'])
            img_models = design_model.ProductImg.objects.all()
            size_img = img_models.filter(name = size)
            paper_img = img_models.filter(name = paper)
            data = design_model.ProductPriceAPI.objects.filter(size=size,paper=paper,side=side,deal=deal)
            sell = [i.sell for i in data]
            if sell:
                price = sell
            else:
                price = 0
            if size_img:
                size_img = [i.images.url for i in size_img]
            if paper_img:
                paper_img = [i.images.url for i in paper_img]

            delivery,count,origin_delivery = self.check(request, serializer)
            back_dic = {
                'sell_price':price,
                'size_img':size_img,
                'paper_img':paper_img,
                'delivery': delivery
            }
            return Response(back_dic)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartProductView(APIView):
    def get(self, request, format=None):
        print(request)
        back_dic = design_model.CartProduct.objects.filter(user=self.request.user).values('id','json_text')
        if back_dic:
            return Response(back_dic)
        else:
            return Response()

    def post(self, request, format=None):
        serializer = serializers.CartProductSerializer(data=request.data)
        if serializer.is_valid():
            text = str(json.dumps(serializer.data, ensure_ascii=False))
            new = design_model.CartProduct.objects.create(user=self.request.user, json_text=text)
            new_dic ={
                'id':new.id,
                'json_text':text
            }
            return Response(new_dic)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        if request.data['num']:
            data_id = request.data['num']
            query = design_model.CartProduct.objects.get(id=data_id, user=request.user)
            if query:
                query.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class SampleListView(viewmixin.PageableMixin, viewmixin.DataSearchFormMixin,
                       generic.ListView):
    template_name = 'design/sample_list.html'
    paginate_by = 10
    model = managing_model.Sample
    data_search_form = managing_forms.DataSearchForm
    context_object_name = 'sample_list'

    def get_queryset(self):
        queryset = super().get_queryset().order_by( '-created').filter(state=True)
        form = self.data_search_form(self.request.GET)
        if form.is_valid() and form.cleaned_data['q']:
            q = form.cleaned_data['q']
            if q:
                try:
                    q = q.split()
                    for i in q:
                        queryset = queryset.filter(
                            Q(name__icontains=i) | Q(keyword__icontains=i)
                        )
                except:
                    pass
        return queryset

    def get_context_data(self, **kwargs):
        context = super(SampleListView, self).get_context_data(**kwargs)
        # if self.request.COOKIES:
        #     print(self.request.COOKIES)

        return context


class CustomerOrderListView(APIView):
    def get(self, request, format=None):
        if 'invoice_id' in request.GET:
            uuid = request.GET.get('invoice_id')
            info = design_model.CustomerOrderInfo.objects.prefetch_related('customer_order_product').get(user=self.request.user,uuid= uuid)
            back_dic = info.customer_order_product.all().values('name','amount','sell')
            if info.tax_bool:
                for i in back_dic:
                    i['nums']= 0
            if back_dic:
                return Response(back_dic)
            else:
                return Response()



