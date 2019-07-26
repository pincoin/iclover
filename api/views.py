from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import viewsets
from member import models as member_models
from design import models as design_models
from managing import models as managing_models
from . import serializers
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
        queryset = self.queryset.prefetch_related('user').filter(~Q(state_select=1)).order_by('company')
        for i in queryset:
            i.id = i.user.id
        return queryset

class ProductTextViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminUser,)
    queryset = design_models.ProductText.objects.all().filter(Q(product_version=1)).order_by('-standard')
    serializer_class = serializers.ProductTextSerializer

    def get_queryset(self):
        queryset = self.queryset
        for i in queryset:
            if not i.horizontal:
                i.horizontal = 0
            if not i.vertical:
                i.vertical = 0
            if not i.sell_price:
                i.sell_price = 0
            if not i.buy_price:
                i.buy_price = 0
            try:
                i.etc = i.etc.strip()
            except:
                pass
            if i.etc == None:
                i.etc = ''
            if i.gram == None:
                i.gram = ''
            if i.memo == None:
                i.memo = ''
        return queryset

class SpecialPriceViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminUser,)
    queryset = managing_models.SpecialPrice.objects.all()
    serializer_class = serializers.SpecialPriceSerializer

    def get_queryset(self):
        get_data = self.request.GET
        try:
            queryset = self.queryset.filter(customer_id =get_data['data'])
        except:
            return {}
        return queryset
