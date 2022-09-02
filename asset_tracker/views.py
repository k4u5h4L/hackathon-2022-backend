from django.shortcuts import render

from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from ratelimit.decorators import ratelimit
from django.contrib.auth.decorators import login_required

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
@login_required
@ratelimit(key='ip', rate='500/h')
def api_auth_testing(request):
    message = {
        'message': 'authenticated',
    }

    return Response(message)
