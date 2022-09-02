from django.urls import path
from . import views as api_views

urlpatterns = [
    path('', api_views.api_overview, name='api-overview'),
    path('assets/list/', api_views.list_assets, name='list-asset'),
    path('auth/', api_views.api_auth_testing, name='auth-testing'),
    path('unauthenticated/', api_views.api_unauth, name='unauthenticated-page'),
]
