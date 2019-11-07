from rest_framework import serializers
from design import models as design_models
from member import models as member_models


class PaymentSerializer(serializers.Serializer):
    phone = serializers.CharField()
    tell = serializers.CharField()
    message = serializers.CharField()

class CustomerProfileSerializer(serializers.Serializer):
    keyword = serializers.CharField(required=False)
    manager = serializers.CharField(required=False)
    memo = serializers.CharField(required=False)
    confirm = serializers.CharField(required=False)
    hoo = serializers.CharField(required=False)
    user_id = serializers.CharField(required=False)
    company = serializers.CharField(required=False)
    ceo = serializers.CharField(required=False)
    tax_bill_mail = serializers.CharField(required=False)
    inside_memo = serializers.CharField(required=False)
    show_memo = serializers.CharField(required=False)
    json_data = serializers.CharField(required=False)
    tell = serializers.CharField(required=False)
    phone = serializers.CharField(required=False)
    address = serializers.CharField(required=False)
    address2 = serializers.CharField(required=False)
    address_detail = serializers.CharField(required=False)
    address_option = serializers.CharField(required=False)
    state = serializers.CharField(required=False)
    state_select = serializers.IntegerField(required=False)
    bill_select = serializers.IntegerField(required=False)
    order_date = serializers.CharField(required=False)
    joo_date = serializers.CharField(required=False)
    tax_bool = serializers.BooleanField(required=False)
    delete_num = serializers.CharField(required=False)