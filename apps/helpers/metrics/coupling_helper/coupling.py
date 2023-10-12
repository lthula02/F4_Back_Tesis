

def calculate_coupling(nodes, edges):

    for node in nodes:
        # Todas las relaciones en las cuales este nodo es partida
        edgesAux = get_all_edges_of_source_node(node, edges)

        # se calcula la variable ni, comun para todas estas relaciones
        ni = calculate_ni(edgesAux, nodes)

        for edge in edgesAux:
            nij = calculate_nij(nodes, edge)

            value = calculate_copupling_value(ni, nij)

            coupling = coupling_serializer(ni, nij, value)
            edge['metrics'].update(coupling)

def get_all_edges_of_source_node(node, edges):
    """ Guarda todas las relaciones en las cuales el nodo donde estamos parados es el mismo nodo de partida de la relación

    Parameters
    ----------
    node: 
        nodo donde estamos parados para comprobar que se trata del nodo de partida de la relación
    edges: list
        lista con todas las aristas de la arquitectura
    """
    edgesAux = []
    
    # Guardar todas las relaciones en las cuales el nodo donde estamos parados es el mismo nodo de partida de la relacion
    for edge in edges:
        if edge['data']['source'] == node['data']['id']:
            edgesAux.append(edge)
    return edgesAux


def calculate_ni(edgesAux, nodes):
    """ Cuenta el numero de nodos de llegada de tipo interfaz en cada relación
    Parameters
    ----------
    nodes: list
        lista con todos los nodos de la arquitectura
    edgesAux: list
        lista auxiliar con todas las aristas de la arquitectura
    """
    count = 0
    for edge in edgesAux:
        for node in nodes:
            if node['data']['id'] == edge['data']['target']:
                if 'isInterface' in node['data'] and node['data']['isInterface'] == True:
                    count += 1
    return count


def calculate_nij(nodes, edge):
    nij = 0
    for node in nodes:
        if node['data']['id'] == edge['data']['target']:
            if 'isInterface' in node['data'] and node['data']['isInterface'] == True:
                nij = 1
            break
    return nij


def calculate_copupling_value(ni, nij):
    if ni == 0:
        return 0
    else:
        return nij / ni


def coupling_serializer(ni, nij, value):
    
    return {
        'coupling': {
            'variables': {
                'nij': nij,
                'ni': ni
            },
            'value': value
        }

    }

    
