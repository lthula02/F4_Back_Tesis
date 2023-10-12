

def calculate_package_mapping(nodes, edges):
    """ Calcula la métrica Mapeo de Paquetes

    Parameters
    ----------
    nodes: list
        lista con todos los nodos de la arquitectura
    edges: list
        lista con todas las aristas de la arquitectura
    """
    for edge in edges:
        nameSource = edge['data']['source']
        nameTarget = edge['data']['target']
        moduleSource = None
        moduleTarget = None
        for node in nodes:
            if moduleSource is None and node['data']['id'] == nameSource and 'module' in node['data']:
                moduleSource = node['data']['module']
            if moduleTarget is None and node['data']['id'] == nameTarget and 'module' in node['data']:
                moduleTarget = node['data']['module']
            if moduleSource is not None and moduleTarget is not None:
                break
        if moduleSource == moduleTarget:
            value = 1
        else:
            value = 0

        packageMapping = package_mapping_serializer(value) 

        edge['metrics'].update(packageMapping)


def package_mapping_serializer(value):
    return {
            'packageMapping': {
                'value': value
            }
        }