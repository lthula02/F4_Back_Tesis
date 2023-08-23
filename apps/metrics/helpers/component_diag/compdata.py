from firebase_admin import db

"""
Compdata debería tener una estructura como la siguiente

compdata = [
{
    'name': 'Transmisión',
    'requires': ['Entretenimiento', 'Confort']
},
{
    'name': 'Entretenimiento',
    'requires': ['Confort']
},
{
    'name': 'Confort',
    'requires': []
}

]
"""


def handleComponentData(data):
    print("Llegue a compdata")
    print(data)
    uid = data["user_id"]
    project_index = data["project_index"]
    arch_index = int(data["arch_index"])
    version_index = data["ver_index"]
    url = "/users/" + uid + "/projects/" + str(project_index)

    arch_ref = db.reference(url + "/architectures")
    arch_arr = arch_ref.get()

    edges = arch_arr[int(arch_index)]["versions"][int(version_index)]["elements"][
        "edges"
    ]

    compdata_dict = {}  # Diccionario para almacenar la información temporalmente

    for edge in edges:
        source_component = edge["data"]["source_component"]
        target_component = edge["data"]["target_component"]

        if source_component not in compdata_dict:
            compdata_dict[source_component] = set()

        compdata_dict[source_component].add(target_component)

    compdata = []

    for source, targets in compdata_dict.items():
        compdata.append({"name": source, "requires": list(targets)})

    return compdata
