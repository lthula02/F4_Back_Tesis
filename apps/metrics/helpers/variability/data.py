from firebase_admin import db


def handleVariabilityData(data):
    uid = data["user_id"]
    project_index = data["project_index"]
    url = "/users/" + uid + "/projects/" + str(project_index)

    architectures_ref = db.reference(url + "/architectures")
    architectures_data = architectures_ref.get()
    num_architectures = len(architectures_data)

    archs = []

    composite_components_data = {}
    composite_components_description = {}

    for arch_index in range(num_architectures):
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
        n = 0
        for component_data in composite_components:
            component_name = component_data["name"]
            component_desc = component_data["description"]

            key = component_name
            if component_desc != "-":
                key = component_desc  # si el nombre de aspecto del cc existe, se usará ese valor

            composite_components_data[key] = {
                "name": component_name,
                "description": component_desc,
                "composite_component": [],  # Se asignará más adelante
            }

        for node_key, node_data in enumerate(nodes):
            node_name = node_data["data"]["id"]
            node_description = node_data["data"]["description"]
            composite_name = node_data["data"].get("composite")
            composite_components_description[node_key] = node_description

            if composite_name in composite_components_data:
                composite_components_data[composite_name]["composite_component"].append(
                    {"name": node_name, "description": node_description}
                )

        archs.append(list(composite_components_data.values()))

    checkVariabilityDiagram(archs)
    # Retornar la lista de arquitecturas
    return archs


# Imprimir el resultado para verificar
def checkVariabilityDiagram(archs):
    for arch_index, components in enumerate(archs):
        print(f"Arquitectura {arch_index}:")
        for component in components:
            print(f"ID del Componente: {component['name']}")
            print(f"Nombre de Aspecto: {component['description']}")
            print(f"Nodos: {component['composite_component']}")
            print("--------------------")
