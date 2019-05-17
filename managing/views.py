import datetime
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import login as django_login, logout as django_logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.mixins import (
    AccessMixin, LoginRequiredMixin )
from django.db.models import Q

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse
from . import models as managing_models
from member import models as member_models
from design import models as design_models
from . import forms as managing_forms
from . import viewmixin

clovi_login_url = '/clovi/login/'

class Login(generic.FormView):
    template_name = 'managing/login.html'
    form_class = managing_forms.LoginForm

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username,password=password)
        if user:
            django_login(self.request, user)
        return redirect('managing:main')

    def form_invalid(self, form):
        form.add_error(None, '아이디 또는 비밀번호가 올바르지 않습니다')
        return super(Login, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(Login, self).get_context_data(**kwargs)
        return context

def logout(request):
    django_logout(request)
    return redirect('managing:main')

class Main(LoginRequiredMixin, viewmixin.PageableMixin, viewmixin.DataSearchFormMixin, generic.ListView):
    template_name = 'managing/main.html'
    context_object_name = 'memo_list'
    paginate_by = 20
    model = managing_models.Memo
    data_search_form = managing_forms.DataSearchForm
    # optional
    login_url = clovi_login_url

    def get_queryset(self):
        return managing_models.Memo.objects.order_by('-importance','-created').filter(confirm=False)

    def get_context_data(self, **kwargs):
        context = super(Main, self).get_context_data(**kwargs)
        context['my_list'] = []
        context['common_list'] = []
        for i in context['memo_list']:
            if i.employees == self.request.user.username:
                data = [i.pk, i.importance, i.content,self.request.user.username, i.common]
                context['my_list'].append(data)
            else:
                if i.common == True:
                    data = [i.pk, i.importance, i.content, i.employees]
                    context['common_list'].append(data)
        return context

class MemoCreateView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
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

    def get_template_names(self):
        if self.request.is_ajax():
            return ['managing/memo_update_form_.html']
        return ['managing/memo_update.html']

class CustomerResultView(LoginRequiredMixin, viewmixin.PageableMixin, viewmixin.DataSearchFormMixin, generic.ListView):
    template_name = 'managing/customer_result.html'
    context_object_name = 'result_list'
    paginate_by = 12
    model = member_models.Profile
    data_search_form = managing_forms.DataSearchForm
    # optional
    login_url = clovi_login_url

    def get_queryset(self):
        queryset = super().get_queryset().select_related('user').order_by('-created')
        form = self.data_search_form(self.request.GET)
        if form.is_valid() and form.cleaned_data['q']:
            q = form.cleaned_data['q']
            if q:
                try:
                    q = q.split()
                    for i in q:
                        queryset = queryset.filter(
                            Q(company__icontains=i) | Q(company_keyword__icontains=i) | Q(address__icontains=i)
                            | Q(phone__icontains=i) | Q(code__icontains=i)  | Q(user__username__icontains=i)
                        )
                except:
                    pass
        return queryset

    def get_context_data(self, **kwargs):
        context = super(CustomerResultView, self).get_context_data(**kwargs)

        return context

class CustomerView(LoginRequiredMixin, viewmixin.PageableMixin, viewmixin.DataSearchFormMixin, generic.ListView):
    context_object_name = 'customer_list'
    paginate_by = 10
    model = member_models.Profile
    data_search_form = managing_forms.DataSearchForm
    # optional
    login_url = clovi_login_url

    def get_queryset(self):
        queryset = super().get_queryset().select_related('user').order_by('-created')
        form = self.data_search_form(self.request.GET)
        if form.is_valid() and form.cleaned_data['q']:
            q = form.cleaned_data['q']
            if q:
                try:
                    q = q.split()
                    for i in q:
                        queryset = queryset.filter(
                            Q(company__icontains=i) | Q(company_keyword__icontains=i)| Q(address__icontains=i)
                            | Q(phone__icontains=i)| Q(code__icontains=i)
                        )
                except:
                    pass
        return queryset

    def get_context_data(self, **kwargs):
        context = super(CustomerView, self).get_context_data(**kwargs)
        return context

    def get_template_names(self):
        return ['managing/customer.html']


class CustomerCreateView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    form_class = managing_forms.CustomerCreateForm
    success_url = "/clovi/customer"
    success_message = '%(company)s님의 정보가 신규 등록 되었습니다..'
    # optional
    login_url = clovi_login_url

    def form_valid(self, form):
        obj = form.save(commit=False)
        name = str(obj.code)+'_temporary'
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
            return  response

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse(dict(form.errors, is_success=False))
        return redirect('/clovi/customer/create')

    def get_template_names(self):
        if self.request.is_ajax():
            return ['managing/customer_create_form_.html']
        return ['managing/customer_create.html']

class CustomerUpdateView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = member_models.Profile
    form_class = managing_forms.CustomerUpdateForm
    context_object_name = 'update_list'
    success_url = "/clovi/customer"
    success_message = '%(company)s님의 정보가 수정되었습니다.'
    # optional
    login_url = clovi_login_url

    def form_valid(self, form):
        response = super(CustomerUpdateView, self).form_valid(form)
        return response

    def get_template_names(self):
        if self.request.is_ajax():
            return ['managing/customer_update_form_.html']
        return ['managing/customer_update.html']

class ProductView(LoginRequiredMixin, viewmixin.PageableMixin, viewmixin.DataSearchFormMixin, generic.ListView):
    template_name = 'managing/product.html'
    context_object_name = 'product_list'
    paginate_by = 10
    model = design_models.ProductBase
    data_search_form = managing_forms.DataSearchForm
    # optional
    login_url = clovi_login_url

    def get_queryset(self):
        queryset = super().get_queryset()
        form = self.data_search_form(self.request.GET)
        if form.is_valid() and form.cleaned_data['q']:
            q = form.cleaned_data['q']
            if q:
                try:
                    q = q.split()
                    for i in q:
                        queryset = queryset.filter(
                            Q(price__icontains=i) | Q(selling_price__icontains=i)
                        )
                except:
                    pass
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ProductView, self).get_context_data(**kwargs)
        return context

class ProdcutCreateView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    form_class = managing_forms.ProductCreateForm
    template_name = 'managing/product_create.html'
    success_url = "/clovi/product"
    success_message = '신규 등록 되었습니다.'
    # optional
    login_url = clovi_login_url

    def get_queryset(self):
        queryset = super(ProdcutCreateView, self).get_queryset()
        return queryset

class ProductUpdateView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = design_models.ProductBase
    form_class = managing_forms.ProductUpdateForm
    context_object_name = 'update_list'
    template_name = 'managing/product_update.html'
    success_url = "/clovi/product"
    success_message = '정보가 수정되었습니다.'
    # optional
    login_url = clovi_login_url


class SampleView(LoginRequiredMixin, viewmixin.PageableMixin, viewmixin.DataSearchFormMixin, generic.ListView):
    template_name = 'managing/sample.html'
    context_object_name = 'sample_list'
    paginate_by = 10
    model = managing_models.Sample
    data_search_form = managing_forms.DataSearchForm
    # optional
    login_url = clovi_login_url

    def get_queryset(self):
        queryset = super().get_queryset().select_related('employees','category','sectors_category').order_by('-created')
        form = self.data_search_form(self.request.GET)
        if form.is_valid() and form.cleaned_data['q']:
            q = form.cleaned_data['q']
            if q:
                try:
                    q = q.split()
                    for i in q:
                        queryset = queryset.filter(
                            Q(keyword__icontains=i) | Q(name__icontains=i)| Q(employees__username__icontains=i)
                            | Q(category__title__icontains=i)| Q(sectors_category__title__icontains=i)
                        )
                except:
                    pass
        return queryset

    def get_context_data(self, **kwargs):
        context = super(SampleView, self).get_context_data(**kwargs)
        return context


class SampleCreateView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    form_class = managing_forms.SampleCreateForm
    template_name = 'managing/sample_create.html'
    success_url = "/clovi/sample"
    success_message = '샘플이 신규 등록 되었습니다.'
    # optional
    login_url = clovi_login_url

    def get_queryset(self):
        queryset = super(SampleCreateView, self).get_queryset().prefetch_related('employees__user')
        return queryset

class SampleUpdateView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = managing_models.Sample
    form_class = managing_forms.SampleUpdateForm
    context_object_name = 'update_list'
    template_name = 'managing/sample_update.html'
    success_url = "/clovi/sample"
    success_message = '%(name)s 샘플이 수정되었습니다.'
    # optional
    login_url = clovi_login_url

class CategoryView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'managing/category.html'
    # optional
    login_url = clovi_login_url

class DiscountView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'managing/discount.html'
    # optional
    login_url = clovi_login_url

class Deal_listView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'managing/deal_list.html'
    # optional
    login_url = clovi_login_url

class DemandView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'managing/demand_list.html'
    # optional
    login_url = clovi_login_url

class EmployeesView(LoginRequiredMixin, viewmixin.PageableMixin, viewmixin.DataSearchFormMixin, generic.ListView):
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

class EmployeesCreateView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    form_class = managing_forms.EmployeesCreateForm
    success_url = "/clovi/employees"
    success_message = '직원이 신규 등록 되었습니다.'
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
                first_name = name+' 디자이너님'
                user = User.objects.create_user(username=name, password='iclover77', is_staff=True, first_name = first_name)
                obj.user_id = user.id
            except:
                pass
            response = super(EmployeesCreateView, self).form_valid(form)
            return  response

    def get_queryset(self):
        queryset = super(EmployeesCreateView, self).get_queryset().select_related('user__user').order_by('-created')
        return queryset

    def get_template_names(self):
        if self.request.is_ajax():
            return ['managing/employees_create_form_.html']
        return ['managing/employees_create.html']

class EmployeesUpdateView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = managing_models.Employees
    form_class = managing_forms.EmployeesUpdateForm
    context_object_name = 'employees_list'
    template_name = 'managing/employees_update.html'
    success_url = "/clovi/employees"
    success_message = '정보가 수정되었습니다.'
    # optional
    login_url = clovi_login_url

class DepositView(LoginRequiredMixin, viewmixin.PageableMixin, viewmixin.DataSearchFormMixin, generic.ListView):
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
        return context

class DepositCreateView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
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
        obj.bank = obj.bank + '_(관리자 등록)'
        obj.part = '입금'
        return super(DepositCreateView, self).form_valid(form)

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse(dict(form.errors, is_success=False))
        return redirect('/managing/deposit/create')

    def get_template_names(self):
        if self.request.is_ajax():
            return ['managing/deposit_create_form_.html']
        return ['managing/deposit_create.html']

class DepositUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = managing_models.Deposit
    form_class = managing_forms.DepositUpdateForm
    success_url = "/clovi/deposit"
    success_message = '요청사항이 수정되었습니다.'
    # optional
    login_url = clovi_login_url

    def get_context_data(self, **kwargs):
        context = super(DepositUpdateView, self).get_context_data(**kwargs)
        print(context)
        return context

class AskView(LoginRequiredMixin, viewmixin.PageableMixin, viewmixin.DataSearchFormMixin, generic.ListView):
    template_name = 'managing/ask.html'
    context_object_name = 'ask_list'
    paginate_by = 10
    model = managing_models.Ask
    data_search_form = managing_forms.DataSearchForm
    template_name_suffix = '__update'
    # optional
    login_url = clovi_login_url

    def get_queryset(self):
        queryset = super().get_queryset().select_related('ask_to__profile').order_by('ask_finish','-created')
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


class AskCreateView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
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
        obj = form.save(commit=False)
        obj.ask_from = self.request.user
        return super(AskCreateView, self).form_valid(form)

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse(dict(form.errors, is_success=False))
        return redirect('/managing/ask/create')

    def get_template_names(self):
        if self.request.is_ajax():
            return ['managing/ask_create_form_.html']
        return ['managing/ask_create.html']

class AskUpdateView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = managing_models.Ask
    form_class = managing_forms.AskUpdateForm
    context_object_name = 'update_list'
    success_url = "/clovi/ask"
    success_message = '요청사항이 수정되었습니다.'
    # optional
    login_url = clovi_login_url

    def form_valid(self, form):
        response = super(AskUpdateView, self).form_valid(form)
        return response

    def get_template_names(self):
        if self.request.is_ajax():
            return ['managing/ask_update_form_.html']
        return ['managing/ask_update.html']