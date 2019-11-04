from functools import reduce

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import viewsets
from rest_framework.response import Response

from member import models as member_models
from design import models as design_models
from managing import models as managing_models
from . import serializers
import operator
from django.db.models import Q
from rest_framework.permissions import IsAdminUser


class UserViewSet(viewsets.ModelViewSet):
    # import pdb;pdb.set_trace()
    permission_classes = (IsAdminUser,)
    queryset = get_user_model().objects.all().order_by('-date_joined')
    serializer_class = serializers.UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminUser,)
    queryset = Group.objects.all()
    serializer_class = serializers.GroupSerializer

class ProfileViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminUser,)
    queryset = member_models.Profile.objects.all()
    serializer_class = serializers.ProfileSerializer
    def get_queryset(self):
        queryset = self.queryset.filter(~Q(state_select=1))
        return queryset

    def list(self, request, *args, **kwargs):
        keyword = request.GET.get('keyword')
        if keyword:
            keyword = keyword.split()
            query = reduce(operator.and_,(Q(company__icontains=item) for item in keyword))
            query1 = reduce(operator.and_, (Q(company_keyword__icontains=item) for item in keyword))
            queryset = self.filter_queryset(self.get_queryset()).filter(query|query1).order_by('company')
        else:
            queryset = self.filter_queryset(self.get_queryset()).order_by('company')[:1]
        page = self.paginate_queryset(queryset)
        for i in page:
            i.id = i.user.id
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ProductTextViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminUser,)
    queryset = design_models.ProductText.objects.all()
    serializer_class = serializers.ProductTextSerializer

    def get_queryset(self):
        queryset = self.queryset.filter(Q(product_version=1)).order_by('-standard')
        return queryset

    def list(self, request, *args, **kwargs):
        keyword = request.GET.get('keyword')
        idx = request.GET.get('idx')
        if keyword:
            keyword = keyword.split()
            query0 = reduce(operator.and_,(Q(standard__icontains=item) for item in keyword))
            query1 = reduce(operator.and_, (Q(gram__icontains=item) for item in keyword))
            query2 = reduce(operator.and_, (Q(memo__icontains=item) for item in keyword))
            query3 = reduce(operator.and_, (Q(etc__icontains=item) for item in keyword))
            queryset = self.filter_queryset(self.get_queryset()).filter(query0|query1|query2|query3).order_by('supplier','-standard')
        else:
            queryset = self.filter_queryset(self.get_queryset()).order_by('supplier','-standard')
        serializer = self.get_serializer(queryset, many=True)
        if idx:
            id_check = managing_models.SpecialPrice.objects.filter(customer_id=idx)
            if id_check.exists():
                has_list = id_check.values_list('product', flat=TabError)
                has_dic = id_check.values('product','new_price')
                for i in serializer.data:
                    if i['id'] in has_list:
                        i['sell_price'] = has_dic.get(product=i['id'])['new_price']
        return Response(serializer.data)

class OrderInfoViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminUser,)
    queryset = design_models.CustomerOrderInfo.objects.all()
    serializer_class = serializers.OrderInfoSerializer

    def list(self, request, *args, **kwargs):
        keyword = request.GET.get('keyword')
        queryset = self.filter_queryset(self.get_queryset().prefetch_related('customer_order_product').filter(user_id=keyword)).order_by('-joo_date','-id')
        page = self.paginate_queryset(queryset)
        for i in page:
            i.order_list = i.customer_order_product.all()
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



class CustomerProfileViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminUser,)
    queryset = member_models.CustomerProfile.objects.all()
    serializer_class = serializers.CustomerProfileSerializer
    def get_queryset(self):
        queryset = self.queryset.select_related('user').prefetch_related('user__customer_memo')
        return queryset

    def list(self, request, *args, **kwargs):
        keyword = request.GET.get('keyword')
        if keyword:
            keyword = keyword.split()
            query = reduce(operator.and_,(Q(company__icontains=item)|Q(user__customer_memo__keyword__icontains=item) for item in keyword))
            queryset = self.filter_queryset(self.get_queryset()).filter(query).order_by('company')
        else:
            queryset = self.filter_queryset(self.get_queryset()).order_by('company')[:1]
        page = self.paginate_queryset(queryset)
        for i in page:
            i.customer_memo = i.user.customer_memo.all()
            i.id = i.user.id
            i.user = i.user
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

#
class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminUser,)
    queryset = design_models.ProductPriceAPI.objects.all()
    serializer_class = serializers.ProductSerializer

    def get_queryset(self):
        queryset = self.queryset.filter().order_by('-created')
        return queryset

    def list(self, request, *args, **kwargs):
        keyword = request.GET.get('keyword')
        idx = request.GET.get('idx')
        if keyword:
            keyword = keyword.split()
            query0 = reduce(operator.and_,(
                Q(size__icontains=item)|Q(side__icontains=item)|Q(paper__icontains=item)|Q(deal__icontains=item)|Q(supplier__icontains=item)
                for item in keyword))
            queryset = self.filter_queryset(self.get_queryset()).filter(query0).order_by('-size')
        else:
            queryset = self.filter_queryset(self.get_queryset()).order_by('-size')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        # if idx:
        #     id_check = managing_models.SpecialPrice.objects.filter(customer_id=idx)
        #     if id_check.exists():
        #         has_list = id_check.values_list('product', flat=TabError)
        #         has_dic = id_check.values('product','new_price')
        #         for i in serializer.data:
        #             if i['id'] in has_list:
        #                 i['sell_price'] = has_dic.get(product=i['id'])['new_price']
        return Response(serializer.data)