from rest_framework.views import APIView
from rest_framework.response import Response

# FIREBASE
from firebase_admin import credentials, db, initialize_app

# METRICS RELATED HANDLERS
from apps.helpers.manager.manager import (
    handleEditArchitecture,
)
from apps.helpers.metrics.combine_metrics import (
    handleCombineMetrics,
    handleCreateCompositeComponent,
)

# DIAGRAMS HANDLERS
from apps.helpers.diagrams.variability.variability import initVariabilityDiagram
from apps.helpers.diagrams.component_diag.compDiagram import initComponentDiagram

# PROJECT HANDLERS
from apps.helpers.proyectos.proyectos import (
    addNewProject,
    handleRemoveProject,
    handleEditProject,
)

# ARCHITECTURE HANDLERS
from apps.helpers.arquitecturas.arquitecturas import (
    createArchitecture,
    handleDeleteArchitecture,
    handleEditArchitectureName,
)

# VERSION HANDLERS
from apps.helpers.versiones.versiones import (
    createNewVersion,
    handleDeleteVersion,
    handleEditVersion,
)

# ELEMENTS HANDLERS
from apps.helpers.elementos.elementos import (
    handleEditNode,
    createElements,
    updatedElements,
)

# COMPOSITE COMPONENTS HANDLERS
from apps.helpers.elementos.composite_component_handler import (
    handleEditName,
    handleEditNodeCompositeComponent,
    handleCompositeComponentBoard,
    handleEditCompositeComponentDescription,
)

import jwt

cred = credentials.Certificate("./firebase-sdk.json")
initialize_app(
    cred,
    {
        "databaseURL": "https://cl-tesis-db-default-rtdb.firebaseio.com/",
    },
)

# 'https://tesis-carlos-vincent-default-rtdb.firebaseio.com/'
# 'https://test-tesis-dce1c-default-rtdb.firebaseio.com/


#
class Login(APIView):
    def post(self, request, *args, **kwargs):
        """Solicitud para inicio de sesión de un usuario o
        crear uno nuevo
        Returns
        -------
        list
            una lista con todos los proyectos del usuario
        """
        token = request.data["token"]
        user = jwt.decode(token, "secret", algorithms=["HS256"])
        user_id = str(user["userid"])
        try:
            user_ref = db.reference("/users/" + user_id)
            user_ref.update({"name": user["name"]})
            projects_ref = db.reference("/users/" + user_id + "/projects")
            return Response(projects_ref.get())
        except Exception as e:
            print(e)
            return Response(status=500)


class Proyectos(APIView):
    def post(self, request, *args, **kwargs):
        """Solicitud para agregar un nuevo proyecto
        a la base de datos del usuario
        Returns
        -------
        list
            una lista actualizada con todos los proyectos del usuario
        """

        token = request.data["token"]
        data = jwt.decode(token, "secret", algorithms=["HS256"])
        return addNewProject(data)

    def delete(self, request, *args, **kwargs):
        """Solicitud para eliminar un proyecto
        de la base de datos del usuario
        Returns
        -------
        list
            una lista actualizada con todos los proyectos del usuario
        """
        token = request.data["token"]
        data = jwt.decode(token, "secret", algorithms=["HS256"])
        return handleRemoveProject(data)

    def put(self, request, *args, **kwargs):
        """Solicitud para editar el nombre de un
        proyecto en la base de datos
        Returns
        -------
        list
            una lista actualizada con todos los proyectos del usuario
        """
        token = request.data["token"]
        data = jwt.decode(token, "secret", algorithms=["HS256"])
        projects = handleEditProject(data)
        return Response(projects)


class Arquitecturas(APIView):
    def post(self, request, *args, **kwargs):
        """Solicitud para agregar una nueva arquitectura
        a la base de datos del usuario

        Returns
        -------
        list
            una lista actualizada con todas las arquitecturas de un
            proyecto del usuario
        """
        data = request.data
        return createArchitecture(data)

    def delete(self, request, *args, **kwargs):
        """Solicitud para eliminar una arquitectura de un
        proyecto de la base de datos del usuario

        Returns
        -------
        list
            una lista actualizada con todas las arquitecturas de un
            proyecto del usuario
        """
        token = request.data["token"]
        data = jwt.decode(token, "secret", algorithms=["HS256"])
        return handleDeleteArchitecture(data)

    def put(self, request, *args, **kwargs):
        """Solicitud para editar el nombre de una arquitecturas
        de la base de datos del usuario

        Returns
        -------
        list
            una lista actualizada con todas las arquitecturas de un
            proyecto del usuario
        """
        token = request.data["token"]
        data = jwt.decode(token, "secret", algorithms=["HS256"])
        return handleEditArchitectureName(data)


class Versiones(APIView):
    def post(self, request, *args, **kwargs):
        """Solicitud para agregar una nueva versión
        a la base de datos del usuario

        Returns
        -------
        list
            una lista actualizada con todas las versiones de
            una arquitectura del usuario
        """
        data = request.data
        return createNewVersion(data)

    def delete(self, request, *args, **kwargs):
        """Solicitud para eliminar una versión de la
        base de datos del usuario

        Returns
        -------
        list
            una lista actualizada con todas las versiones de
            una arquitectura del usuario
        """
        token = request.data["token"]
        data = jwt.decode(token, "secret", algorithms=["HS256"])
        return handleDeleteVersion(data)

    def put(self, request, *args, **kwargs):
        """Solicitud para editar el nombre de una versión
        de la base de datos del usuario

        Returns
        -------
        list
            una lista actualizada con todas las versiones de
            una arquitectura del usuario
        """
        token = request.data["token"]
        data = jwt.decode(token, "secret", algorithms=["HS256"])
        return handleEditVersion(data)


class Elementos(APIView):
    def post(self, request, *args, **kwargs):
        """Solicitud para agregar elementos a la base
        de datos del usuario
        Returns
        -------
        list
            lista actualizada con todos los elementos de una
            versión del usuario
        """
        data = request.data
        elems = createElements(data)
        return Response(elems)


class UpdatedElements(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        elems = updatedElements(data)
        return Response(elems)


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


class CreateComponentDiagram(APIView):
    def put(self, request):
        return Response(initComponentDiagram(request.data["data"]))


class CreateVariabilityDiagram(APIView):
    def put(self, request):
        return Response(initVariabilityDiagram(request.data["data"]))


class CreateCompositeComponentBoard(APIView):
    def put(self, request):
        return handleCompositeComponentBoard(request.data["data"])


class EditCompositeComponentDescription(APIView):
    def put(self, request):
        return handleEditCompositeComponentDescription(request.data["data"])
