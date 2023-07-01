from firebase_admin import db


def handleVariabilityDiagram(data):
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

        for component_data in composite_components:
            component_name = component_data["name"]
            composite_components_data[component_name] = {
                "name": component_name,
                "description": "",  # Se asignará más adelante
                "composite_component": [],  # Se asignará más adelante
            }

        for node_key, node_data in enumerate(nodes):
            node_description = node_data["data"]["description"]
            composite_name = node_data["data"].get("composite")
            composite_components_description[node_key] = node_description

            if composite_name in composite_components_data:
                composite_components_data[composite_name]["composite_component"].append(
                    {"name": node_key, "description": node_description}
                )

        archs.append(list(composite_components_data.values()))

    # Retornar la lista de arquitecturas
    print(archs)
    return archs


# Imprimir el resultado para verificar
def checkVariabilityDiagram(archs):
    for arch_index, components in enumerate(archs):
        print(f"Arquitectura {arch_index}:")
        for component in components:
            print(f"Componente: {component['name']}")
            print(f"Descripción: {component['description']}")
            print(f"Nodos: {component['composite_component']}")
            print("--------------------")
