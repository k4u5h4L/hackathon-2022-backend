from django.urls import path
from . import views as api_views

urlpatterns = [
    path('', api_views.api_overview, name='api-overview'),
    path('auth/', api_views.api_auth_testing, name='auth-testing'),
    path('unauthenticated/', api_views.api_unauth, name='unauthenticated-page'),
    path('assets/list/', api_views.list_assets, name='list-asset'),
    path('assets/create/', api_views.create_assets, name='create-asset'),
    path('assets/update/<int:id>/', api_views.update_assets, name='update-asset'),
    path('assets/delete/<int:id>/', api_views.delete_assets, name='delete-asset'),
]
