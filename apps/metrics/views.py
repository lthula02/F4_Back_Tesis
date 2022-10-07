# from asyncio.windows_events import NULL
from django.shortcuts import render
from rest_framework import status as status_response
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.metrics.helpers.manager import *
from .helpers.manager.manager import handleEditArchitecture

# Create your views here.
class Metricas(APIView):

    def put(self, request, *args, **kwargs):
        return handleEditArchitecture(request.data)
        



