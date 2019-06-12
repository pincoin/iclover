from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, User
from rest_framework import serializers
from member import models as member_models


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model= member_models.Profile
        fields = ['id','code','company','company_keyword','address','tax_bill_mail','tell','keywords','memo',
                  'phone','options','confirm','manager']

