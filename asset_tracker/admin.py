from django.contrib import admin

from asset_tracker.models import Asset, AssetAssigned, AssetRequested, AssetFeedback
# Register your models here.


# admin stuff
name = "Asset-Tracker"
admin.site.site_header = f"{name} Admin"
admin.site.site_title = f"{name} Admin Portal"
admin.site.index_title = f"Welcome to {name} Portal"


admin.site.register(Asset)
admin.site.register(AssetAssigned)
admin.site.register(AssetRequested)
admin.site.register(AssetFeedback)
