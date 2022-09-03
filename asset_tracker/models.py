from datetime import datetime, date
from django.db import models
from django.core.exceptions import ValidationError

from asset_tracker.enums.approval_status import ApprovalStatus
from asset_tracker.enums.asset_status import AssetStatus
from asset_tracker.enums.category import Category
from asset_tracker.enums.requested_needed import RequestedNeeded
from users.models import CustomUser

# Create your models here.


class Asset(models.Model):
    name = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    amount = models.IntegerField(default=0)
    category = models.CharField(
        max_length=20,
        choices=Category.choices(),
        default=Category.LAPTOP,
    )
    category_type = models.CharField(
        max_length=20,
        default=Category.LAPTOP,
    )
    purchase_date = models.DateField(default=date.today)
    manufactured_date = models.DateField(default=date.today)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        to=CustomUser, on_delete=models.DO_NOTHING, related_name='asset_created_by')
    update_at = models.DateTimeField(auto_now=True)
    update_by = models.ForeignKey(
        to=CustomUser, on_delete=models.DO_NOTHING, related_name='asset_updated_by')

    def __str__(self):
        return self.name


class AssetAssigned(models.Model):
    assigned_asset = models.ForeignKey(to=Asset, on_delete=models.DO_NOTHING)
    assigned_to = models.ForeignKey(
        to=CustomUser, on_delete=models.DO_NOTHING, related_name='asset_assigned_to')
    assigned_date = models.DateField(default=date.today)
    approved_by = models.ForeignKey(
        to=CustomUser, on_delete=models.DO_NOTHING, related_name='asset_approved_by')
    asset_status = models.CharField(
        max_length=20,
        choices=AssetStatus.choices(),
        default=AssetStatus.IN_STOCK,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        to=CustomUser, on_delete=models.DO_NOTHING, related_name='asset_assigned_created_by')
    update_at = models.DateTimeField(auto_now=True)
    update_by = models.ForeignKey(
        to=CustomUser, on_delete=models.DO_NOTHING, related_name='asset_assigned_update_by')

    def __str__(self):
        return f'Asset Assigned : {self.assigned_asset} To {self.assigned_to} on {self.assigned_date}'


class AssetRequested(models.Model):
    requested_date = models.DateField(default=date.today)
    requested_by = models.ForeignKey(
        to=CustomUser, on_delete=models.DO_NOTHING, related_name='asset_requested_by')
    requested_to = models.ForeignKey(
        to=CustomUser, on_delete=models.DO_NOTHING, related_name='asset_requested_to')
    manager_approval = models.BooleanField(default=False)
    reason = models.CharField(max_length=100)
    approval_status = models.CharField(
        max_length=10,
        choices=ApprovalStatus.choices(),
        default=ApprovalStatus.PENDING,
    )
    request_needed = models.CharField(
        max_length=10,
        choices=RequestedNeeded.choices(),
        default=RequestedNeeded.NEW,
    )

    category = models.CharField(
        max_length=20,
        choices=Category.choices(),
        default=Category.LAPTOP,
    )
    category_type = models.CharField(
        max_length=20,
        default=Category.LAPTOP,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        to=CustomUser, on_delete=models.DO_NOTHING, related_name='asset_request_created_by')
    update_at = models.DateTimeField(auto_now=True)
    update_by = models.ForeignKey(
        to=CustomUser, on_delete=models.DO_NOTHING, related_name='asset_request_update_by')

    def __str__(self):
        return f'Asset Requested by : {self.requested_by}'


class AssetFeedback(models.Model):
    def validate_productivity_rating(productivity_rating):
        if not 0 < productivity_rating <= 5:
            raise ValidationError(
                f'Rating needs to be in rang (1,5) found : {productivity_rating}')

    asset = models.ForeignKey(to=Asset, on_delete=models.DO_NOTHING)
    feedback_by = models.ForeignKey(
        to=CustomUser, on_delete=models.DO_NOTHING, related_name='asset_feedback_by')
    feedback_date = models.DateField(default=date.today)
    feedback = models.CharField(max_length=100)
    is_working = models.CharField(max_length=100)
    productivity_rating = models.IntegerField(
        validators=[validate_productivity_rating])

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        to=CustomUser, on_delete=models.DO_NOTHING, related_name='asset_feedback_created_by')
    update_at = models.DateTimeField(auto_now=True)
    update_by = models.ForeignKey(
        to=CustomUser, on_delete=models.DO_NOTHING, related_name='asset_feedback_update_by')

    def __str__(self):
        return f'Feedback : {self.feedback} To {self.asset}'
