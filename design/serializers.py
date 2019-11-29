from rest_framework import serializers
from design import models as design_models
from member import models as member_models


class PaymentSerializer(serializers.Serializer):
    size = serializers.CharField()
    paper = serializers.CharField()
    side = serializers.CharField()
    deal = serializers.CharField()
    amount = serializers.CharField()


class CartProductSerializer(serializers.Serializer):
    title = serializers.CharField()
    kind = serializers.CharField()
    size = serializers.CharField()
    size_text = serializers.CharField()
    paper = serializers.CharField()
    paper_text = serializers.CharField()
    side = serializers.CharField()
    side_text = serializers.CharField()
    deal = serializers.CharField()
    deal_text = serializers.CharField()
    amount = serializers.IntegerField()
    price = serializers.CharField()
    memo = serializers.CharField(required=False)
    delivery = serializers.CharField()