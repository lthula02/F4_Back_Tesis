"""tesis_back URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import include, re_path
from django.contrib import admin
from apps.views import (
    # METRICS
    CombineMetrics,
    Metricas,
    # NODE AND COMPOSITE COMPONENTS
    EditNodeDescription,
    CreateCompositeComponent,
    EditNameCompositeComponent,
    EditNodeCompositeComponent,
    CreateCompositeComponentBoard,
    EditCompositeComponentDescription,
    # DIAGRAMS
    CreateClassDiagram,
    CreateComponentDiagram,
    CreateVariabilityDiagram,
    # CORE
    Login,
    Proyectos,
    Arquitecturas,
    Versiones,
    Elementos,
    UpdatedElements,
)

urlpatterns = [
    re_path(r"^admin/", admin.site.urls),
    re_path(r"^api-auth/", include("rest_framework.urls")),
    re_path(r"^login/", Login.as_view(), name="login"),
    re_path(r"^proyectos/", Proyectos.as_view(), name="proyectos"),
    re_path(r"^arquitecturas/", Arquitecturas.as_view(), name="arquitecturas"),
    re_path(r"^version/", Versiones.as_view(), name="version"),
    re_path(r"^elementos/", Elementos.as_view(), name="elementos"),
    re_path(r"^updated-elements/", UpdatedElements.as_view(), name="updated_elements"),
    re_path(r"^metricas/", Metricas.as_view(), name="metricas"),
    re_path(r"^combine-metrics/", CombineMetrics.as_view(), name="combine_metrics"),
    re_path(
        r"^composite-component/",
        CreateCompositeComponent.as_view(),
        name="composite_component",
    ),
    re_path(
        r"^edit_cc_name/", EditNameCompositeComponent.as_view(), name="edit_cc_name"
    ),
    re_path(
        r"^edit_node_cc/", EditNodeCompositeComponent.as_view(), name="edit_node_cc"
    ),
    re_path(r"^edit_node_desc/", EditNodeDescription.as_view(), name="edit_node_desc"),
    re_path(
        r"^create_class_diagram/",
        CreateClassDiagram.as_view(),
        name="create_class_diagram",
    ),
    re_path(
        r"^create_comp_diagram/",
        CreateComponentDiagram.as_view(),
        name="create_comp_diagram",
    ),
    re_path(
        r"^create_var_diagram/",
        CreateVariabilityDiagram.as_view(),
        name="create_var_diagram",
    ),
    re_path(
        r"^create_cc_board/",
        CreateCompositeComponentBoard.as_view(),
        name="create_cc_board",
    ),
    re_path(
        r"^edit_cc_description/",
        EditCompositeComponentDescription.as_view(),
        name="edit_cc_description",
    ),
]
