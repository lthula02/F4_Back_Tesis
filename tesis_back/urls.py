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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from apps.metrics.views import CombineMetrics, Metricas, CreateCompositeComponent, EditNameCompositeComponent, EditNodeCompositeComponent, CreateCompositeComponentBoard, EditCompositeComponentDescription
from core.views import Login, Proyectos, Arquitecturas, Versiones, Elementos, UpdatedElements

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('login/', Login.as_view(), name='login'),
    path('proyectos/', Proyectos.as_view(), name='proyectos'),
    path('arquitecturas/', Arquitecturas.as_view(), name='arquitecturas'),
    path('version/', Versiones.as_view(), name='version'),
    path('elementos/', Elementos.as_view(), name='elementos'),
     path('updated-elements/', UpdatedElements.as_view(), name='updated_elements'),
    path('metricas/', Metricas.as_view(), name='metricas'),
    path('combine-metrics/', CombineMetrics.as_view(), name='combine_metrics'),
    path('composite-component/', CreateCompositeComponent.as_view(), name= 'composite_component'),
    path('edit_cc_name/', EditNameCompositeComponent.as_view(), name= 'edit_cc_name'),
    path('edit_node_cc/', EditNodeCompositeComponent.as_view(), name= 'edit_node_cc'),
    path('create_cc_board/', CreateCompositeComponentBoard.as_view(), name= 'create_cc_board'),
    path('edit_cc_description/', EditCompositeComponentDescription.as_view(), name= 'edit_cc_description'),

]



