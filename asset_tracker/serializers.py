from django.db.models import fields
from rest_framework import serializers

from users.models import CustomUser, Profile
from .models import Asset, AssetAssigned, AssetFeedback, AssetRequested


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['image']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser

        # exclude = ('password',)
        fields = ['username', 'email', 'about', 'groups', 'designation',
                  'objects', 'is_staff', 'is_active', 'start_date', ]
        depth = 1


class AssetListSerializer(serializers.ModelSerializer):
    created_by = UserSerializer()
    update_by = UserSerializer()

    class Meta:
        model = Asset
        depth = 2
        fields = '__all__'


class AssetAssignedListSerializer(serializers.ModelSerializer):
    created_by = UserSerializer()
    update_by = UserSerializer()
    assigned_to = UserSerializer()
    approved_by = UserSerializer()
    assigned_asset = AssetListSerializer()

    class Meta:
        model = AssetAssigned
        depth = 2
        fields = '__all__'


class AssetRequestedListSerializer(serializers.ModelSerializer):
    created_by = UserSerializer()
    update_by = UserSerializer()
    requested_by = UserSerializer()
    requested_to = UserSerializer()

    class Meta:
        model = AssetRequested
        depth = 2
        fields = '__all__'


class AssetFeedbackListSerializer(serializers.ModelSerializer):
    created_by = UserSerializer()
    update_by = UserSerializer()
    asset = AssetListSerializer()
    feedback_by = UserSerializer()

    class Meta:
        model = AssetFeedback
        depth = 2
        fields = '__all__'


class AssetCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = ('name', 'serial_number', 'model', 'amount', 'category', 'category_type',
                  'purchase_date', 'manufactured_date')


class AssetAssignedCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetAssigned
        fields = ('assigned_date', 'asset_status',
                  'assigned_to', 'approved_by')


class AssetRequestedCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetRequested
        fields = ('requested_date', 'requested_by',
                  'requested_to', 'manager_approval', 'reason',
                  'approval_status', 'request_needed', 'category',
                  'category_type')


class AssetFeedbackCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetFeedback
        fields = ('feedback_by', 'feedback_date',
                  'feedback', 'is_working', 'productivity_rating')
