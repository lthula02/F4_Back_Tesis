def count_aspects(archs_compdata):
    '''
    Agrega a la estructura de datos, una cuenta de en cuántas arquitecturas está presente cada aspecto
    '''
    component_dict = {}

    for arch_data in archs_compdata.values():
        for component in arch_data:
            component_name = component["name"]
            component_requires = component["requires"]
            if component_name not in component_dict:
                component_dict[component_name] = {
                    "name": component_name,
                    "requires": component_requires,
                    "count": 1,
                }
            else:
                component_dict[component_name]["count"] += 1

    compdata = list(component_dict.values())

    return compdata


"""
Estructura que debe tener compdata al finalizar corrida (datos de ejemplo):

compdata = [
{
    'name': 'Transmisión',
    'requires': ['Entretenimiento', 'Confort'],
    'count': 2
},
{
    'name': 'Entretenimiento',
    'requires': ['Confort'],
    'count': 2
},
{
    'name': 'Confort',
    'requires': [],
    'count': 1
}
]

"""
