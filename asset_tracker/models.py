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
        max_length=10,
        choices=Category.choices,
        default=Category.LAPTOP,
    )
    category_type = models.CharField(
        max_length=20
    )
    purchase_date = models.DateTimeField()
    manufactured_date = models.DateTimeField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(to=CustomUser, on_delete=models.DO_NOTHING)
    update_at = models.DateTimeField(auto_now=True)
    update_by = models.ForeignKey(to=CustomUser, on_delete=models.DO_NOTHING)
    
    def __str__(self):
        return self.name

class AssetAssigned(models.Model):
    assigned_asset = models.ForeignKey(Asset, on_delete=models.DO_NOTHING)
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    assigned_date = models.DateTimeField()
    approved_by = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    asset_status = models.CharField(
        max_length=10,
        choices=AssetStatus.choices,
        default=AssetStatus.IN_STOCK,
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(to=CustomUser, on_delete=models.DO_NOTHING)
    update_at = models.DateTimeField(auto_now=True)
    update_by = models.ForeignKey(to=CustomUser, on_delete=models.DO_NOTHING)
    
    def __str__(self):
        return f'Asset Assigned : {self.assigned_asset} To {self.assigned_to} on {self.assigned_date}'


class AssetRequested(models.Model):
    requested_date = models.DateTimeField()
    requested_by = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    requested_to = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    manager_approval = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    reason = models.CharField(max_length=100)
    approval_status = models.CharField(
        max_length=10,
        choices=ApprovalStatus.choices,
        default=ApprovalStatus.PENDING,
    )
    request_needed = models.CharField(
        max_length=10,
        choices=RequestedNeeded.choices,
        default=RequestedNeeded.NEW,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(to=CustomUser, on_delete=models.DO_NOTHING)
    update_at = models.DateTimeField(auto_now=True)
    update_by = models.ForeignKey(to=CustomUser, on_delete=models.DO_NOTHING)
    
    def __str__(self):
        return f'Asset Requested by : {self.requested_by}'

class AssetFeedback(models.Model):
    def validate_productivity_rating(productivity_rating):
        if not 0 < productivity_rating < 5:
            raise ValidationError(f'Rating needs to be in rang (0,5) found : {productivity_rating}')
    
    asset = models.ForeignKey(Asset, on_delete=models.DO_NOTHING)
    feedback_by = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    feedback_date = models.DateTimeField()
    feedback = models.CharField(max_length=100)
    is_working = models.CharField(max_length=100)
    productivity_rating = models.IntegerField(validators=[validate_productivity_rating])
    
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(to=CustomUser, on_delete=models.DO_NOTHING)
    update_at = models.DateTimeField(auto_now=True)
    update_by = models.ForeignKey(to=CustomUser, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'Feedback : {self.feedback} To {self.asset}'
    
    
