from django.urls import path
from . import views as api_views

urlpatterns = [
    path('', api_views.api_overview, name='api-overview'),
    path('auth/', api_views.api_auth_testing, name='auth-testing'),
    path('unauthenticated/', api_views.api_unauth, name='unauthenticated-page'),
]
