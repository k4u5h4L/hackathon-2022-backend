from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from asset_tracker.serializers import UserSerializer
from .serializers import CustomUserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ratelimit.decorators import ratelimit
from rest_framework import status
from django.contrib.auth.decorators import login_required

from .models import Profile

# Create your views here.


@api_view(['GET'])
@login_required
@ratelimit(key='ip', rate='500/h')
def get_user(request):
    user = UserSerializer(instance=request.user)

    return Response(user.data)


class CustomUserCreate(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format='json'):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                json = serializer.data
                p = Profile(user=user)
                p.save()
                print(f'Profile saved for user {user}')
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlacklistTokenUpdateView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = ()

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
