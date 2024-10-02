from firebase_admin import db


def handleVariabilityData(data):
    '''
    Crea la estructura de datos necesaria a partir de los datos del firebase

    '''
    uid = data["user_id"]
    project_index = data["project_index"]
    url = "/users/" + uid + "/projects/" + str(project_index)

    architectures_ref = db.reference(url + "/architectures")
    architectures_data = architectures_ref.get()
    num_architectures = len(architectures_data)

    archs = []

    for arch_index in range(num_architectures):
        composite_components_data = {}

        versions_ref = architectures_ref.child(str(arch_index)).child("versions")
        versions_data = versions_ref.get()
        latest_version_index = len(versions_data) - 1

        list_t_ref = versions_ref.child(str(latest_version_index)).child(
            "elements/list_t"
        )

        composite_components = list_t_ref.get()

        nodes_ref = versions_ref.child(str(latest_version_index)).child(
            "elements/nodes"
        )
        nodes = nodes_ref.get()
        for component_data in composite_components:
            component_name = component_data["name"]
            component_desc = component_data["description"]

            key = component_name
            if component_desc != "-":
                key = component_desc  # si el nombre de aspecto del cc existe, se usará ese valor

            composite_components_data[key] = {
                "name": component_name,
                "arq_name": architectures_data[arch_index]['name'],
                "description": component_desc,
                "composite_component": [],  # Se asignará más adelante
            }

        for node_key, node_data in enumerate(nodes):
            node_name = node_data["data"]["id"]
            node_description = str(node_data["data"]["description"])
            composite_name = str(node_data["data"].get("composite"))

            if composite_name in composite_components_data:
                composite_components_data[composite_name]["composite_component"].append(
                    {"name": node_name, "description": node_description}
                )

        archs.append(list(composite_components_data.values()))

    # checkVariabilityDiagram(archs)
    # Retornar la lista de arquitecturas
    return archs


def checkVariabilityDiagram(archs):
    '''Imprime el resultado para verificar'''
    for arch_index, components in enumerate(archs):
        print(f"ARQUITECTURA {arch_index}:")
        for component in components:
            print(f"ID del Componente: {component['name']}")
            print(f"Nombre de Aspecto: {component['description']}")
            print(f"Nodos: {component['composite_component']}")
            print(f"Nombre Arquitectura: {component['arq_name']}")
            print("--------------------")
