from apps.helpers.metrics.coupling_helper.coupling import calculate_coupling
from apps.helpers.metrics.abstractness_helper.abstractness import calculate_abstractness
from apps.helpers.metrics.instability_helper.instability import calculate_instability
from apps.helpers.metrics.dms_helper.dms import calculate_dms
from apps.helpers.metrics.package_mapping_helper.package_mapping import (
    calculate_package_mapping,
)
from apps.helpers.metrics.name_ressemblance_helper.name_ressemblance import (
    claculate_nameResemblance,
)

from firebase_admin import db
from rest_framework.response import Response

"""
manager.py se encarga de centralizar todo el proceso para 'CALCULAR METRICAS'

Los nombres de las funciones se deben a que se actualiza la arquitectura en
base a los valores calculados, y se muestran en las tablas
"""


def handleEditArchitecture(data):
    uid = data["user_id"]
    project_index = data["project_index"]
    arch_index = int(data["arch_index"])
    version_index = data["ver_index"]
    name_ressemblance_umbral = data["name_ressemblance_umbral"]

    url = "/users/" + uid + "/projects/" + str(project_index)

    try:
        architectures = editArchitecture(
            url, arch_index, version_index, name_ressemblance_umbral
        )

        return Response(data=architectures)
    except:
        return Response(data=None, status=500)


def editArchitecture(url, archIndex, versionIndex, name_ressemblance_umbral):
    arch_ref = db.reference(url + "/architectures")
    arch_arr = arch_ref.get()

    # elements = arch_arr[int(archIndex)]['versions'][int(versionIndex)]['elements']

    nodes = arch_arr[int(archIndex)]["versions"][int(versionIndex)]["elements"]["nodes"]

    edges = arch_arr[int(archIndex)]["versions"][int(versionIndex)]["elements"]["edges"]

    calculate_metrics(nodes, edges, name_ressemblance_umbral)
    arch_arr[int(archIndex)]["versions"][int(versionIndex)]["elements"]["edges"] = edges
    arch_arr[int(archIndex)]["versions"][int(versionIndex)]["elements"]["nodes"] = nodes

    project_ref = db.reference(url)

    project_ref.update({"architectures": arch_arr})
    return arch_arr


def calculate_metrics(nodes, edges, name_ressemblance_umbral):
    """Se llaman todos los métodos correspondientes al cálculo de métricas

    Parameters
    ----------
    nodes: list
        lista con todos los nodos de la arquitectura
    edges: list
        lista con todas las aristas de la arquitectura
    """
    # se crea el json vacio 'metrics' para cada relacion
    add_metric_json(edges)
    # incompleteResources
    inComplete_nodes_properties(nodes)
    # Coupling
    calculate_coupling(nodes, edges)
    # Abstractness
    calculate_abstractness(nodes, edges)
    # Inestabilidad
    calculate_instability(edges, nodes)
    # DMS
    calculate_dms(edges)
    # Package Mapping
    calculate_package_mapping(nodes, edges)
    # name resemblance
    claculate_nameResemblance(edges, name_ressemblance_umbral)

    return edges


def add_metric_json(edges):
    for edge in edges:
        test = {"metrics": {}}
        edge.update(test)


def inComplete_nodes_properties(nodes):
    """Marca cada nodo como imcompleto si no tiene los recursos necesarios para calcular las métricas

    Parameters
    ----------
    nodes: list
        lista con todos los nodos de la arquitectura
    """
    flag = False
    for node in nodes:
        if (
            "module" not in node["data"]
            or "isAbstract" not in node["data"]
            or "isInterface" not in node["data"]
        ):
            flag = True
        else:
            flag = False
        incomompleteProperties = {"incomompleteProperties": flag}
        node["data"].update(incomompleteProperties)
