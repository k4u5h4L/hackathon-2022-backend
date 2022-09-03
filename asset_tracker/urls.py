from django.urls import path
from . import views as api_views

urlpatterns = [
    path('', api_views.api_overview, name='api-overview'),
    path('auth/', api_views.api_auth_testing, name='auth-testing'),
    path('unauthenticated/', api_views.api_unauth, name='unauthenticated-page'),

    path('assets/<int:id>/', api_views.get_asset, name='get-asset'),
    path('assets/list/', api_views.list_assets, name='list-asset'),
    path('assets/create/', api_views.create_assets, name='create-asset'),
    path('assets/update/<int:id>/', api_views.update_assets, name='update-asset'),
    path('assets/delete/<int:id>/', api_views.delete_assets, name='delete-asset'),

    path('assets-assigned/list/', api_views.list_current_assets_assigned_to_user,
         name='list_current_assets_assigned_to_user'),
    path('assets-assigned/list/all/', api_views.list_assets_assigned,
         name='list-asset-assigned'),
    path('assets-assigned/create/<int:asset_id>/', api_views.create_assets_assigned,
         name='create-asset-assigned'),
    path('assets-assigned/update/<int:id>/<int:asset_id>/',
         api_views.update_assets_assigned, name='update-asset-assigned'),
    path('assets-assigned/delete/<int:id>/',
         api_views.delete_assets_assigned, name='delete-asset-assigned'),

    path('assets-requested/list/', api_views.list_assets_requested,
         name='list-asset-requested'),
    path('assets-requested/create/', api_views.create_assets_requested,
         name='create-asset-requested'),
    path('assets-requested/update/<int:id>/',
         api_views.update_assets_requested, name='update-asset-requested'),
    path('assets-requested/delete/<int:id>/',
         api_views.delete_assets_requested, name='delete-asset-requested'),

    path('assets-feedback/list/', api_views.list_assets_feedback,
         name='list-asset-feedback'),
    path('assets-feedback/create/<int:asset_id>/', api_views.create_assets_feedback,
         name='create-asset-feedback'),
    path('assets-feedback/update/<int:id>/<int:asset_id>/',
         api_views.update_assets_feedback, name='update-asset-feedback'),
    path('assets-feedback/delete/<int:id>/',
         api_views.delete_assets_feedback, name='delete-asset-feedback'),
]
