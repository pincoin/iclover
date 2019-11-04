from django.contrib.auth.mixins import (UserPassesTestMixin,
    LoginRequiredMixin, PermissionRequiredMixin)
from django.http import HttpResponse
from django.shortcuts import redirect
import re
from design import models as design_model


class PageableMixin(object):

    def get_context_data(self, **kwargs):
        context = super(PageableMixin, self).get_context_data(**kwargs)
        paginator = context['paginator']
        context['page_all_count'] = paginator.count
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

class DataSearchFormMixin(object):

    def get_context_data(self, **kwargs):
        context = super(DataSearchFormMixin, self).get_context_data(**kwargs)
        context['data_search_form'] = self.data_search_form(
            q=self.request.GET.get('q') if self.request.GET.get('q') else ''
        )
        if self.request.GET.get('q'):
            context['q'] = self.request.GET.get('q')

        return context

class UserIsStaffMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_staff:
            return redirect('design:home')
        user_test_result = self.get_test_func()()
        if not user_test_result:
            return HttpResponse('Wemix 관리자가 아닌 경우 접근을 불허합니다.')
        return super(UserPassesTestMixin, self).dispatch(request, *args, **kwargs)


class DeliveryMixin(object):

    def check(self, request, serializer):
        # count 반드시 return
        delivery = ''
        count = 1
        price_d = ''
        try:
            size = serializer.data['size']
            paper = serializer.data['paper']
            side = serializer.data['side']
            deal = serializer.data['deal'].replace(',', '')
            amount = int(serializer.data['amount'])
            item = request.META['HTTP_REFERER'].split('/?item=')[-1]
        except:
            size = serializer['size']
            paper = serializer['paper']
            side = serializer['side']
            deal = serializer['deal'].replace(',', '')
            amount = int(serializer['amount'])
            item = serializer['kind']
        try:
            i = int(re.findall('\d+', deal)[-1])
        except:
            i = None

        del_model = design_model.DeliveryPrice.objects.filter(kind=item)
        if 'flyer' in item:
            count = i * amount
            if 'A' in size:
                price_d = del_model.get(size__icontains='A').sell
                delivery = round(float(price_d)* i * amount * 1.1)
            elif 'B' in size:
                price_d = del_model.get(size__icontains='B').sell
                delivery = round(float(price_d) * i * amount * 1.1)
        elif 'card' in item:
            price_d = del_model.get(kind='card').sell
            i = int(re.findall('\d+', deal)[-1])*amount
            if i <= 10500:
                delivery = round(float(price_d)*1.1)
            elif i <= 26000:
                count = 2
                delivery = round(float(price_d)*count*1.1)
            else:
                count = 3
                delivery = round(float(price_d)*count*1.1)
        return delivery, count, price_d