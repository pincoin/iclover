from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth.models import User

from . import models as managing_models
from member import models as member_models
from design import models as design_models
from . import forms as managing_forms

class Main(generic.TemplateView):
    template_name = 'managing/main.html'

class CustomerView(generic.ListView):
    template_name = 'managing/customer.html'
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
        paginator = context['paginator']
        context['data_search_form'] = self.data_search_form(
            q = self.request.GET.get('q') if self.request.GET.get('q') else ''
        )
        page_numbers_range = 5  # Display only 5 page numbers
        max_index = paginator.page_range[-1]
        page = self.request.GET.get('page')
        current_page = int(page) if page else 1
        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index
        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range
        return context

class CustomerCreateView(SuccessMessageMixin, generic.CreateView):
    form_class = managing_forms.CustomerCreateForm
    template_name = 'managing/customer_create.html'
    success_url = "/managing/customer"
    success_message = '%(company)s님의 정보가 신규 등록 되었습니다..'

    def form_valid(self, form):
        obj = form.save(commit=False)
        name = str(obj.code)+'_temporary'
        check_is = User.objects.filter(username=name).exists()
        if check_is:
            return redirect('/managing/customer/create/')
        else:
            try:
                user = User.objects.create_user(username=name, password='iclover77', is_active=False)
                obj.user_id = user.id
            except:
                pass
            return super(CustomerCreateView, self).form_valid(form)

class CustomerUpdateView(SuccessMessageMixin, generic.UpdateView):
    model = member_models.Profile
    form_class = managing_forms.CustomerUpdateForm
    context_object_name = 'update_list'
    template_name = 'managing/customer_update.html'
    success_url = "/managing/customer"
    success_message = '%(company)s님의 정보가 수정되었습니다.'

class ProductView(generic.ListView):
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
        paginator = context['paginator']
        context['data_search_form'] = self.data_search_form(
            q=self.request.GET.get('q') if self.request.GET.get('q') else ''
        )
        page_numbers_range = 5  # Display only 5 page numbers
        max_index = paginator.page_range[-1]
        page = self.request.GET.get('page')
        current_page = int(page) if page else 1
        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index
        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range
        return context

class ProdcutCreateView(SuccessMessageMixin, generic.CreateView):
    form_class = managing_forms.ProductCreateForm
    template_name = 'managing/product_create.html'
    success_url = "/managing/product"
    success_message = '님의 정보가 신규 등록 되었습니다..'

    def get_queryset(self):
        queryset = super(ProdcutCreateView, self).get_queryset()
        return queryset

class ProductUpdateView(SuccessMessageMixin, generic.UpdateView):
    model = design_models.ProductBase
    form_class = managing_forms.ProductUpdateForm
    context_object_name = 'update_list'
    template_name = 'managing/product_update.html'
    success_url = "/managing/product"
    success_message = '님의 정보가 수정되었습니다.'

class SampleView(generic.TemplateView):
    template_name = 'managing/sample.html'

class CategoryView(generic.TemplateView):
    template_name = 'managing/category.html'

class DiscountView(generic.TemplateView):
    template_name = 'managing/discount.html'

class Deal_listView(generic.TemplateView):
    template_name = 'managing/deal_list.html'

class DemandView(generic.TemplateView):
    template_name = 'managing/demand.html'