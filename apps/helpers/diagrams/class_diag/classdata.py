from firebase_admin import db


def handleClassData(data):
    uid = data["user_id"]
    project_index = data["project_index"]
    arch_index = int(data["arch_index"])
    version_index = data["ver_index"]
    url = "/users/" + uid + "/projects/" + str(project_index)

    arch_ref = db.reference(url + "/architectures")
    arch_data = arch_ref.get()

    arch_name_ref = arch_data[int(arch_index)]["versions"][int(version_index)]["name"]
    arch_name = arch_name_ref.get()

    edges_ref = arch_data[int(arch_index)]["versions"][int(version_index)]["elements"][
        "edges"
    ]
    edges = edges_ref.get()

    compdata_dict = {}  # Diccionario para almacenar la información temporalmente
    for edge in edges:
        source_component = edge["data"]["source_component"]
        target_component = edge["data"]["target_component"]
        if source_component != "n/a" and target_component != "n/a":
            if source_component not in compdata_dict:
                compdata_dict[source_component] = set()
            if target_component != source_component:
                compdata_dict[source_component].add(target_component)

    list_t_ref = arch_data[int(arch_index)]["versions"][int(version_index)]["elements"][
        "list_t"
    ]
    list_t = list_t_ref.get()

    class_data = []  # Lista de diccionarios con los datos

    for cc in list_t:
        if cc["name"] in compdata_dict:
            head = cc["name"]
        elif cc["description"] in compdata_dict:
            head = cc["description"]

        class_data.append(
            {
                "head": head,
                "body": list(cc["composite_component"].values()),
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
