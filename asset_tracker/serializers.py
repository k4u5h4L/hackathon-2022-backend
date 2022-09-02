from django.db.models import fields
from rest_framework import serializers

from users.models import CustomUser, Profile
from .models import Asset


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['image']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser

        # exclude = ('password',)
        fields = ['username', 'email', 'about', 'groups']
        depth = 1


class AssetSerializer(serializers.ModelSerializer):
    created_by = UserSerializer()
    update_by = UserSerializer()

    class Meta:
        model = Asset
        depth = 2
        fields = ('name', 'serial_number', 'model', 'amount', 'category', 'category_type',
                  'purchase_date', 'manufactured_date', 'created_by', 'update_by')
