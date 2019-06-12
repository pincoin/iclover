from rest_framework import serializers
from design import models as design_models
from member import models as member_models


class PaymentSerializer(serializers.Serializer):
    phone = serializers.CharField()
    tell = serializers.CharField()
    message = serializers.CharField()
