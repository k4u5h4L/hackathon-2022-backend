from django.shortcuts import render

from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from ratelimit.decorators import ratelimit
from rest_framework import status
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail

from asset_tracker.models import Asset, AssetAssigned, AssetFeedback, AssetRequested
from asset_tracker.serializers import AssetAssignedCreateSerializer, AssetCreateSerializer, AssetFeedbackCreateSerializer, AssetFeedbackListSerializer, AssetListSerializer, AssetAssignedListSerializer, AssetRequestedCreateSerializer, AssetRequestedListSerializer
from server import settings

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


@api_view(['POST'])
@login_required
@ratelimit(key='ip', rate='500/h')
def update_assets(request, id):
    try:
        data = Asset.objects.get(id=id)
    except Asset.DoesNotExist:
        return Response({'detail': 'No items with that ID exist'}, status=status.HTTP_404_NOT_FOUND)

    asset = AssetCreateSerializer(instance=data, data=request.data)

    if asset.is_valid():
        asset.save(created_by=request.user, update_by=request.user)
        return Response(asset.data, status=status.HTTP_200_OK)
    else:
        print(asset.errors)
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE'])
@login_required
@ratelimit(key='ip', rate='500/h')
def delete_assets(request, id):
    try:
        asset = Asset.objects.get(id=id)
    except Asset.DoesNotExist:
        return Response({'detail': 'No items with that ID exist'}, status=status.HTTP_404_NOT_FOUND)

    try:
        asset.delete()
        return Response({'detail': 'Item deleted'}, status=status.HTTP_200_OK)
    except Exception:
        print(asset.errors)
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@login_required
@ratelimit(key='ip', rate='500/h')
def list_assets_assigned(request):
    assets_assigned = AssetAssigned.objects.all().order_by('-id')

    serializer = AssetAssignedListSerializer(assets_assigned, many=True)

    return Response(serializer.data)


@api_view(['POST'])
@login_required
@ratelimit(key='ip', rate='500/h')
def create_assets_assigned(request, asset_id):
    try:
        asset = Asset.objects.get(id=asset_id)
    except Asset.DoesNotExist:
        return Response({'detail': 'No items with that ID exist'}, status=status.HTTP_404_NOT_FOUND)

    asset_assigned = AssetAssignedCreateSerializer(data=request.data)

    if asset_assigned.is_valid():
        asset_assigned.save(created_by=request.user,
                            update_by=request.user, assigned_asset=asset)
        return Response(asset_assigned.data, status=status.HTTP_201_CREATED)
    else:
        print(asset_assigned.errors)
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@login_required
@ratelimit(key='ip', rate='500/h')
def update_assets_assigned(request, id, asset_id):
    try:
        asset = Asset.objects.get(id=asset_id)
    except Asset.DoesNotExist:
        return Response({'detail': 'No Assets with that ID exist'}, status=status.HTTP_404_NOT_FOUND)

    try:
        data = AssetAssigned.objects.get(id=id)
    except AssetAssigned.DoesNotExist:
        return Response({'detail': 'No AssetsAssigned with that ID exist'}, status=status.HTTP_404_NOT_FOUND)

    asset_assigned = AssetAssignedCreateSerializer(
        instance=data, data=request.data)

    if asset_assigned.is_valid():
        asset_assigned.save(created_by=request.user,
                            update_by=request.user, assigned_asset=asset)
        return Response(asset_assigned.data, status=status.HTTP_200_OK)
    else:
        print(asset_assigned.errors)
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE'])
@login_required
@ratelimit(key='ip', rate='500/h')
def delete_assets_assigned(request, id):
    try:
        asset = AssetAssigned.objects.get(id=id)
    except AssetAssigned.DoesNotExist:
        return Response({'detail': 'No items with that ID exist'}, status=status.HTTP_404_NOT_FOUND)

    try:
        asset.delete()
        return Response({'detail': 'Item deleted'}, status=status.HTTP_200_OK)
    except Exception:
        print(asset.errors)
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@login_required
@ratelimit(key='ip', rate='500/h')
def list_assets_requested(request):
    assets = AssetRequested.objects.all().order_by('-id')

    serializer = AssetRequestedListSerializer(assets, many=True)

    return Response(serializer.data)


@api_view(['POST'])
@login_required
@ratelimit(key='ip', rate='500/h')
def create_assets_requested(request):
    asset = AssetRequestedCreateSerializer(data=request.data)

    if asset.is_valid():
        asset.save(created_by=request.user, update_by=request.user)
        return Response(asset.data, status=status.HTTP_201_CREATED)
    else:
        print(asset.errors)
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@login_required
@ratelimit(key='ip', rate='500/h')
def update_assets_requested(request, id):
    try:
        data = AssetRequested.objects.get(id=id)
    except AssetRequested.DoesNotExist:
        return Response({'detail': 'No items with that ID exist'}, status=status.HTTP_404_NOT_FOUND)

    asset = AssetRequestedCreateSerializer(instance=data, data=request.data)

    if asset.is_valid():
        asset.save(created_by=request.user, update_by=request.user)
        return Response(asset.data, status=status.HTTP_200_OK)
    else:
        print(asset.errors)
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE'])
@login_required
@ratelimit(key='ip', rate='500/h')
def delete_assets_requested(request, id):
    try:
        asset = AssetRequested.objects.get(id=id)
    except AssetRequested.DoesNotExist:
        return Response({'detail': 'No items with that ID exist'}, status=status.HTTP_404_NOT_FOUND)

    try:
        asset.delete()
        return Response({'detail': 'Item deleted'}, status=status.HTTP_200_OK)
    except Exception:
        print(asset.errors)
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@login_required
@ratelimit(key='ip', rate='500/h')
def list_assets_feedback(request):
    assets = AssetFeedback.objects.all().order_by('-id')

    serializer = AssetFeedbackListSerializer(assets, many=True)

    return Response(serializer.data)


@api_view(['POST'])
@login_required
@ratelimit(key='ip', rate='500/h')
def create_assets_feedback(request, asset_id):
    try:
        asset = Asset.objects.get(id=asset_id)
    except Asset.DoesNotExist:
        return Response({'detail': 'No items with that ID exist'}, status=status.HTTP_404_NOT_FOUND)

    asset_feedback = AssetFeedbackCreateSerializer(data=request.data)

    if asset_feedback.is_valid():
        asset_feedback.save(created_by=request.user,
                            update_by=request.user, asset=asset)
        return Response(asset_feedback.data, status=status.HTTP_201_CREATED)
    else:
        print(asset_feedback.errors)
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@login_required
@ratelimit(key='ip', rate='500/h')
def update_assets_feedback(request, id, asset_id):
    try:
        data = Asset.objects.get(id=asset_id)
    except Asset.DoesNotExist:
        return Response({'detail': 'No Assets with that ID exist'}, status=status.HTTP_404_NOT_FOUND)

    try:
        asset = AssetFeedback.objects.get(id=id)
    except AssetFeedback.DoesNotExist:
        return Response({'detail': 'No AssetFeedback with that ID exist'}, status=status.HTTP_404_NOT_FOUND)

    asset_feedback = AssetFeedbackCreateSerializer(
        instance=data, data=request.data)

    if asset_feedback.is_valid():
        asset_feedback.save(created_by=request.user,
                            update_by=request.user, asset=asset)
        return Response(asset_feedback.data, status=status.HTTP_200_OK)
    else:
        print(asset_feedback.errors)
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE'])
@login_required
@ratelimit(key='ip', rate='500/h')
def delete_assets_feedback(request, id):
    try:
        asset = AssetFeedback.objects.get(id=id)
    except AssetFeedback.DoesNotExist:
        return Response({'detail': 'No items with that ID exist'}, status=status.HTTP_404_NOT_FOUND)

    try:
        asset.delete()
        return Response({'detail': 'Item deleted'}, status=status.HTTP_200_OK)
    except Exception:
        print(asset.errors)
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@ratelimit(key='ip', rate='500/h')
def send_email_to_user(request, email):
    print(f"sending email to {email}")

    try:
        send_mail(
            'Test subject',
            'Test email message.',
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )

        return Response({'detail': 'Email sent'})
    except Exception as e:
        print(e)
        return Response({'detail': f'failed to send email to {email}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
