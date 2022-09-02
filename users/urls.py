from django.urls import path
from .views import CustomUserCreate, BlacklistTokenUpdateView, get_user

app_name = 'users'

urlpatterns = [
    path('register/', CustomUserCreate.as_view(), name='create-user'),
    path('logout/blacklist/', BlacklistTokenUpdateView.as_view(),
         name='blacklist'),
    path('', get_user, name='get-user')
]
