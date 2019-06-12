from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import viewsets
from member import models as member_models
from . import serializers
from django.db.models import Q
from rest_framework.permissions import IsAdminUser


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminUser,)
    queryset = get_user_model().objects.all().order_by('-date_joined')
    serializer_class = serializers.UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminUser,)
    queryset = Group.objects.all()
    serializer_class = serializers.GroupSerializer

class ProfileViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminUser,)
    queryset = member_models.Profile.objects.filter(~Q(state_select=1)).order_by('company')
    serializer_class = serializers.ProfileSerializer
