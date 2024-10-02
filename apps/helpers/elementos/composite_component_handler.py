from firebase_admin import db
from rest_framework.response import Response
from apps.helpers.metrics.combine_metrics import SearchNode


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
    dataNeeded = extractData(data, True, True, True, False)

    list_t = dataNeeded["list_t"]
    nodes = dataNeeded["nodes"]

    nodeName = data["node"]
    new_component = data["new_name"]

    try:
        fullNode = SearchNode(nodeName, nodes)  # me quede sin nombres jeje
        nodeName = fullNode["data"]["id"]

        # Si el nodo pertenece con anterioridad a otro componente compuesto, actualizar lista_t
        if "composite" in fullNode["data"]:
            if fullNode["data"]["composite"] != "-":
                old_component = fullNode["data"]["composite"]
                i = 0
                for lt in list_t:
                    if (
                        old_component in lt["description"]
                        or old_component in lt["name"]
                    ):
                        if nodeName in lt["composite_component"]:
                            lt["composite_component"].remove(nodeName)
                            i += 1
                    if (
                        new_component in lt["description"]
                        or new_component in lt["name"]
                    ):
                        lt["composite_component"].append(nodeName)
                        i += 1
                    if i == 2:
                        break

        # Agregar el nodo al nuevo componente compuesto
        fullNode["data"]["composite"] = new_component
        node_dict = {}
        for node in nodes:
            if node["data"]["id"] == nodeName:
                node_dict[nodeName] = fullNode
            else:
                node_dict[node["data"]["id"]] = node

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

 Fijese que se actualiza source y target con el valor de "composite" del nodo,
 es por esto que en la función handleEditCompositeComponentDescription se inserta
 la nueva descripción en esta clave del nodo, intercambiando el nombre, para poder
 generar el diagrama de componentes con los nombres de aspecto
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

            print(f"\nProcessing composite component: {item['name']}")  # Name of the composite component

            for component in item["composite_component"]:
                print(f"Looking for component: {component}")
                for edge in edges:
                    source_node = node_dict[edge["data"]["source"]]
                    target_node = node_dict[edge["data"]["target"]]

                    # Check if current component is the source of this edge
                    if component == source_node["data"]["id"]:
                        print(f"Component matched with source node: {source_node['data']['id']}")
                        if edge["scratch"]["index"] not in ce and edge["scratch"]["index"] not in ca:
                            print(f"Adding to provided interfaces (ce): {edge['scratch']['index']}")
                            ce.append(edge["scratch"]["index"])

                    # Check if current component is the target of this edge
                    if component == target_node["data"]["id"]:
                        print(f"Component matched with target node: {target_node['data']['id']}")
                        if edge["scratch"]["index"] not in ca and edge["scratch"]["index"] not in ce:
                            print(f"Adding to required interfaces (ca): {edge['scratch']['index']}")
                            ca.append(edge["scratch"]["index"])

            print("Required interfaces (ca):", ca)
            print("Provided interfaces (ce):", ce)

            # Update the item with the interfaces
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
# Edita la descripción (aspectos) de los componentes compuestos
def handleEditCompositeComponentDescription(data):
    dataNeeded = extractData(data, True, True, True, False)
    list_t = dataNeeded["list_t"]
    nodes_list = dataNeeded["nodes"]

    # Convertir la lista de nodos a un diccionario para búsqueda eficiente
    node_dict = {node["data"]["id"]: node for node in nodes_list}

    cc_name = data["name"]
    new_description = data["description"]

    try:
        for item in list_t:
            if item["name"] == cc_name:
                old_description = item.get("description", "")
                item.update({"description": new_description})

                # Actualizar la clave "composite" en el diccionario de nodos
                # Esto se añade para que el nombre de aspecto (descripción) esté en composite en vez del nombre id (C0, por ejemplo)
                for node_id, node in node_dict.items():
                    if "composite" in node["data"]:
                        if node["data"]["composite"] == old_description:
                            node["data"]["composite"] = new_description
                        elif node["data"]["composite"] == cc_name:
                            node["data"]["composite"] = new_description

        edges = updateEdgesNodesCompositeComponent(dataNeeded["edges"], node_dict)
        updateData(data, list_t, nodes_list, edges)  # Actualizar también los nodos

        return Response(data={"ok": True})
    except Exception as e:
        print(e)
        return Response(data={"ok": False})
