from django.shortcuts import render
from django.db.models import Q
from django.views.generic import TemplateView, CreateView, ListView, UpdateView

from . import models as managing_models
from member import models as member_models
from design import models as design_models


class Main(TemplateView):
    template_name = 'managing/main.html'

class CustomerView(ListView):
    template_name = 'managing/customer.html'
    context_object_name = 'customer_list'
    paginate_by = 2
    model = member_models.Profile

    def get_queryset(self):
        queryset = super().get_queryset().select_related('user')
        if self.request.GET.get('q'):
            q = self.request.GET.get('q')
            try:
                q = q.split()
                for i in q:
                    queryset = queryset.filter(
                        Q(company__icontains=i) | Q(company_keyword__icontains=i)
                    )
            except:
                pass
        return queryset


    def get_context_data(self, **kwargs):
        context = super(CustomerView, self).get_context_data(**kwargs)
        paginator = context['paginator']
        context['q'] = self.request.GET.get('q')
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


class ProductView(TemplateView):
    template_name = 'managing/product.html'

class SampleView(TemplateView):
    template_name = 'managing/sample.html'

class CategoryView(TemplateView):
    template_name = 'managing/category.html'

class DiscountView(TemplateView):
    template_name = 'managing/discount.html'

class Deal_listView(TemplateView):
    template_name = 'managing/deal_list.html'

class DemandView(TemplateView):
    template_name = 'managing/demand.html'