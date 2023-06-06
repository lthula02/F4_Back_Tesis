# from asyncio.windows_events import NULL
from rest_framework.views import APIView
from apps.metrics.helpers.manager import *
from apps.metrics.helpers.manager.manager import handleEditArchitecture, handleEditNode
from apps.metrics.helpers.combine_metrics_helper.combine_metrics import (
    handleCombineMetrics,
    handleCreateCompositeComponent,
)
from apps.metrics.helpers.combine_metrics_helper.composite_component_handler import (
    handleEditName,
    handleEditNodeCompositeComponent,
    handleCompositeComponentBoard,
    handleEditCompositeComponentDescription,
)

import jwt


# Create your views here.
class Metricas(APIView):
    def put(self, request, *args, **kwargs):
        token = request.data["token"]
        data = jwt.decode(token, "secret", algorithms=["HS256"])
        return handleEditArchitecture(data)


class CombineMetrics(APIView):
    def put(self, request, *args, **kwargs):
        return handleCombineMetrics(request.data["data"])


class CreateCompositeComponent(APIView):
    def put(self, request, *args, **kwargs):
        return handleCreateCompositeComponent(request.data["data"])


class EditNameCompositeComponent(APIView):
    def put(self, request):
        return handleEditName(request.data["data"])


class EditNodeCompositeComponent(APIView):
    def put(self, request):
        return handleEditNodeCompositeComponent(request.data["data"])


class EditNodeDescription(APIView):
    def put(self, request):
        return handleEditNode(request.data["data"])


class CreateCompositeComponentBoard(APIView):
    def put(self, request):
        return handleCompositeComponentBoard(request.data["data"])


class EditCompositeComponentDescription(APIView):
    def put(self, request):
        return handleEditCompositeComponentDescription(request.data["data"])
