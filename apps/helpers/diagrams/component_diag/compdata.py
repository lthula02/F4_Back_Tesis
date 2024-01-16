from firebase_admin import db


def handleComponentData(data):
    uid = data["user_id"]
    project_index = data["project_index"]
    url = "/users/" + uid + "/projects/" + str(project_index)

    architectures_ref = db.reference(url + "/architectures")
    architectures_data = architectures_ref.get()
    num_architectures = len(architectures_data)

    archs_compdata = {}

    for arch_index in range(num_architectures):
        name_ref = architectures_ref.child(str(arch_index)).child("name")
        architecture_name = name_ref.get()
        versions_ref = architectures_ref.child(str(arch_index)).child("versions")
        versions_data = versions_ref.get()
        latest_version_index = len(versions_data) - 1

        edges_ref = versions_ref.child(str(latest_version_index)).child(
            "elements/edges"
        )
        edges = edges_ref.get()

        compdata_dict = {}  # Diccionario para almacenar la información temporalmente
        for edge in edges:
            #print('--------------------------------------')
            #print(f'{edge["data"]["source_component"]} to {edge["data"]["target_component"]}')
            #print('--------------------------------------')
            source_component = edge["data"]["source_component"]
            target_component = edge["data"]["target_component"]
            if source_component != "n/a" and target_component != "n/a":
                if source_component not in compdata_dict:
                    compdata_dict[source_component] = set()

                if target_component != source_component:
                    compdata_dict[source_component].add(target_component)

        arch_comp = []
        for source, targets in compdata_dict.items():
            arch_comp.append({"name": source, "requires": list(targets)})
        archs_compdata[architecture_name] = arch_comp

    return archs_compdata


"""
De esta forma se debería ver archs_compdata:

archs_compdata = {
    "Architecture_1": [
        {"name": "Component_A", "requires": ["Component_B", "Component_C"]},
        {"name": "Component_B", "requires": ["Component_C"]},
        {"name": "Component_C", "requires": []}
    ],
    "Architecture_2": [
        {"name": "Component_X", "requires": ["Component_Y"]},
        {"name": "Component_Y", "requires": []}
    ],
    # ... más arquitecturas ...
}
"""
