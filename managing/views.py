import datetime
import re

from django.urls import reverse

from managing import log_save
from django.core import serializers as core_serializer

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login as django_login, logout as django_logout, authenticate, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import (UserPassesTestMixin,
                                        LoginRequiredMixin, PermissionRequiredMixin)
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q, Max, Min, Avg, Sum
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import generic
from rest_framework import status, viewsets
from rest_framework import generics as api_generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse, HttpResponseRedirect
from design import models as design_models
from member import models as member_models
from . import forms as managing_forms
from . import models as managing_models
from . import viewmixin
from . import serializers
import PIL

clovi_login_url = '/clovi/login/'


class Login(generic.FormView):
    template_name = 'managing/login.html'
    form_class = managing_forms.LoginForm

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_staff:
                django_login(self.request, user)
                return redirect('managing:main')
            else:
                return HttpResponse('Wemix 관리자가 아닌 경우 접근을 불허합니다.')
        else:
            return redirect('managing:main')

    def form_invalid(self, form):
        print('오휴')
        return self

    def get_context_data(self, **kwargs):
        context = super(Login, self).get_context_data(**kwargs)
        return context


def logout(request):
    django_logout(request)
    return redirect('managing:main')


def change_password(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)  # Important!
                return redirect('managing:main')
            else:
                pass
        else:
            form = PasswordChangeForm(request.user)
        return render(request, 'managing/change_password.html', {
            'form': form
        })
    else:
        return redirect('managing:login')


class Main(LoginRequiredMixin, viewmixin.PageableMixin, viewmixin.DataSearchFormMixin, generic.ListView):
    template_name = 'managing/main.html'
    context_object_name = 'memo_list'
    paginate_by = 20
    model = managing_models.Memo
    data_search_form = managing_forms.DataSearchForm
    # optional
    login_url = clovi_login_url

    def get_queryset(self):
        return managing_models.Memo.objects.order_by('-importance', '-created').filter(confirm=False)

    def get_context_data(self, **kwargs):
        state_list = [1,2,3,9] #[주문,시안,발주,배송]
        context = super(Main, self).get_context_data(**kwargs)
        context['order_list'] = design_models.OrderInfo.objects.filter(
            Q(state__in=state_list)&Q(employees=self.request.user)).select_related('user').prefetch_related('order_list')\
            .order_by('state','-joo_date')
        count = {}
        for i in context['order_list']:
            a = i.get_state_display()
            if a not in count:
                count[a] = 1
            else:
                count[a] += 1

        context['count'] = count
        context['my_list'] = []
        context['common_list'] = []
        for i in context['memo_list']:
            if i.employees == self.request.user.username:
                data = [i.pk, i.importance, i.content, self.request.user, i.common]
                context['my_list'].append(data)
            else:
                if i.common == True:
                    data = [i.pk, i.importance, i.content, i.employees]
                    context['common_list'].append(data)
        return context


class MemoCreateView(viewmixin.UserIsStaffMixin, SuccessMessageMixin, generic.CreateView):
    form_class = managing_forms.MemoCreateForm
    success_url = "/clovi/"
    # optional
    login_url = clovi_login_url

    def form_valid(self, form):
        obj = form.save(commit=False)
        common = self.request.path[-1]
        if common == "1":  # 0이면 개인메모 1 이면 공통메모
            obj.common = True
        obj.employees = self.request.user
        response = super(MemoCreateView, self).form_valid(form)
        return response

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse(dict(form.errors, is_success=False))
        return redirect('/clovi/memo/create')

    def get_template_names(self):
        if self.request.is_ajax():
            return ['managing/memo_create_form_.html']
        return ['managing/memo_create.html']

    def get_context_data(self, **kwargs):
        context = super(MemoCreateView, self).get_context_data(**kwargs)
        return context



class MemoUpdateView(SuccessMessageMixin, generic.UpdateView):
    model = managing_models.Memo
    form_class = managing_forms.MemoUpdateForm
    context_object_name = 'update_list'
    success_url = "/clovi/"
    # optional
    login_url = clovi_login_url

    def form_valid(self, form):
        response = super(MemoUpdateView, self).form_valid(form)
        log_save.UserLogs(action='수정', url=self.request.path,
                 model_id=self.kwargs['pk'], model_name=self.model.__name__
                 )
        return response

    def get_template_names(self):
        if self.request.is_ajax():
            return ['managing/memo_update_form_.html']
        return ['managing/memo_update.html']


class CustomerResultView(viewmixin.UserIsStaffMixin, viewmixin.PageableMixin, viewmixin.DataSearchFormMixin,
                         generic.ListView):
    template_name = 'managing/customer_result.html'
    context_object_name = 'result_list'
    paginate_by = 12
    model = member_models.Profile
    data_search_form = managing_forms.DataSearchForm
    # optional
    login_url = clovi_login_url

    def get_queryset(self):
        queryset = super().get_queryset().select_related('user').order_by('state_select', '-created')
        form = self.data_search_form(self.request.GET)
        if form.is_valid() and form.cleaned_data['q']:
            q = form.cleaned_data['q']
            if q:
                try:
                    q = q.split()
                    for i in q:
                        queryset = queryset.filter(
                            Q(company__icontains=i) | Q(company_keyword__icontains=i) | Q(address__icontains=i)
                            | Q(phone__icontains=i) | Q(code__icontains=i) | Q(user__username__icontains=i)
                        )
                except:
                    pass
        return queryset

    def get_context_data(self, **kwargs):
        context = super(CustomerResultView, self).get_context_data(**kwargs)
        if len(context['object_list']) == 1:
            user = ''.join([str(i.user.id) for i in context['object_list']])
            data = design_models.OrderInfo.objects.select_related('user').filter(user_id=user)
            context['analysis'] = data.aggregate(Max('joo_date'), Min('joo_date'))
        return context


class CustomerView(viewmixin.UserIsStaffMixin, viewmixin.PageableMixin, viewmixin.DataSearchFormMixin,
                   generic.ListView):
    context_object_name = 'customer_list'
    paginate_by = 10
    model = member_models.Profile
    data_search_form = managing_forms.DataSearchForm
    # optional
    login_url = clovi_login_url

    def get_queryset(self):
        queryset = super().get_queryset().select_related('user').order_by('-id')
        form = self.data_search_form(self.request.GET)
        if form.is_valid() and form.cleaned_data['q']:
            q = form.cleaned_data['q']
            if q:
                try:
                    q = q.split()
                    for i in q:
                        queryset = queryset.filter(
                            Q(company__icontains=i) | Q(company_keyword__icontains=i) | Q(address__icontains=i)
                            | Q(phone__icontains=i) | Q(code__icontains=i)
                        )
                except:
                    pass
        return queryset

    def get_context_data(self, **kwargs):
        context = super(CustomerView, self).get_context_data(**kwargs)
        return context

    def get_template_names(self):
        return ['managing/customer.html']


class CustomerCreateView(viewmixin.UserIsStaffMixin, SuccessMessageMixin, generic.CreateView):
    form_class = managing_forms.CustomerCreateForm
    success_url = "/clovi/customer"
    success_message = '%(company)s님의 정보가 신규 등록 되었습니다..'
    # optional
    login_url = clovi_login_url

    def form_valid(self, form):
        obj = form.save(commit=False)
        name = '[임시]_' + str(obj.company) + '_' + str(obj.code)
        check_is = User.objects.filter(username=name).exists()
        if check_is:
            if self.request.is_ajax():
                return JsonResponse(dict(login_error='이미 해당 사업자로 가입된 계정이 존재합니다.', is_success=False))
            return redirect('/clovi/customer/create')
        else:
            try:
                user = User.objects.create_user(username=name, password='iclover77', is_active=False)
                obj.user_id = user.id
            except:
                pass
            response = super(CustomerCreateView, self).form_valid(form)
            return response

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse(dict(form.errors, is_success=False))
        messages.error(self.request, '생성할 수 없습니다')
        return redirect('/clovi/customer/')

    def get_template_names(self):
        if self.request.is_ajax():
            return ['managing/customer_create_form_.html']
        return ['managing/customer_create.html']


class CustomerUpdateView(viewmixin.UserIsStaffMixin, SuccessMessageMixin, generic.UpdateView):
    model = member_models.Profile
    form_class = managing_forms.CustomerUpdateForm
    context_object_name = 'update_list'
    success_url = "/clovi/customer"
    success_message = '%(company)s 님의 정보가 수정되었습니다.'
    # optional
    login_url = clovi_login_url

    def get_context_data(self, **kwargs):
        context = super(CustomerUpdateView, self).get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        if self.request.is_ajax():
            self.success_url = self.request.META.get('HTTP_REFERER')
        response = super(CustomerUpdateView, self).form_valid(form)
        return response

    def get_template_names(self):
        if self.request.is_ajax():
            return ['managing/customer_update_form_.html']
        return ['managing/customer_update.html']


class ProductView(viewmixin.UserIsStaffMixin, viewmixin.PageableMixin, viewmixin.DataSearchFormMixin, generic.ListView):
    template_name = 'managing/product.html'
    context_object_name = 'product_list'
    paginate_by = 10
    model = design_models.ProductText
    data_search_form = managing_forms.DataSearchForm
    # optional
    login_url = clovi_login_url

    def get_queryset(self):
        queryset = super().get_queryset().select_related('category').prefetch_related('supplier').order_by(
           '-id', '-supplier')
        form = self.data_search_form(self.request.GET)
        if form.is_valid() and form.cleaned_data['q']:
            q = form.cleaned_data['q']
            if q:
                try:
                    q = q.split()
                    for i in q:
                        queryset = queryset.filter(
                            Q(title__icontains=i) | Q(memo__icontains=i) | Q(etc__icontains=i) | Q(
                                etc_option__icontains=i)
                            | Q(standard__icontains=i) | Q(horizontal__icontains=i) | Q(vertical__icontains=i)
                            | Q(paper__icontains=i) | Q(gram__icontains=i) | Q(paper_option__icontains=i)
                            | Q(color__icontains=i) | Q(side__icontains=i) | Q(supplier__username__icontains=i)
                        )
                except:
                    pass
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ProductView, self).get_context_data(**kwargs)
        try:
            for i in context['product_list']:
                z = i.supplier.username.split('_')
                i.company = z[1]
        except:
            pass
        return context


class ProdcutCreateView(viewmixin.UserIsStaffMixin, SuccessMessageMixin, generic.CreateView):
    form_class = managing_forms.ProductCreateForm
    template_name = 'managing/product_create.html'
    success_url = "/clovi/product"
    success_message = '%(standard)s 신규 등록 되었습니다.'
    # optional
    login_url = clovi_login_url

    def form_valid(self, form):
        response = super(ProdcutCreateView, self).form_valid(form)
        return response

    def get_queryset(self):
        queryset = super(ProdcutCreateView, self).get_queryset()
        return queryset


class ProductUpdateView(viewmixin.UserIsStaffMixin, SuccessMessageMixin, generic.UpdateView):
    model = design_models.ProductText
    form_class = managing_forms.ProductUpdateForm
    template_name = 'managing/product_update.html'
    success_url = "/clovi/product"
    success_message = '%(standard)s 정보가 수정되었습니다.'
    # optional
    login_url = clovi_login_url

    def form_valid(self, form):
        response = super(ProductUpdateView, self).form_valid(form)
        return response


class SampleView(viewmixin.UserIsStaffMixin, viewmixin.PageableMixin, viewmixin.DataSearchFormMixin, generic.ListView):
    template_name = 'managing/sample.html'
    context_object_name = 'sample_list'
    paginate_by = 10
    model = managing_models.Sample
    data_search_form = managing_forms.DataSearchForm
    # optional
    login_url = clovi_login_url

    def get_queryset(self):
        queryset = super().get_queryset().select_related('employees', 'category', 'sectors_category').order_by(
            '-created')
        form = self.data_search_form(self.request.GET)
        if form.is_valid() and form.cleaned_data['q']:
            q = form.cleaned_data['q']
            if q:
                try:
                    q = q.split()
                    for i in q:
                        queryset = queryset.filter(
                            Q(keyword__icontains=i) | Q(name__icontains=i) | Q(employees__username__icontains=i)
                            | Q(category__title__icontains=i) | Q(sectors_category__title__icontains=i)
                        )
                except:
                    pass
        return queryset

    def get_context_data(self, **kwargs):
        context = super(SampleView, self).get_context_data(**kwargs)
        return context

class SampleCreateView(viewmixin.UserIsStaffMixin, SuccessMessageMixin, generic.CreateView):
    form_class = managing_forms.SampleCreateForm
    template_name = 'managing/sample_create.html'
    success_url = "/clovi/sample"
    success_message = '샘플이 신규 등록 되었습니다.'
    # optional
    login_url = clovi_login_url

    def form_valid(self, form):
        response = super(SampleCreateView, self).form_valid(form)
        return response

    def get_queryset(self):
        queryset = super(SampleCreateView, self).get_queryset().prefetch_related('employees__user')
        return queryset


class SampleUpdateView(viewmixin.UserIsStaffMixin, SuccessMessageMixin, generic.UpdateView):
    model = managing_models.Sample
    form_class = managing_forms.SampleUpdateForm
    context_object_name = 'update_list'
    template_name = 'managing/sample_update.html'
    success_url = "/clovi/sample"
    success_message = '%(name)s 샘플이 수정되었습니다.'
    # optional
    login_url = clovi_login_url

    def form_valid(self, form):
        response = super(SampleUpdateView, self).form_valid(form)
        return response


class CategoryView(viewmixin.UserIsStaffMixin, generic.ListView):
    template_name = 'managing/category.html'
    # optional
    login_url = clovi_login_url

    def get_queryset(self):
        queryset = design_models.Category.objects.prefetch_related('children').filter(level=0)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryView, self).get_context_data(**kwargs)
        context['sector'] = design_models.SectorsCategory.objects.prefetch_related('children').filter(level=0)
        return context

class CategoryCreateView(viewmixin.UserIsStaffMixin, SuccessMessageMixin, generic.FormView):
    # optional
    login_url = clovi_login_url

    form_class = managing_forms.CategoryCreateForm
    success_url = "/clovi/category/"

    def get_context_data(self, **kwargs):
        context = super(CategoryCreateView, self).get_context_data(**kwargs)
        context['title'] = self.request.GET['title']
        return context

    def get_template_names(self):
        if self.request.is_ajax():
            return ['managing/category_create_form_.html']
        return ['managing/category_create_form_.html']

    def form_valid(self, form):
        name = form.cleaned_data['name']
        kind = self.kwargs['kind']
        level = self.kwargs['level']
        title = self.request.GET['title']
        if kind == 0:
            if level == 1:
                parent = design_models.SectorsCategory.objects._mptt_filter(title=title)
                for i in parent:
                    parent = i.id
            elif level == 0:
                parent = None
            sec_category = design_models.SectorsCategory(title=name, parent_id=parent)
            sec_category.save()
        elif kind == 1:
            if level == 1:
                parent = design_models.Category.objects.filter(title=title)
                for i in parent:
                    parent = i.id
            elif level == 0:
                parent = None
            category = design_models.Category(title=name, parent_id=parent)
            category.save()

        response = super(CategoryCreateView, self).form_valid(form)
        return response

class CategoryDeleteView(viewmixin.UserIsStaffMixin, generic.DeleteView):
    model = design_models.Category
    success_url = "/clovi/category/"

    def dispatch(self, request, *args, **kwargs):
        kind = kwargs['kind']
        level = kwargs['level']
        pk = kwargs['pk']

        def delete_f(model, pk, level):
            data = model.filter(id=pk)
            if level == 0:
                for i in data:
                    child = i.children.all()
                    child.delete()
                data.delete()
            elif level == 1:
                data.delete()

        if kind == 0: #업종 카테고리
            model = design_models.SectorsCategory.objects
            delete_f(model, pk, level)
        elif kind == 1: #품목 카테고리
            model = design_models.Category.objects
            delete_f(model, pk, level)
        return redirect('/clovi/category/')


class DiscountView(viewmixin.UserIsStaffMixin, generic.TemplateView):
    template_name = 'managing/discount.html'
    # optional
    login_url = clovi_login_url


def analysis(model , date, user):
    total = sum([i.selling_price * i.quantity for i in model])
    month_total = model.filter(order_info__order_date__range=date,
                                   order_info__employees=user)
    return
class MyPageView(viewmixin.UserIsStaffMixin, generic.TemplateView):
    template_name = 'managing/my_page.html'
    '''
    labels: [1,2,3,4,5,6,7,8,9,10,11,12],
    datasets: [{
        data: [86,114,106,106,107,111,133,221,783,2478],
        label: "Africa",
        backgroundColor: "#3e95cd",
        borderColor: "#3e95cd",
        fill: false
      }]
    '''
    # optional
    login_url = clovi_login_url

    def get_context_data(self, **kwargs):
        user =self.request.user.username
        context = super(MyPageView, self).get_context_data(**kwargs)
        today = datetime.date.today()
        oder_list = design_models.OrderList.objects.prefetch_related('order_info').filter(Q(order_info__state=4),Q(order_info__employees=user))
        data = oder_list.values('order_info__order_date','selling_price','quantity')
        data.aggregate(total_price=Sum('selling_price'))
        for i in data:
            print(i)
        # total = sum([i.selling_price * i.quantity for i in oder_list])
        # print(total)
        this_month = { 'year':today.year,'month':today.month}
        print(this_month)
        return context

class OrderListView(viewmixin.UserIsStaffMixin, viewmixin.PageableMixin, viewmixin.DataSearchFormMixin,
                    generic.ListView):
    template_name = 'managing/order.html'
    paginate_by = 10
    model = design_models.OrderInfo
    data_search_form = managing_forms.DataSearchForm

    def get_queryset(self):
        state = int(self.kwargs['common'])
        if state == 99: #단독 검색시
            queryset = super(OrderListView, self).get_queryset().select_related('user').prefetch_related(
                'order_list','order_img').filter(~Q(state=state)).order_by('-joo_date', '-today_num')
        elif state == 4:
            state_list = [0,1,2,3,4,9]
            queryset = super(OrderListView, self).get_queryset().select_related('user').prefetch_related(
                'order_list', 'order_img').filter(Q(state__in=state_list)).order_by('-joo_date', '-today_num')
        elif state == 5:
            state_list = [5,6,7]
            queryset = super(OrderListView, self).get_queryset().select_related('user').prefetch_related(
                'order_list', 'order_img').filter(Q(state__in=state_list)).order_by('-joo_date', '-today_num')
        else:
            queryset = super(OrderListView, self).get_queryset().select_related('user').prefetch_related(
                'order_list','order_img').filter(Q(state=state)).order_by('-joo_date', '-today_num')
        form = self.data_search_form(self.request.GET)
        if form.is_valid() and form.cleaned_data['q']:
            q = form.cleaned_data['q']
            match_term = re.search(r'\d{4}-\d{2}-\d{2}~\d{4}-\d{2}-\d{2}', q)
            match = re.search(r'\d{4}-\d{2}-\d{2}', q)

            if q:
                try:
                    q = q.split()
                    if match_term:
                        term_date = match_term.group()
                        q.remove(term_date)
                        term_date = term_date.split('~')
                        start_date = list(map(int, term_date[0].split('-')))
                        end_date = list(map(int, term_date[1].split('-')))
                        start_date = datetime.date(start_date[0], start_date[1], start_date[2])
                        end_date = datetime.date(end_date[0], end_date[1], end_date[2])
                        queryset = queryset.filter(joo_date__range=[start_date, end_date])

                    elif match:
                        single_date = match.group()
                        q.remove(single_date)
                        single_date = list(map(int, single_date.split('-')))
                        start_date = datetime.date(single_date[0], single_date[1], single_date[2])
                        queryset = queryset.filter(joo_date=start_date)
                    for i in q:
                        queryset = queryset.filter(
                            Q(employees__icontains=i) | Q(company__icontains=i) | Q(company_keyword__icontains=i)
                            | Q(company_keyword__icontains=i)
                        )
                except:
                    pass
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(OrderListView, self).get_context_data(**kwargs)
        for i in context['object_list']:
            orderlist = i.order_list.all()
            total_price = 0
            total_tax = 0
            count = 0
            name = ''
            for z in orderlist:
                total_price += (round(z.selling_price) *z.quantity)
                total_tax += (round(z.selling_price_tax)*z.quantity)
                if z.list_sort == 1:
                    name = z.name
                count += 1

            i.total = total_price+total_tax
            i.total_price = total_price
            i.total_tax = total_tax

            if count == 1:
                i.product = name
            elif count == 0:
                i.product = ''
            else:
                i.product = name+' 외 '+ str(count-1)+' 건'

            # i.products = name+' 외 '+ str(data[check_date][0])+'건'
            i.img_bool = i.order_img.exists()
        context['common'] = self.kwargs['common']
        return context

    # optional
    login_url = clovi_login_url


class OrdersCreateView(viewmixin.UserIsStaffMixin, SuccessMessageMixin, generic.FormView):
    form_class = managing_forms.OrderForm
    model = design_models.OrderInfo
    success_url = "/clovi/order/0/"
    success_message = '%(company)s 신규 등록 되었습니다.'

    def get_form(self, form_class=None):
        today = datetime.date.today().strftime('%Y-%m-%d')
        form = super(OrdersCreateView, self).get_form(form_class)
        form.fields['joo_date'].widget.attrs.update({'value': today})
        return form

    def get_context_data(self, **kwargs):
        context = super(OrdersCreateView, self).get_context_data(**kwargs)
        employees = User.objects.filter(is_staff=True,is_active=True).order_by('username')
        data_manager = {}
        for i in employees:
            data_manager[i.username] = i.id
        context['manager_ls'] = data_manager  # 직원이름 select
        return context

    def get_template_names(self):
        if self.request.is_ajax():
            return ['managing/order_create_form_.html']
        return ['managing/order_create.html']

    def form_valid(self, form):
        json_data = form.cleaned_data['json_data'].split('#,,#')
        json_all_num = len(json_data)
        json_tr_long = 12  # 한 tr의 td 개수
        json_pre = 0  # 인덱싱
        json_next = json_tr_long  # 인덱싱
        if json_all_num:
            product_list = []
            json_all_num = json_all_num / json_tr_long  # tr 수 찾기
            try:
                for i in range(0, int(json_all_num)):
                    product_list.append(json_data[json_pre:json_next])
                    json_pre += json_tr_long
                    json_next += json_tr_long
            except:
                messages.error(self.request, '알수없는 에러가 발생하였습니다.')
                urls = self.request.META.get('HTTP_REFERER')
                return redirect(urls)
            if product_list:
                code = int(form.cleaned_data['code'])
                user = member_models.Profile.objects.select_related('user').get(code=code)
                joo_date = form.cleaned_data['joo_date']
                state = form.cleaned_data['state']
                if state == '1' :
                    self.success_url = "/clovi/order/1/"
                today_num = design_models.OrderInfo.objects.filter(joo_date=joo_date).aggregate(Max('today_num'))
                if form.cleaned_data['order_date']:
                    order_date = form.cleaned_data['order_date']
                    state = 1
                else:
                    order_date = None
                if not today_num['today_num__max']:  # 1번을 만들기 위함
                    today_num['today_num__max'] = 0
                today_num = today_num['today_num__max'] + 1
                tax = True if form.cleaned_data['tax'] == '0' else False
                order_info = design_models.OrderInfo(
                    user=user.user,
                    today_num=today_num,
                    joo_date=joo_date,
                    company=form.cleaned_data['company'],
                    company_keyword=form.cleaned_data['company_keyword'],
                    employees=form.cleaned_data['manager'],
                    options=form.cleaned_data['option'],
                    address=form.cleaned_data['address'],
                    tell=form.cleaned_data['tell'],
                    checker=form.cleaned_data['confirm'],
                    keywords=form.cleaned_data['memo'],
                    in_memo=form.cleaned_data['in_memo'],
                    out_memo=form.cleaned_data['out_memo'],
                    fix_manager=form.cleaned_data['fix_manager'],
                    order_date=order_date,
                    state=state,
                    tax=tax,
                )
                order_info.save()
                list_sort = 1

                for product_data in product_list:
                    quantity = product_data[3].replace(',','')
                    selling_price = product_data[4].replace(',', '')
                    price = product_data[7].replace(',', '')
                    price_tax = round(float(price)/ 10)
                    if tax:
                        selling_price_tax = round(float(selling_price) / 10)
                    else:
                        selling_price_tax = 0

                    design_models.OrderList(
                        order_info_id=order_info.id,
                        list_sort= int(list_sort),
                        num= int(today_num),
                        code= int(product_data[0]),
                        name=product_data[1],
                        standard = product_data[2],
                        quantity = float(quantity),
                        selling_price=float(selling_price),
                        selling_price_tax=float(selling_price_tax),
                        price=float(price),
                        price_tax=price_tax,
                        group_manage=product_data[8],
                        gram=product_data[9],
                        etc=product_data[10],
                        memo=product_data[11],
                    ).save()
                    list_sort += 1

        if self.request.is_ajax():
            self.success_url = self.request.META.get('HTTP_REFERER')
        response = super(OrdersCreateView, self).form_valid(form)
        log_save.UserLogs(user=self.request.user.username, model_id=order_info.id, model_name=self.model.__name__, action='생성')
        return response

    def form_invalid(self, form):
        error_message = '[확인 해야할 오류 항목] \n'
        if 'company' in form.errors:
            error_message += '업체명\n'
        if 'code' in form.errors:
            error_message += '코드번호'
        if 'manager' in form.errors:
            error_message += '담당자'
        if 'json_data' in form.errors:
            error_message += '품목이 없거나 잘못되었습니다.'
        messages.error(self.request, error_message)
        urls = self.request.META.get('HTTP_REFERER')
        return redirect(urls)

    # optional
    login_url = clovi_login_url


class OrdersUpdateView(viewmixin.UserIsStaffMixin, SuccessMessageMixin, generic.FormView):
    form_class = managing_forms.OrderForm
    model = design_models.OrderInfo
    success_url = "/clovi/order/0/"
    success_message = '%(company)s 수정 되었습니다.'

    def get_form(self, form_class=None):
        url_pk = self.kwargs['pk']
        self.queryset = design_models.OrderInfo.objects.select_related('user').prefetch_related('order_list','user__profile').filter(
            id=url_pk)
        form = super(OrdersUpdateView, self).get_form(form_class)
        for i in self.queryset:
            form.fields['joo_date'].widget.attrs.update({'value': i.joo_date})
            if i.order_date:
                form.fields['order_date'].widget.attrs.update({'value': i.order_date})
            if i.company:
                form.fields['company'].widget.attrs.update({'value': i.company})
            if i.company_keyword:
                form.fields['company_keyword'].widget.attrs.update({'value': i.company_keyword})
            if i.address:
                form.fields['address'].widget.attrs.update({'value': i.address})
            if i.tell:
                form.fields['tell'].widget.attrs.update({'value': i.tell})
            try:
                if i.user.profile.code:
                    form.fields['code'].widget.attrs.update({'value': i.user.profile.code})
            except:
                pass
            if i.fix_manager:
                form.fields['fix_manager'].widget.attrs.update({'value': i.fix_manager})
            if i.checker:
                form.fields['confirm'].widget.attrs.update({'value': i.checker})
            if i.options:
                form.fields['option'].widget.attrs.update({'value': i.options})
            if i.keywords:
                form.fields['memo'].initial = i.keywords
            if i.employees:
                form.fields['manager'].initial = i.employees
            if i.state:
                form.fields['state'].initial = i.state
            if i.in_memo:
                form.fields['in_memo'].widget.attrs.update({'value': i.in_memo})
            if i.out_memo:
                form.fields['out_memo'].widget.attrs.update({'value': i.out_memo})

            form.fields['tax'].widget.attrs.update({'value': i.tax})
        return form

    def get_context_data(self, **kwargs):
        context = super(OrdersUpdateView, self).get_context_data(**kwargs)
        for i in self.queryset:
            context['order_list'] = i.order_list.all()
            context['put_employees'] = i.employees
            context['tax'] = i.tax
            context['put_today_num'] = i.today_num
            context['put_joo_date'] = i.joo_date
            try:
                context['put_code'] = i.user.profile.code
                context['put_company'] = i.user.profile.company.strip()
                context['put_company_keyword'] = i.user.profile.company_keyword.strip()
                context['put_address'] = i.user.profile.address.strip()
                context['put_tax_bill_mail'] = i.user.profile.tax_bill_mail.strip()
                context['put_tell'] = i.user.profile.tell.strip()
                context['put_phone'] = i.user.profile.phone.strip()
                context['put_keywords'] = i.user.profile.keywords.strip()
                context['put_memo'] = i.user.profile.memo.strip()
                context['put_options'] = i.user.profile.options.strip()
                context['put_confirm'] = i.user.profile.confirm.strip()
                context['put_manager'] = i.user.profile.manager.strip()
            except:
                pass

        employees = User.objects.filter(is_staff=True, is_active=True).order_by('username')
        data_manager = {}
        for i in employees:
            data_manager[i.username] = i.id
        context['manager_ls'] = data_manager  # 직원이름 select
        return context

    def get_template_names(self):
        if self.request.is_ajax():
            return ['managing/order_update_form_.html']
        return ['managing/order_create.html']

    def form_valid(self, form):
        context_data = self.get_context_data()
        json_data = form.cleaned_data['json_data'].split('#,,#')
        json_all_num = len(json_data)
        json_tr_long = 12  # 한 tr의 td 개수
        json_pre = 0  # 인덱싱
        json_next = json_tr_long  # 인덱싱
        if json_all_num:
            product_list = []
            json_all_num = json_all_num / json_tr_long  # tr 수 찾기
            try:
                for i in range(0, int(json_all_num)):
                    product_list.append(json_data[json_pre:json_next])
                    json_pre += json_tr_long
                    json_next += json_tr_long
            except:
                messages.error(self.request, '알수없는 에러가 발생하였습니다.')
                urls = self.request.META.get('HTTP_REFERER')
                return redirect(urls)

            order_info_pk = self.kwargs['pk']
            query_update =design_models.OrderInfo.objects.filter(id=order_info_pk)
            if product_list:
                state = form.cleaned_data['state']
                tax = True if form.cleaned_data['tax'] == '0' else False
                joo_date = form.cleaned_data['joo_date']
                if str(context_data['put_joo_date']) == joo_date:
                    today_num = context_data['put_today_num']
                else:
                    today_num = design_models.OrderInfo.objects.filter(joo_date=joo_date).aggregate(Max('today_num'))
                    if not today_num['today_num__max']:  # 1번을 만들기 위함
                        today_num['today_num__max'] = 0
                    today_num = today_num['today_num__max'] + 1


                if form.cleaned_data['order_date']:
                    order_date = form.cleaned_data['order_date']
                else:
                    order_date = None

                for query in query_update:
                    if int(context_data['put_code']) != int(form.cleaned_data['code']):
                        try:
                            code = int(form.cleaned_data['code'])
                            user = member_models.Profile.objects.select_related('user').get(code=code)
                            user = user.user
                        except:
                            user = None
                        query.user = user
                    query.joo_date = joo_date
                    query.order_date = order_date
                    query.today_num = today_num
                    query.company = form.cleaned_data['company']
                    query.company_keyword = form.cleaned_data['company_keyword']
                    query.employees = form.cleaned_data['manager']
                    query.options = form.cleaned_data['option']
                    query.address = form.cleaned_data['address']
                    query.tell = form.cleaned_data['tell']
                    query.checker = form.cleaned_data['confirm']
                    query.keywords = form.cleaned_data['memo']
                    query.in_memo = form.cleaned_data['in_memo']
                    query.out_memo = form.cleaned_data['out_memo']
                    query.fix_manager = form.cleaned_data['fix_manager']
                    query.state = state
                    query.tax = tax
                    query.save()

                #for product list below

                list_sort = 1

                order_lists = design_models.OrderList.objects.filter(order_info_id=order_info_pk)
                pk_list = [k.id for k in order_lists]
                pk_list_len = len(pk_list)
                product_list_len = len(product_list)
                update_count = 0
                for product_data in product_list:
                    quantity = product_data[3].replace(',', '')
                    selling_price = product_data[4].replace(',', '')
                    price = product_data[7].replace(',', '')
                    price_tax = round(float(price) / 10)
                    if tax:
                        selling_price_tax = round(float(selling_price) / 10)
                    else:
                        selling_price_tax = 0
                    try:
                        code = int(product_data[0])
                    except:
                        code = None

                    data = {
                        'order_info_id': order_info_pk,
                        'list_sort': int(list_sort),
                        'num': int(today_num),
                        'code': code,
                        'name': product_data[1],
                        'standard': product_data[2],
                        'quantity': float(quantity),
                        'selling_price': float(selling_price),
                        'selling_price_tax': float(selling_price_tax),
                        'price': float(price),
                        'price_tax': price_tax,
                        'group_manage': product_data[8],
                        'gram': product_data[9],
                        'etc': product_data[10],
                        'memo': product_data[11],
                    }
                    if pk_list_len > product_list_len:  # 기존 > 신규
                        # 이경우 0번째 id는 재사용 나머지는 삭제
                        design_models.OrderList.objects.update_or_create(
                            id=pk_list[0],
                            defaults={**data},
                        )
                        num = pk_list[0]
                        pk_list.remove(num)
                        print(update_count ,pk_list_len, product_list_len)
                        if update_count == product_list_len-1:
                            del_data =design_models.OrderList.objects.filter(id__in=pk_list)
                            del_data.delete()
                    else: # 기존 <= 신규
                        try: # 기존 id 덮어쓰기 + 신규 생성
                            design_models.OrderList.objects.update_or_create(
                                        id=pk_list[update_count],
                                        defaults={**data},
                                    )
                        except:
                            design_models.OrderList(**data).save()
                    update_count += 1
                    list_sort += 1


        self.success_url = self.request.META.get('HTTP_REFERER')
        response = super(OrdersUpdateView, self).form_valid(form)
        log_save.UserLogs(user=self.request.user.username, model_id=self.kwargs['pk'], model_name=self.model.__name__, action='수정')
        return response

    def form_invalid(self, form):
        error_message = '[확인 해야할 오류 항목] \n'
        if 'company' in form.errors:
            error_message += '업체명\n'
        if 'code' in form.errors:
            error_message += '코드번호'
        if 'manager' in form.errors:
            error_message += '담당자'
        if 'json_data' in form.errors:
            error_message += '품목이 없거나 잘못되었습니다.'
        messages.error(self.request, error_message)
        urls = self.request.META.get('HTTP_REFERER')
        return redirect(urls)

    # optional
    login_url = clovi_login_url


class DemandView(viewmixin.UserIsStaffMixin, generic.TemplateView):
    template_name = 'managing/demand_list.html'
    # optional
    login_url = clovi_login_url

class BillView(generic.DetailView):
    template_name = 'managing/bill.html'
    model = design_models.OrderInfo

    def get_queryset(self):
        queryset = design_models.OrderInfo.objects.prefetch_related('order_list')
        return queryset

    def get_object(self, queryset=None):
        obj = super(BillView, self).get_object(queryset=queryset)
        all = obj.order_list.all()
        sub = 0
        tax = 0
        total = 0
        for i in all:
            sub += round(i.selling_price)*i.quantity
            tax += round(i.selling_price_tax)*i.quantity

        obj.sub = round(sub)
        obj.tax = round(tax)
        obj.total =  round(sub)+round(tax)
        return obj


class SpecialPriceView(viewmixin.UserIsStaffMixin, viewmixin.PageableMixin, viewmixin.DataSearchFormMixin,
                       generic.ListView):
    template_name = 'managing/special_price.html'
    paginate_by = 10
    model = managing_models.SpecialPrice
    data_search_form = managing_forms.DataSearchForm
    # optional
    login_url = clovi_login_url

    def get_queryset(self):
        queryset = super().get_queryset().select_related('product__supplier__profile', 'customer__profile').order_by(
            '-created')
        form = self.data_search_form(self.request.GET)
        if form.is_valid() and form.cleaned_data['q']:
            q = form.cleaned_data['q']
            if q:
                try:
                    q = q.split()
                    for i in q:
                        queryset = queryset.filter(
                            Q(customer__profile__company__icontains=i) | Q(new_price__icontains=i)
                            | Q(product__standard__icontains=i)
                        )
                except:
                    pass
        return queryset


class SpecialPriceCreateView(viewmixin.UserIsStaffMixin, SuccessMessageMixin, generic.FormView):
    template_name = 'managing/special_price_create.html'
    form_class = managing_forms.SpecialPriceForm
    success_url = "/clovi/special_price"
    success_message = '신규 등록 되었습니다.'

    def form_valid(self, form):
        customer = form.cleaned_data['customer']
        try:
            customer = member_models.Profile.objects.filter(code=customer)
        except:
            messages.error(self.request, '고객 정보를 불러오는데 실패하였습니다.')
            return redirect('/clovi/special_price')
        for i in customer:
            customer = i.user_id
        product = form.cleaned_data['product']
        new_price = form.cleaned_data['new_price']
        managing_models.SpecialPrice(customer_id=customer, product_id=product, new_price=new_price).save()
        response = super(SpecialPriceCreateView, self).form_valid(form)
        return response


class SpecialPriceUpdateView(viewmixin.UserIsStaffMixin, SuccessMessageMixin, generic.FormView):
    template_name = 'managing/special_price_update.html'
    form_class = managing_forms.SpecialPriceForm
    success_url = "/clovi/special_price"
    success_message = '수정 되었습니다.'

    def get_context_data(self, **kwargs):
        context = super(SpecialPriceUpdateView, self).get_context_data(**kwargs)
        path = self.kwargs['pk']
        data = managing_models.SpecialPrice.objects.select_related('product__supplier__profile',
                                                                   'customer__profile').filter(id=path)
        for z in data:
            context['new'] = z.new_price
            context['customer'] = z.customer.profile.company
            context['product'] = z.product.standard
            context['customer_id'] = z.customer.profile.code
            context['product_id'] = z.product.id
        return context

    def form_valid(self, form):
        path = self.kwargs['pk']
        data = managing_models.SpecialPrice.objects.get(id=path)
        customer = form.cleaned_data['customer']
        try:
            customer = member_models.Profile.objects.filter(code=customer)
        except:
            messages.error(self.request, '고객 정보를 불러오는데 실패하였습니다.')
            return redirect('/clovi/special_price')
        for i in customer:
            customer = i.user_id
        product = form.cleaned_data['product']
        new_price = form.cleaned_data['new_price']
        data.customer_id = customer
        data.product_id = product
        data.new_price = new_price
        data.save()
        response = super(SpecialPriceUpdateView, self).form_valid(form)
        return response


class SpecialPriceDeleteView(viewmixin.UserIsStaffMixin, generic.DeleteView):
    model = managing_models.SpecialPrice
    success_url = "/clovi/special_price"



class EmployeesView(viewmixin.UserIsStaffMixin, viewmixin.PageableMixin, viewmixin.DataSearchFormMixin,
                    generic.ListView):
    template_name = 'managing/employees.html'
    context_object_name = 'employees_list'
    model = managing_models.Employees
    paginate_by = 10
    data_search_form = managing_forms.DataSearchForm
    # optional
    login_url = clovi_login_url

    def get_queryset(self):
        queryset = super(EmployeesView, self).get_queryset().select_related('user').order_by('-created')
        return queryset

    def get_context_data(self, **kwargs):
        context = super(EmployeesView, self).get_context_data(**kwargs)
        return context


class EmployeesCreateView(viewmixin.UserIsStaffMixin, SuccessMessageMixin, generic.CreateView):
    form_class = managing_forms.EmployeesCreateForm
    success_url = "/clovi/employees"
    success_message = '%(user)s 신규 등록 되었습니다.'
    # optional
    login_url = clovi_login_url

    def form_valid(self, form):
        obj = form.save(commit=False)
        name = str(obj.name)
        check_is = User.objects.filter(username=name).exists()
        if check_is:
            if self.request.is_ajax():
                return JsonResponse(dict(login_error='이미 가입된 계정이 존재합니다.', is_success=False))
            return redirect('/clovi/employees/create')
        else:
            try:
                first_name = name + ' 디자이너님'
                user = User.objects.create_user(username=name, password='iclover77', is_staff=True,
                                                first_name=first_name)
                obj.user_id = user.id
            except:
                pass
            response = super(EmployeesCreateView, self).form_valid(form)
            return response

    def get_queryset(self):
        queryset = super(EmployeesCreateView, self).get_queryset().select_related('user__user').order_by('-created')
        return queryset

    def get_template_names(self):
        if self.request.is_ajax():
            return ['managing/employees_create_form_.html']
        return ['managing/employees_create.html']


class EmployeesUpdateView(viewmixin.UserIsStaffMixin, SuccessMessageMixin, generic.UpdateView):
    model = managing_models.Employees
    form_class = managing_forms.EmployeesUpdateForm
    context_object_name = 'employees_list'
    template_name = 'managing/employees_update.html'
    success_url = "/clovi/employees"
    success_message = '정보가 수정되었습니다.'
    # optional
    login_url = clovi_login_url

class ImageBoxView(viewmixin.UserIsStaffMixin, viewmixin.PageableMixin, viewmixin.DataSearchFormMixin, generic.ListView):
    template_name = 'managing/img_box.html'
    context_object_name = 'image_list'
    paginate_by = 20
    model = managing_models.Sample
    data_search_form = managing_forms.DataSearchForm
    # optional
    login_url = clovi_login_url


    def get_queryset(self):
        queryset_sample = super().get_queryset()
        queryset_order =design_models.OrderImg.objects
        form = self.data_search_form(self.request.GET)
        if form.is_valid() and form.cleaned_data['q']:
            def com(queryset, q):
                queryset = queryset.filter( Q(name__icontains=q) | Q(keyword__icontains=q))
                return queryset
            q = form.cleaned_data['q']
            log_save.ImageSearchLogs(action='검색',user=self.request.user.username, q = q)
            if q:
                try:
                    q = q.split()
                    for i in q:
                        queryset_sample= com(queryset_sample,i)
                        queryset_order = com(queryset_order,i)
                except:
                    pass

        queryset_sample = queryset_sample.values_list('images', 'name', 'keyword', 'link', 'created')
        queryset_order = queryset_order.values_list('images', 'name', 'keyword', 'link', 'created')
        queryset = queryset_order.union(queryset_sample).order_by('-created')
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ImageBoxView, self).get_context_data(**kwargs)
        return context



class DepositView(viewmixin.UserIsStaffMixin, viewmixin.PageableMixin, viewmixin.DataSearchFormMixin, generic.ListView):
    template_name = 'managing/deposit.html'
    context_object_name = 'deposit_list'
    paginate_by = 10
    model = managing_models.Deposit
    data_search_form = managing_forms.DataSearchForm
    # optional
    login_url = clovi_login_url

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-created')
        form = self.data_search_form(self.request.GET)
        if form.is_valid() and form.cleaned_data['q']:
            q = form.cleaned_data['q']
            if q:
                try:
                    q = q.split()
                    for i in q:
                        queryset = queryset.filter(
                            Q(bank__icontains=i) | Q(name__icontains=i)
                            | Q(amount__icontains=i) | Q(memo__icontains=i)
                        )
                except:
                    pass
        return queryset

    def get_context_data(self, **kwargs):
        context = super(DepositView, self).get_context_data(**kwargs)
        obj_id_list = [i.id for i in context['object_list']]
        data = managing_models.OrderWithDeposit.objects.select_related('deposit_with','order_info_with').prefetch_related('order_info_with__order_list').filter(deposit_with_id__in=obj_id_list)
        data_id_list = [i.deposit_with.id for i in data]
        for i in context['object_list']:
            if i.id in data_id_list:
                data_list = []
                for z in data:
                    total = 0
                    if i.id == z.deposit_with.id:
                        for o in z.order_info_with.order_list.all():
                            total += o.total
                        joo =[z.order_info_with.joo_date.strftime('%Y-%m-%d'), z.order_info_with.company, total]
                        data_list.append(joo)
                i.data_list = data_list
        return context


class DepositCreateView(viewmixin.UserIsStaffMixin, SuccessMessageMixin, generic.CreateView):
    form_class = managing_forms.DepositCreateForm
    template_name = 'managing/deposit_create.html'
    success_url = "/clovi/deposit"
    success_message = '신규 등록 되었습니다.'
    # optional
    login_url = clovi_login_url

    def get_queryset(self):
        queryset = super(DepositCreateView, self).get_queryset()
        return queryset

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.date = datetime.datetime.now()
        try:
            obj.bank = obj.bank + '_(관리자 등록)'
        except:
            return redirect('managing:deposit')
        obj.part = '입금'
        return super(DepositCreateView, self).form_valid(form)

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse(dict(form.errors, is_success=False))
        return redirect('/clovi/deposit/create')

    def get_template_names(self):
        if self.request.is_ajax():
            return ['managing/deposit_create_form_.html']
        return ['managing/deposit_create.html']


class DepositUpdateView(viewmixin.UserIsStaffMixin, generic.UpdateView):
    model = managing_models.Deposit
    form_class = managing_forms.DepositUpdateForm
    success_url = "/clovi/deposit"
    success_message = '요청사항이 수정되었습니다.'
    # optional
    login_url = clovi_login_url

    def form_valid(self, form):
        if self.request.is_ajax():
            self.success_url = self.request.META.get('HTTP_REFERER')
        response = super(DepositUpdateView, self).form_valid(form)
        return response

    def get_context_data(self, **kwargs):
        context = super(DepositUpdateView, self).get_context_data(**kwargs)
        print(context)
        return context


class DepositDeleteView(viewmixin.UserIsStaffMixin, generic.DeleteView):
    model = managing_models.Deposit
    success_url = '/clovi/deposit/'


class OrderWithDepositCreateView(viewmixin.UserIsStaffMixin, SuccessMessageMixin, generic.FormView):
    form_class = managing_forms.OrderWithDepositCreateForm
    success_url = "/clovi/order/0/"
    success_message = '입금이 연결 되었습니다.'
    # optional
    login_url = clovi_login_url

    def get_context_data(self, **kwargs):
        get_id = self.kwargs['pk']
        context = super(OrderWithDepositCreateView, self).get_context_data(**kwargs)
        context['deposit_list'] = managing_models.Deposit.objects.filter(state=False).order_by('-id')
        data = design_models.OrderInfo.objects.filter(id=get_id).prefetch_related('order_list')
        order_id = ''
        for i in data:
            order_id = i.id
            selling_price = []
            selling_price_tax = []
            context['company'] = i.company
            context['deposit_check'] = i.deposit_check
            for z in i.order_list.all():
                selling_price.append(round(z.selling_price*z.quantity))
                selling_price_tax.append(round(z.selling_price_tax * z.quantity))

            context['selling_price'] = sum(selling_price)
            context['selling_price_tax'] = sum(selling_price_tax)
            context['total'] = sum(selling_price) + sum(selling_price_tax)
        context['order_deposit_list'] = managing_models.OrderWithDeposit.objects.filter(order_info_with_id = order_id).prefetch_related('deposit_with','order_info_with')
        return context

    def form_valid(self, form):
        print(form.cleaned_data)
        self.success_url = self.request.META.get('HTTP_REFERER')
        order_id = self.kwargs['pk']
        balance = form.cleaned_data['balance']
        deposit = form.cleaned_data['deposit']
        delete = form.cleaned_data['delete']
        division = form.cleaned_data['division']
        order_with = managing_models.OrderWithDeposit

        if ',' in deposit:
            deposit = deposit.split(',')
            for i in deposit:
                data = order_with(order_info_with_id =order_id,deposit_with_id=i)
                if balance == '0':
                    depo_id = managing_models.Deposit.objects.get(id=i)
                    depo_id.state = True
                    depo_id.save()
                data.save()
        elif deposit != '':
            data = order_with(order_info_with_id =order_id,deposit_with_id=deposit)
            if balance == '0':
                depo_id = managing_models.Deposit.objects.get(id=deposit)
                depo_id.state = True
                depo_id.save()
            data.save()
        update_mdel = managing_models.Deposit
        if ',' in delete:
            delete = delete.split(',')
            dele_list = order_with.objects.filter(id__in=delete).prefetch_related('deposit_with')
            for i in dele_list:
                update_id = i.deposit_with.id
                updata_data = update_mdel.objects.get(id=update_id)
                updata_data.state = False
                updata_data.save()
            dele_list.delete()
        elif delete != '':
            dele_list = order_with.objects.filter(id=delete).prefetch_related('deposit_with')
            for i in dele_list:
                update_id = i.deposit_with.id
                updata_data = update_mdel.objects.get(id=update_id)
                updata_data.state = False
                updata_data.save()
            dele_list.delete()

        data = design_models.OrderInfo.objects.filter(id=order_id)
        for i in data:
            i.deposit = balance
            if balance == '0':
                i.deposit_check = 0
            elif balance != '':
                i.deposit_check = balance
            if division == '987654':
                i.deposit_check = 987654
            elif  division == '-1':
                i.deposit_check = -1
            i.save()


        return super(OrderWithDepositCreateView, self).form_valid(form)

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse(dict(form.errors, is_success=False))
        return redirect('/clovi/order/0/')

    def get_template_names(self):
        if self.request.is_ajax():
            return ['managing/order_deposit_create_form_.html']
        return ['managing/order_deposit_create_form_.html']

class OrderWithImagesCreateView(viewmixin.UserIsStaffMixin, SuccessMessageMixin, generic.FormView):
    form_class = managing_forms.OrderWithImagesCreateForm
    success_url = "/clovi/order/0/"
    success_message = '이미지가 등록 되었습니다.'
    # optional
    login_url = clovi_login_url

    def get_context_data(self, **kwargs):
        get_id = self.kwargs['pk']
        context = super(OrderWithImagesCreateView, self).get_context_data(**kwargs)
        context['img_list'] = design_models.OrderImg.objects.filter(order_info_id=get_id)
        return context

    def form_valid(self, form):
        files = self.request.FILES.getlist('pro_image')
        self.success_url = self.request.META.get('HTTP_REFERER')
        order_id = self.kwargs['pk']
        for file in files:
            img_model = design_models.OrderImg(order_info_id=order_id, images=file, name=file.name)
            img_model.save()

        return super(OrderWithImagesCreateView, self).form_valid(form)

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse(dict(form.errors, is_success=False))
        return redirect('/clovi/order/0/')

    def get_template_names(self):
        if self.request.is_ajax():
            return ['managing/order_images_create_form_.html']
        return ['managing/order_images_create_form_.html']


class OrderWithImagesDeleteView(viewmixin.UserIsStaffMixin, generic.DeleteView):
    model = design_models.OrderImg
    success_url = "/clovi/order/0/"

    def dispatch(self, request, *args, **kwargs):
        if self.request.is_ajax():
            img_id = kwargs['pk']
            path = self.request.POST['path']
            i = int(re.findall('\d+', path)[-1])
            try:
                data = design_models.OrderImg.objects.get(id=img_id, order_info_id=i)
                data.delete()
            except:
                raise ValueError
        return redirect('/clovi/order/0/')




class AskView(viewmixin.UserIsStaffMixin, viewmixin.PageableMixin, viewmixin.DataSearchFormMixin, generic.ListView):
    template_name = 'managing/ask.html'
    context_object_name = 'ask_list'
    paginate_by = 10
    model = managing_models.Ask
    data_search_form = managing_forms.DataSearchForm
    template_name_suffix = '__update'
    # optional
    login_url = clovi_login_url

    def get_queryset(self):
        queryset = super().get_queryset().select_related('ask_to__profile').order_by('ask_finish', '-created')
        form = self.data_search_form(self.request.GET)
        if form.is_valid() and form.cleaned_data['q']:
            q = form.cleaned_data['q']
            if q:
                try:
                    q = q.split()
                    for i in q:
                        queryset = queryset.filter(
                            Q(ask_from__icontains=i) | Q(ask_to__username__icontains=i)
                            | Q(ask_what__icontains=i)
                        )
                except:
                    pass
        return queryset

    def get_context_data(self, **kwargs):
        context = super(AskView, self).get_context_data(**kwargs)
        return context


class AskCreateView(viewmixin.UserIsStaffMixin, SuccessMessageMixin, generic.CreateView):
    form_class = managing_forms.AskCreateForm
    template_name = 'managing/ask_create.html'
    success_url = "/clovi/ask"
    success_message = '요청이 신규 등록 되었습니다.'
    # optional
    login_url = clovi_login_url

    def get_queryset(self):
        queryset = super(AskCreateView, self).get_queryset().select_related('ask_to__profile')
        return queryset

    def form_valid(self, form):
        if self.request.is_ajax():
            self.success_url = self.request.META.get('HTTP_REFERER')
        obj = form.save(commit=False)
        obj.ask_from = self.request.user
        return super(AskCreateView, self).form_valid(form)

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse(dict(form.errors, is_success=False))
        return redirect('/clovi/ask/create')

    def get_template_names(self):
        if self.request.is_ajax():
            return ['managing/ask_create_form_.html']
        return ['managing/ask_create.html']


class AskUpdateView(viewmixin.UserIsStaffMixin, SuccessMessageMixin, generic.UpdateView):
    model = managing_models.Ask
    form_class = managing_forms.AskUpdateForm
    context_object_name = 'update_list'
    success_url = "/clovi/ask"
    success_message = '요청사항이 수정되었습니다.'
    # optional
    login_url = clovi_login_url

    def form_valid(self, form):
        if self.request.is_ajax():
            self.success_url = self.request.META.get('HTTP_REFERER')
        response = super(AskUpdateView, self).form_valid(form)
        return response

    def get_template_names(self):
        if self.request.is_ajax():
            return ['managing/ask_update_form_.html']
        return ['managing/ask_update.html']


class PaymentListView(APIView):
    permission_classes = (IsAuthenticated,) if not settings.DEBUG else ()

    def get(self, request, format=None):
        payments = [{'상호명': p.name, '금액': p.amount} for p in
                    managing_models.Deposit.objects.all()[:10]] if settings.DEBUG else None
        return Response(payments)

    def post(self, request, format=None):
        serializer = serializers.PaymentSerializer(data=request.data)
        if serializer.is_valid():
            phone= request.data['phone']
            tell = request.data['tell']
            message = request.data['message']
            print(f'{phone} {tell} {message}')
            save = True

            if save:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
