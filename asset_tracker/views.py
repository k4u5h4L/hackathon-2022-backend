from django.shortcuts import render

from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from ratelimit.decorators import ratelimit
from rest_framework import status
from django.contrib.auth.decorators import login_required

from asset_tracker.models import Asset
from asset_tracker.serializers import AssetCreateSerializer, AssetListSerializer

# Create your views here.

cache_timeout = 60


@api_view(['GET'])
@ratelimit(key='ip', rate='500/h')
def api_overview(request):
    api_urls = {
        'Foo': '/bar',
        'test': '/testing',
    }

    return Response(api_urls)


@api_view(['GET'])
@ratelimit(key='ip', rate='500/h')
def api_unauth(request):
    message = {
        'message': 'unauthenticated',
        'status': 401
    }

    return Response(message)


@api_view(['GET'])
@login_required
@ratelimit(key='ip', rate='500/h')
def api_auth_testing(request):
    user = request.user

    message = {
        'message': 'authenticated',
        'user': user.email
    }

    return Response(message)


@api_view(['GET'])
@login_required
@ratelimit(key='ip', rate='500/h')
def list_assets(request):
    assets = Asset.objects.all().order_by('-id')

    serializer = AssetListSerializer(assets, many=True)

    return Response(serializer.data)


@api_view(['POST'])
@login_required
@ratelimit(key='ip', rate='500/h')
def create_assets(request):
    asset = AssetCreateSerializer(data=request.data)

    if asset.is_valid():
        asset.save(created_by=request.user, update_by=request.user)
        return Response(asset.data, status=status.HTTP_201_CREATED)
    else:
        print(asset.errors)
        return Response(status=status.HTTP_400_BAD_REQUEST)
