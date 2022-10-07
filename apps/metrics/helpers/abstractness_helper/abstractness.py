
def calculate_abstractness(nodes, edges):
    """ Calcula de la métrica Abstracción y llama a los métodos de sus variables

    Parameters
    ----------
    nodes: list
        lista con todos los nodos de la arquitectura
    edges: list
        lista con todas las aristas de la arquitectura
    """
    for edge in edges:
        na = calculate_variable_na(nodes, edge)
        nc = 2

        value = calculate_abstractness_value(na, nc)
        
        abstractness = abstractness_serializer(na, nc, value)

        edge['metrics'].update(abstractness)



def calculate_variable_na(nodes, edge):
    """ Calcula la variable Na de la métrica Abstracción

    Parameters
    ----------
    nodes: list
        lista con todos los nodos de la arquitectura
    edge: 
        relacion a la cual se le va a calcular la variable Na
    """
    na = 0
    for node in nodes:

        if node['data']['id'] == edge['data']['source']:
            if ('isInterface' in node['data'] and node['data']['isInterface'] == True) or ('isAbstract' in node['data'] and node['data']['isAbstract'] == True):

                na = na + 1

        if node['data']['id'] == edge['data']['target']:
            if ('isInterface' in node['data'] and node['data']['isInterface'] == True) or ('isAbstract' in node['data'] and node['data']['isAbstract'] == True):
                na = na + 1

    return na


def calculate_abstractness_value(na, nc):
    if nc == 0:
        return  0
    else:
        return  na / nc



def abstractness_serializer(na, nc, value):
     return {
            'abstractness': {
                'variables': {
                    'na': na,
                    'nc': nc
                },
                'value': value
            }
        }