from rest_framework import serializers
from design import models as design_models
from member import models as member_models


class PaymentSerializer(serializers.Serializer):
    size = serializers.CharField()
    paper = serializers.CharField()
    side = serializers.CharField()
    deal = serializers.CharField()


class CartProductSerializer(serializers.Serializer):
    title = serializers.CharField()
    size = serializers.CharField()
    paper = serializers.CharField()
    side = serializers.CharField()
    deal = serializers.CharField()
    price = serializers.CharField()