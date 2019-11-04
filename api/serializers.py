from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, User
from rest_framework import serializers
from member import models as member_models
from design import models as design_models
from managing import models as managing_models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'groups')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model= member_models.Profile
        fields = ('id','code','company','company_keyword','address','tax_bill_mail','tell','keywords','memo',
                  'phone','options','confirm','manager')

class ProductTextSerializer(serializers.ModelSerializer):
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

class OrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = design_models.CustomerOrderProduct
        fields = ('id','name','amount','sell')

class OrderInfoSerializer(serializers.ModelSerializer):
    order_list = OrderListSerializer(many=True,read_only=True)
    class Meta:
        model = design_models.CustomerOrderInfo
        fields = ('id','user', 'state','company','joo_date','order_list')


class CustomerMemoSerializer(serializers.ModelSerializer):
    class Meta:
        model= managing_models.CustomerMemo
        fields = ('keyword','memo','manager','confirm','hoo')

class CustomerProfileSerializer(serializers.ModelSerializer):
    customer_memo = CustomerMemoSerializer(many=True,read_only=True)
    user = serializers.CharField()
    class Meta:
        model= member_models.CustomerProfile
        fields = ('id','code','company','ceo','address','tax_bill_mail','tell','memo','bill_select','user',
                  'phone','address2','manager','address_detail','address_option','customer_memo')

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model= design_models.ProductPriceAPI
        fields = ('id','kind', 'title', 'size', 'paper', 'side','deal','option1','option2','supplier','memo','buy_price',
                  'size_text', 'paper_text', 'side_text', 'deal_text', 'option1_text', 'option2_text','sell')
