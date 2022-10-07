

def calculate_instability(edges, nodes):
    """ Calcula de la métrica Inestabilidad y llama a los métodos de sus variables

    Parameters
    ----------
    edges: list
        lista con todas las aristas de la arquitectura
    """
    for edge in edges:
        ce = calculate_variableCe(edge, edges, nodes)
        ca = calculate_variableCa(edge, edges, nodes)

        value = calculate_instability_value(ca, ce)
      

        instabilityVariables = instability_serializer(ca, ce, value)
        
        
        
        edge['metrics'].update(instabilityVariables)


def calculate_variableCe(edge, edges, nodes):
    """ Calcula la variable Ce de la métrica Inestabilidad

    Parameters
    ----------
    edges: list
        lista con todas las aristas de la arquitectura
    edge: 
        relacion a la cual se le va a calcular la variable Ce
    """
    ce = 0
    nodeSource = edge['data']['source']
    nodeTarget = edge['data']['target']

    nodeName = None

    for edgeAux in edges:
        if edgeAux['data']['source'] == nodeSource and edgeAux['data']['target'] != nodeTarget:
            for node in nodes:
                if node['data']['id'] == edgeAux['data']['target'] and 'isInterface' in node['data'] and node['data']['isInterface'] == True:
                    ce = ce + 1
                    nodeSource = "finished"
                    break
        if edgeAux['data']['source'] == nodeTarget:
            for node in nodes:
                if node['data']['id'] == edgeAux['data']['target'] and 'isInterface' in node['data'] and node['data']['isInterface']:
                    ce = ce + 1
                    nodeTarget = "finished"
                    break
        if nodeSource == "finished" and nodeTarget == "finished":
            break
    return ce


def calculate_variableCa(edge, edges, nodes):
    """ Calcula la variable Ca de la métrica Inestabilidad

    Parameters
    ----------
    edges: list
        lista con todas las aristas de la arquitectura
    edge: 
        relacion a la cual se le va a calcular la variable Ca
    """
    ca = 0
    nodeSource = edge['data']['source']
    nodeTarget = edge['data']['target']

    sourceInterface = False
    targetInterface = False

    for node in nodes:
        if node['data']['id'] == nodeSource and 'isInterface' in node['data'] and node['data']['isInterface']:
            sourceInterface = True
        if node['data']['id'] == nodeTarget and 'isInterface' in node['data'] and node['data']['isInterface']:
            targetInterface = True
        if sourceInterface and targetInterface:
            break

    for edgeAux in edges:
        if edgeAux['data']['source'] == nodeSource and edgeAux['data']['target'] == nodeTarget:
            continue
        else:
            if edgeAux['data']['target'] == nodeSource and sourceInterface:
                ca = ca + 1
            elif edgeAux['data']['target'] == nodeTarget and targetInterface:
                ca = ca + 1
    return ca



def calculate_instability_value(ca, ce):
    if (ca + ce) == 0:
        return  0
    else:
        return  ce / (ca + ce)



def instability_serializer(ca, ce, value):
    return {
            'instability': {
                'variables': {
                    'ce': ce,
                    'ca': ca
                },
                'value': value
            }
        }