import datetime

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.models import User
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


class Main(generic.TemplateView):
    template_name = 'managing/main.html'

class ToDoView(generic.TemplateView):
    template_name = 'managing/to_do.html'

class CustomerResultView(viewmixin.PageableMixin, viewmixin.DataSearchFormMixin, generic.ListView):
    template_name = 'managing/customer_result.html'
    context_object_name = 'result_list'
    paginate_by = 12
    model = member_models.Profile
    data_search_form = managing_forms.DataSearchForm

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

class CustomerView(viewmixin.PageableMixin, viewmixin.DataSearchFormMixin, generic.ListView):
    context_object_name = 'customer_list'
    paginate_by = 10
    model = member_models.Profile
    data_search_form = managing_forms.DataSearchForm

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


class CustomerCreateView(SuccessMessageMixin, generic.CreateView):
    form_class = managing_forms.CustomerCreateForm
    success_url = "/managing/customer"
    success_message = '%(company)s님의 정보가 신규 등록 되었습니다..'

    def form_valid(self, form):
        obj = form.save(commit=False)
        name = str(obj.code)+'_temporary'
        check_is = User.objects.filter(username=name).exists()
        if check_is:
            if self.request.is_ajax():
                return JsonResponse(dict(login_error='이미 해당 사업자로 가입된 계정이 존재합니다.', is_success=False))
            return redirect('/managing/customer/create')
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
        return redirect('/managing/customer/create')

    def get_template_names(self):
        if self.request.is_ajax():
            return ['managing/customer_create_form_.html']
        return ['managing/customer_create.html']

class CustomerUpdateView(SuccessMessageMixin, generic.UpdateView):
    model = member_models.Profile
    form_class = managing_forms.CustomerUpdateForm
    context_object_name = 'update_list'
    success_url = "/managing/customer"
    success_message = '%(company)s님의 정보가 수정되었습니다.'

    def form_valid(self, form):
        response = super(CustomerUpdateView, self).form_valid(form)
        return response

    def get_template_names(self):
        if self.request.is_ajax():
            return ['managing/customer_update_form_.html']
        return ['managing/customer_update.html']

class ProductView(viewmixin.PageableMixin, viewmixin.DataSearchFormMixin, generic.ListView):
    template_name = 'managing/product.html'
    context_object_name = 'product_list'
    paginate_by = 10
    model = design_models.ProductBase
    data_search_form = managing_forms.DataSearchForm

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

class ProdcutCreateView(SuccessMessageMixin, generic.CreateView):
    form_class = managing_forms.ProductCreateForm
    template_name = 'managing/product_create.html'
    success_url = "/managing/product"
    success_message = '신규 등록 되었습니다.'

    def get_queryset(self):
        queryset = super(ProdcutCreateView, self).get_queryset()
        return queryset

class ProductUpdateView(SuccessMessageMixin, generic.UpdateView):
    model = design_models.ProductBase
    form_class = managing_forms.ProductUpdateForm
    context_object_name = 'update_list'
    template_name = 'managing/product_update.html'
    success_url = "/managing/product"
    success_message = '정보가 수정되었습니다.'


class SampleView(viewmixin.PageableMixin, viewmixin.DataSearchFormMixin, generic.ListView):
    template_name = 'managing/sample.html'
    context_object_name = 'sample_list'
    paginate_by = 10
    model = managing_models.Sample
    data_search_form = managing_forms.DataSearchForm

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
                            Q(keyword__icontains=i) | Q(name__icontains=i)| Q(employees__name__icontains=i)
                            | Q(category__title__icontains=i)| Q(sectors_category__title__icontains=i)
                        )
                except:
                    pass
        return queryset

    def get_context_data(self, **kwargs):
        context = super(SampleView, self).get_context_data(**kwargs)
        return context


class SampleCreateView(SuccessMessageMixin, generic.CreateView):
    form_class = managing_forms.SampleCreateForm
    template_name = 'managing/sample_create.html'
    success_url = "/managing/sample"
    success_message = '샘플이 신규 등록 되었습니다.'

    def get_queryset(self):
        queryset = super(SampleCreateView, self).get_queryset()
        return queryset

class SampleUpdateView(SuccessMessageMixin, generic.UpdateView):
    model = managing_models.Sample
    form_class = managing_forms.SampleUpdateForm
    context_object_name = 'update_list'
    template_name = 'managing/sample_update.html'
    success_url = "/managing/sample"
    success_message = '%(name)s 샘플이 수정되었습니다.'

class CategoryView(generic.TemplateView):
    template_name = 'managing/category.html'

class DiscountView(generic.TemplateView):
    template_name = 'managing/discount.html'

class Deal_listView(generic.TemplateView):
    template_name = 'managing/deal_list.html'

class DemandView(generic.TemplateView):
    template_name = 'managing/demand.html'

class DepositView(viewmixin.PageableMixin, viewmixin.DataSearchFormMixin, generic.ListView):
    template_name = 'managing/deposit.html'
    context_object_name = 'deposit_list'
    paginate_by = 10
    model = managing_models.Deposit
    data_search_form = managing_forms.DataSearchForm

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

class DepositCreateView(SuccessMessageMixin, generic.CreateView):
    form_class = managing_forms.DepositCreateForm
    template_name = 'managing/deposit_create.html'
    success_url = "/managing/deposit"
    success_message = '신규 등록 되었습니다.'

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

class DepositUpdateView(generic.UpdateView):
    model = managing_models.Deposit
    form_class = managing_forms.DepositUpdateForm
    success_url = "/managing/deposit"
    success_message = '요청사항이 수정되었습니다.'

    def get_context_data(self, **kwargs):
        context = super(DepositUpdateView, self).get_context_data(**kwargs)
        print(context)
        return context

class AskView(viewmixin.PageableMixin, viewmixin.DataSearchFormMixin, generic.ListView):
    template_name = 'managing/ask.html'
    context_object_name = 'ask_list'
    paginate_by = 10
    model = managing_models.Ask
    data_search_form = managing_forms.DataSearchForm
    template_name_suffix = '__update'

    def get_queryset(self):
        queryset = super().get_queryset().select_related('ask_to__user').order_by('ask_finish','-created')
        form = self.data_search_form(self.request.GET)
        if form.is_valid() and form.cleaned_data['q']:
            q = form.cleaned_data['q']
            if q:
                try:
                    q = q.split()
                    for i in q:
                        queryset = queryset.filter(
                            Q(ask_from__icontains=i) | Q(ask_to__user__username__icontains=i)
                            | Q(ask_what__icontains=i)
                        )
                except:
                    pass
        return queryset

    def get_context_data(self, **kwargs):
        context = super(AskView, self).get_context_data(**kwargs)
        return context


class AskCreateView(SuccessMessageMixin, generic.CreateView):
    form_class = managing_forms.AskCreateForm
    template_name = 'managing/ask_create.html'
    success_url = "/managing/ask"
    success_message = '요청이 신규 등록 되었습니다.'

    def get_queryset(self):
        queryset = super(AskCreateView, self).get_queryset().prefetch_related('ask_to__user')
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

class AskUpdateView(SuccessMessageMixin, generic.UpdateView):
    model = managing_models.Ask
    form_class = managing_forms.AskUpdateForm
    context_object_name = 'update_list'
    success_url = "/managing/ask"
    success_message = '요청사항이 수정되었습니다.'

    def form_valid(self, form):
        response = super(AskUpdateView, self).form_valid(form)
        return response

    def get_template_names(self):
        if self.request.is_ajax():
            return ['managing/ask_update_form_.html']
        return ['managing/ask_update.html']