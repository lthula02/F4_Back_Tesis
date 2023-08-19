from firebase_admin import db
from rest_framework.response import Response
from apps.metrics.helpers.combine_metrics_helper.combine_metrics import SearchNode


# Esta función extrae la información de la base de datos para poder ser utilizada por las funciones
def extractData(data, l, n, e, update):
    # l es list_t, n es nodes, y e es edges, cada uno es un booleano que especifica si son requeridos o no
    # update es un booleano para mandar las variables necesarias para actualizar la bd
    uid = data["user_id"]
    project_index = data["project_index"]
    arch_index = int(data["arch_index"])
    version_index = data["ver_index"]
    url = "/users/" + uid + "/projects/" + str(project_index)

    arch_ref = db.reference(url + "/architectures")
    arch_arr = arch_ref.get()

    result = {"list_t": None, "nodes": None, "edges": None}

    if l:
        result["list_t"] = arch_arr[int(arch_index)]["versions"][int(version_index)][
            "elements"
        ]["list_t"]
    if n:
        result["nodes"] = arch_arr[int(arch_index)]["versions"][int(version_index)][
            "elements"
        ]["nodes"]
    if e:
        result["edges"] = arch_arr[int(arch_index)]["versions"][int(version_index)][
            "elements"
        ]["edges"]
    if update:
        update_data = {
            "arch_arr": arch_arr,
            "arch_index": arch_index,
            "version_index": version_index,
            "url": url,
        }
        return update_data

    return result


# Esta función actualiza los datos en la base de datos
def updateData(data, list_t, nodes, edges):
    d = extractData(data, False, False, False, True)
    try:
        if list_t != None:
            # Actualizar la lista t en la estructura de datos
            d["arch_arr"][int(d["arch_index"])]["versions"][int(d["version_index"])][
                "elements"
            ]["list_t"] = list_t
        if nodes != None:
            # Actualizar la lista nodes con los valores actualizados del diccionario
            d["arch_arr"][int(d["arch_index"])]["versions"][int(d["version_index"])][
                "elements"
            ]["nodes"] = nodes
        if edges != None:
            # Actualizar la lista edges en la estructura de datos
            d["arch_arr"][int(d["arch_index"])]["versions"][int(d["version_index"])][
                "elements"
            ]["edges"] = edges

        # Actualizar la base de datos
        project_ref = db.reference(d["url"])
        project_ref.update({"architectures": d["arch_arr"]})

        return Response(data={"ok": True})
    except Exception as e:
        print("Error:", e)
    return Response({"ok": False})


def handleEditName(data):
    dataNeeded = extractData(data, True, True, True, False)
    list_t = dataNeeded["list_t"]
    nodes = dataNeeded["nodes"]

    old_name = data["old_name"]
    new_name = data["new_name"]

    # Crear un diccionario para búsqueda eficiente de nodos
    node_dict = {node["data"]["id"]: node for node in nodes}

    try:
        for t in list_t:
            if t["name"] == old_name:
                t["name"] = str(new_name).upper()
                for node_id in t["composite_component"]:
                    if node_id in node_dict:
                        node = node_dict[node_id]
                        node["data"]["composite"] = str(new_name).upper()
                break

        edges = updateEdgesNodesCompositeComponent(dataNeeded["edges"], node_dict)
        updateData(data, list_t, list(node_dict.values()), edges)

        return Response(data={"ok": True})
    except Exception as e:
        print("Error:", e)
    return Response({"ok": False})


# Permite editar el componente compuesto al que pertenece un nodo
def handleEditNodeCompositeComponent(data):
    dataNeeded = extractData(data, True, True, False, False)
    list_t = dataNeeded["list_t"]
    nodes = dataNeeded["nodes"]

    nodeData = data["node"]
    composite_component = data["new_name"]

    # Crear un diccionario para búsqueda eficiente de nodos
    node_dict = {node["data"]["id"]: node for node in nodes}

    try:
        fullNode = SearchNode(nodeData, nodes)  # me quede sin nombres jeje

        # Si el nodo pertenece con anterioridad a otro componente compuesto, actualizar lista_t
        if "composite" in fullNode["data"]:
            old_composite = fullNode["data"]["composite"]
            for lt in list_t:
                if old_composite in lt["composite_component"]:
                    lt["composite_component"].remove(old_composite)
                    break

        # Agregar el nodo al nuevo componente compuesto
        if composite_component in node_dict:
            t = node_dict[composite_component]
            t["composite_component"].append(nodeData)
            node_dict[nodeData]["data"].update({"composite": t["name"], "bg": t["bg"]})

        edges = updateEdgesNodesCompositeComponent(dataNeeded["edges"], node_dict)
        updateData(data, list_t, nodes, edges)

        return Response(data={"ok": True})
    except Exception as e:
        print(e)
        return Response(data={"ok": False})


""" 
 Actualiza en edges (las relaciones) los componentes compuestos de cada nodo
 Especifica de que cc viene el nodo origen y el nodo destino 
 - edges: lista de aristas en la base de datos
 - nodes: diccionario de nodos en la base de datos
"""


def updateEdgesNodesCompositeComponent(edges, nodes):
    # Actualizar source_component y target_component en edges
    for edge in edges:
        source_node_id = edge["data"]["source"]
        target_node_id = edge["data"]["target"]
        if source_node_id in nodes and "composite" in nodes[source_node_id]["data"]:
            edge["data"]["source_component"] = nodes[source_node_id]["data"][
                "composite"
            ]
        if target_node_id in nodes and "composite" in nodes[target_node_id]["data"]:
            edge["data"]["target_component"] = nodes[target_node_id]["data"][
                "composite"
            ]

    return edges


# Genera la tabla de los componentes compuestos
def handleCompositeComponentBoard(data):
    dataNeeded = extractData(data, True, True, True, False)
    list_t = dataNeeded["list_t"]
    nodes = dataNeeded["nodes"]
    edges = dataNeeded["edges"]

    try:
        node_dict = {node["data"]["id"]: node for node in nodes}

        for item in list_t:
            ca = []  # Required interfaces
            ce = []  # Provided interfaces

            for component in item["composite_component"]:
                for edge in edges:
                    source_node = node_dict[edge["data"]["source"]]
                    target_node = node_dict[edge["data"]["target"]]

                    if component == source_node["data"]["id"]:
                        composite_source = source_node["data"].get("composite", "")
                        if source_node["data"]["composite"] != composite_source:
                            if (
                                edge["scratch"]["index"] not in ce
                                and edge["scratch"]["index"] not in ca
                            ):
                                ce.append(edge["scratch"]["index"])

                    if component == target_node["data"]["id"]:
                        composite_target = target_node["data"].get("composite", "")
                        if target_node["data"]["composite"] != composite_target:
                            if (
                                edge["scratch"]["index"] not in ca
                                and edge["scratch"]["index"] not in ce
                            ):
                                ca.append(edge["scratch"]["index"])

            item.update(
                {
                    "required_interfaces": ca,
                    "provided_interfaces": ce,
                    "description": "",
                }
            )

        updateData(data, list_t, None, None)

        return Response(data={"ok": True})
    except Exception as e:
        print(e)
        return Response(data={"ok": False})


# TODO
# ? Hace falta limpiar las tablas
# Edita la descripción de los componentes compuestos
def handleEditCompositeComponentDescription(data):
    dataNeeded = extractData(data, True, False, False, False)
    list_t = dataNeeded["list_t"]

    cc_name = data["name"]
    description = data["description"]

    try:
        for item in list_t:
            if item["name"] == cc_name:
                item.update({"description": description})

        updateData(data, list_t, None, None)

        return Response(data={"ok": True})
    except Exception as e:
        print(e)
        return Response(data={"ok": False})
