from rest_framework import serializers
from design import models as design_models
from member import models as member_models


class PaymentSerializer(serializers.Serializer):
    phone = serializers.CharField()
    tell = serializers.CharField()
    message = serializers.CharField()

class CustomerProfileSerializer(serializers.Serializer):
    customer_foreign = serializers.CharField(required=False)
    keyword = serializers.CharField(required=False)
    manager = serializers.CharField(required=False)
    memo = serializers.CharField(required=False)
    confirm = serializers.CharField(required=False)
    hoo = serializers.CharField(required=False)
    code = serializers.IntegerField(required=False)
    company = serializers.CharField(required=False)
    ceo = serializers.CharField(required=False)
    tax_bill_mail = serializers.CharField(required=False)
    sectors = serializers.CharField(required=False)
    business = serializers.CharField(required=False)
    sectors_category_foreign = serializers.CharField(required=False)
    tell = serializers.CharField(required=False)
    phone = serializers.CharField(required=False)
    address = serializers.CharField(required=False)
    address2 = serializers.CharField(required=False)
    address_detail = serializers.CharField(required=False)
    address_option = serializers.CharField(required=False)
    state = serializers.CharField(required=False)
    state_select = serializers.IntegerField(required=False)
    bill_select = serializers.IntegerField(required=False)