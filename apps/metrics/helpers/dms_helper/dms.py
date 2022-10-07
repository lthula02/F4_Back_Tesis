


def calculate_dms(edges):
    """ Calcula la métrica Distancia de la secuencia principal que es dependiente de las métricas Abstracción e Inestabilidad

    Parameters
    ----------
    edges: list
        lista con todas las aristas de la arquitectura
    """
    for edge in edges:
        value = calculate_dms_value(edge)

        DMS = dms_serializer(value)

        edge['metrics'].update(DMS)
        

def calculate_dms_value(edge):
    value = abs(edge['metrics']['abstractness']['value'] + edge['metrics']['instability']['value'] - 1)

    return value


def dms_serializer(value):
    return  {
            'DMS': {
                'value': value
            }
        }