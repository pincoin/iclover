from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, User
from rest_framework import serializers
from member import models as member_models
from design import models as design_models
from managing import models as managing_models


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model= member_models.Profile
        fields = ('id','code','company','company_keyword','address','tax_bill_mail','tell','keywords','memo',
                  'phone','options','confirm','manager')

class ProductTextSerializer(serializers.HyperlinkedModelSerializer):
    company_name = serializers.SerializerMethodField()

    class Meta:
        model= design_models.ProductText
        fields = ('id','quantity','buy_price','sell_price','standard','paper','paper_option','product_version','title',
                  'memo','gram','code','etc','horizontal','vertical','width','height','supplier','company_name',
                  )

    def get_company_name(self, obj):
        company_name = ''
        if obj.supplier:
            company_name = obj.supplier.username.split('_')[-2]
        return company_name

class SpecialPriceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model= managing_models.SpecialPrice
        fields = '__all__'


