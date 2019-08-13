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
        print(keyword, idx)
        if keyword:
            keyword = keyword.split()
            query = reduce(operator.and_,(Q(company__icontains=item) for item in keyword))
            query1 = reduce(operator.and_, (Q(company_keyword__icontains=item) for item in keyword))
            queryset = self.filter_queryset(self.get_queryset()).filter(query|query1).order_by('company')
        else:
            queryset = self.filter_queryset(self.get_queryset()).order_by('-id')
        page = self.paginate_queryset(queryset)
        # for i in page:
        #     i.id = i.user.id
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class SpecialPriceViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminUser,)
    queryset = managing_models.SpecialPrice.objects.all()
    serializer_class = serializers.SpecialPriceSerializer

    def get_queryset(self):
        get_data = self.request.GET
        try:
            queryset = self.queryset.filter(customer_id =get_data['data']).order_by('product')
        except:
            return {}
        return queryset
