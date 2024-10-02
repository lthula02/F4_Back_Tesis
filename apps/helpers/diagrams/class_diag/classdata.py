from firebase_admin import db


def handleClassData(data):
    uid = data["user_id"]
    project_index = data["project_index"]
    arch_index = int(data["arch_index"])
    version_index = data["ver_index"]
    url = "/users/" + uid + "/projects/" + str(project_index)

    arch_ref = db.reference(url + "/architectures")
    arch_data = arch_ref.get()

    arch_name = arch_data[int(arch_index)]["versions"][int(version_index)]["name"]

    edges = arch_data[int(arch_index)]["versions"][int(version_index)]["elements"][
        "edges"
    ]

    compdata_dict = {}  # Diccionario para almacenar la información temporalmente
    for edge in edges:
        source_component = edge["data"]["source_component"]
        target_component = edge["data"]["target_component"]
        if source_component != "n/a" and target_component != "n/a":
            if source_component not in compdata_dict:
                compdata_dict[source_component] = set()
            if target_component != source_component:
                compdata_dict[source_component].add(target_component)

    list_t = arch_data[int(arch_index)]["versions"][int(version_index)]["elements"][
        "list_t"
    ]

    class_data = []  # Lista de diccionarios con los datos

    for cc in list_t:
        # Determine the 'head' based on 'name' or 'description'
        if cc["name"] in compdata_dict:
            head = cc["name"]
        elif cc["description"] in compdata_dict:
            head = cc["description"]
        
        # Check if 'head' already exists in class_data
        existing_component = next((item for item in class_data if item["head"] == head), None)
        
        if existing_component:
            # If it exists, extend the 'body' and 'requires' of the existing component
            existing_component["body"].extend(list(cc["composite_component"]))
            existing_component["requires"].extend(list(compdata_dict[head]))
        else:
            # Otherwise, create a new component
            class_data.append(
                {
                    "head": head,
                    "body": list(cc["composite_component"]),
                    "requires": list(compdata_dict[head]),
                }
            )

    return arch_name, class_data


"""
De esta forma se debería ver class_data:

class_data = [
{
    'head': 'C0',
    'body': ['EvtTranslator', 'I18NTranslator'],
    'requires': ['C1']
},
{
    'head': 'C1',
    'body': ['PruebaTranslator', 'Prueba2Translator'],
    'requires': []
}
]
"""
