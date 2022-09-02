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


class AssetListSerializer(serializers.ModelSerializer):
    created_by = UserSerializer()
    update_by = UserSerializer()

    class Meta:
        model = Asset
        depth = 2
        fields = '__all__'


class AssetCreateSerializer(serializers.ModelSerializer):
    # created_by = serializers.PrimaryKeyRelatedField(
    #     read_only=True, default=serializers.CurrentUserDefault())
    # update_by = serializers.PrimaryKeyRelatedField(
    #     read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Asset
        fields = ('name', 'serial_number', 'model', 'amount', 'category', 'category_type',
                  'purchase_date', 'manufactured_date')
