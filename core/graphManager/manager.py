from core.parser.parser import xmlToJson
from fuzzywuzzy import fuzz
# from fuzzywuzzy import process


def manageFiles(files, nodes, edges, node_set, edge_set):
    """ Leer todos los archivos y manejar la creación de
    sus nodos y relaciones.

    Parameters
    ----------
    files: list
        lista con todos los archivos XML
    nodes: list
        lista con todos los nodos de la arquitectura
    edges: list
        lista con todas las aristas de la arquitectura
    node_set: set
        set para mantener constancia de los nodos ya creados
    edge_set
        set pata mantener constancia de las aristas ya creadas
    """


    for file in files:
        file_json = xmlToJson(file)
        handleGraphBuild(file_json, nodes, edges, node_set, edge_set)
    #calculateMetricsVariables(nodes, edges)


def calculateMetricsVariables(nodes, edges):
    """ Se llaman todos los métodos correspondientes al cálculo de métricas

    Parameters
    ----------
    nodes: list
        lista con todos los nodos de la arquitectura
    edges: list
        lista con todas las aristas de la arquitectura
    """
    # incompleteResources
    inCompleteResources(nodes)
    # Coupling
    for node in nodes:
        calculateCouplingVariables(getAllEdgesOfSourceNode(node, edges), nodes)
    # Abstractness
    calculateAbstractness(nodes, edges)
    # Inestabilidad
    calculateInstability(edges, nodes)
    # DMS
    calculateDMS(edges)
    # Package Mapping
    calculatePackageMapping(nodes, edges)
    # name resemblance
    claculateNameResemblance(edges)


def claculateNameResemblance(edges):
    for edge in edges:
        word1 = edge['data']['source']
        word2 = edge['data']['target']
        ratio = fuzz.ratio(word1, word2)
        value = 0

        if word1 in word2 or word2 in word1:
            value = 1
        elif ratio > 45:
            value = 1
        ratio = str(ratio) + "%"
        nameResemblance = {
            'nameResemblance': {
                'value': value,
                'ratio': ratio
            }
        }

        edge['metrics'].update(nameResemblance)


def inCompleteResources(nodes):
    """ Marca cada nodo como imcompleto si no tiene los recursos necesarios para calcular las métricas

    Parameters
    ----------
    nodes: list
        lista con todos los nodos de la arquitectura
    """
    flag = False
    for node in nodes:
        # aqui no entra
        if 'module' not in node['data'] or 'isAbstract' not in node['data'] or 'isInterface' not in node['data']:
            flag = True
        else:
            flag = False
        incompleteResources = {
            'incompleteResources': flag
        }
        node['data'].update(incompleteResources)


def calculateDMS(edges):
    """ Calcula la métrica Distancia de la secuencia principal que es dependiente de las métricas Abstracción e Inestabilidad

    Parameters
    ----------
    edges: list
        lista con todas las aristas de la arquitectura
    """
    for edge in edges:
        value = edge['metrics']['abstractness']['value'] + \
            edge['metrics']['instability']['value'] - 1

        if value < 0:
            value = value * -1

        DMS = {
            'DMS': {
                'value': value
            }
        }

        edge['metrics'].update(DMS)


def calculateAbstractness(nodes, edges):
    """ Calcula de la métrica Abstracción y llama a los métodos de sus variables

    Parameters
    ----------
    nodes: list
        lista con todos los nodos de la arquitectura
    edges: list
        lista con todas las aristas de la arquitectura
    """
    for edge in edges:
        na = calculateVariableNa(nodes, edge)
        nc = 2

        value = 0
        if nc == 0:
            value = 0
        else:
            value = na / nc

        abstractnessVariables = {
            'abstractness': {
                'variables': {
                    'na': na,
                    'nc': nc
                },
                'value': value
            }
        }

        edge['metrics'].update(abstractnessVariables)


def calculateVariableNa(nodes, edge):
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


def calculateVariableNc(nodes, edge):
    """ Calcula la variable Nc de la métrica Abstracción

    Parameters
    ----------
    nodes: list
        lista con todos los nodos de la arquitectura
    edge:
        relacion a la cual se le va a calcular la variable Na
    """
    nc = 0
    flagSource = False
    flagTarget = False
    for node in nodes:
        if node['data']['id'] == edge['data']['source']:
            if 'isAbstract' in node['data'] and node['data']['isAbstract'] != True:
                nc = nc + 1
                flagSource = True

        if 'isAbstract' in node['data'] and node['data']['id'] == edge['data']['target']:
            if node['data']['isAbstract'] != True:
                nc = nc + 1
                flagTarget = True

        if flagSource and flagTarget:
            break

    return nc


def calculateInstability(edges, nodes):
    """ Calcula de la métrica Inestabilidad y llama a los métodos de sus variables

    Parameters
    ----------
    edges: list
        lista con todas las aristas de la arquitectura
    """
    for edge in edges:
        ce = calculateVariableCe(edge, edges, nodes)
        ca = calculateVariableCa(edge, edges, nodes)

        value = 0
        if (ca + ce) == 0:
            value = 0
        else:
            value = ce / (ca + ce)

        instabilityVariables = {
            'instability': {
                'variables': {
                    'ce': ce,
                    'ca': ca
                },
                'value': value
            }
        }
        edge['metrics'].update(instabilityVariables)


def calculateVariableCe(edge, edges, nodes):
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
                if node['data']['id'] == edgeAux['data']['target'] and 'isInterface' in node['data'] and node['data']['isInterface']:
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


def calculateVariableCa(edge, edges, nodes):
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


def calculatePackageMapping(nodes, edges):
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

        packageMapping = {
            'packageMapping': {
                'value': value
            }
        }

        edge['metrics'].update(packageMapping)


def getAllEdgesOfSourceNode(node, edges):
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


def calculateCouplingVariables(edgesAux, nodes):
    """ Calcula las variables Ni y Nij de la métrica Acoplamiento

    Parameters
    ----------
    nodes: list
        lista con todos los nodos de la arquitectura
    edgesAux: list
        lista auxiliar con todas las aristas de la arquitectura
    """
    ni = countNumberInterfaces(edgesAux, nodes)
    for edge in edgesAux:
        nij = 0

        for node in nodes:
            if node['data']['id'] == edge['data']['target']:
                if 'isInterface' in node['data'] and node['data']['isInterface'] == True:
                    nij = 1
                break
        value = 0
        if ni == 0:
            value = 0
        else:
            value = nij / ni

        couplingVariables = {
            'metrics': {
                'coupling': {
                    'variables': {
                        'nij': nij,
                        'ni': ni
                    },
                    'value': value
                }
            }
        }
        edge.update(couplingVariables)


def countNumberInterfaces(edgesAux, nodes):
    """ Cuenta el numero de interfaces presentes en cada relación
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


def handleGraphBuild(json, nodes, edges, node_set, edge_set):
    """ Inicialización de los nodos y aristas de un archivo

    Parameters
    ----------
    json: dict
        diccionario de archivo XML convertido a json
    nodes: list
        lista con todos los nodos de la arquitectura
    edges: list
        lista con todas las aristas de la arquitectura
    node_set: set
        set para mantener constancia de los nodos ya creados
    edge_set
        set pata mantener constancia de las aristas ya creadas
    """
    base = json['doxygen']['compounddef']
    if(base['compoundname'] == 'README.md'):
        return
    node = createNode(base, nodes, node_set)
    if node is not None:
        nodes.append(node)
        node_set.add(node['data']['id'])
    handleEdgeCreation(base, edges, nodes, node_set, edge_set)


def createNode(base, nodes, node_set):
    """ Creación del objeto nodo
    Parameters
    ----------
    base: dict
        diccionario con información del nodo
    node_set: set
        set para mantener constancia de los nodos ya creados

    Returns
    -------
    dict
        diccionario con el objeto nodo creado
    """
    class_id = getClassId(base)
    isAbstract = isAbstractClass(base['programlisting']['codeline'])
    isInterface = isInterfaceClass(base['programlisting']['codeline'])
    module = getModule(base)

    if class_id in node_set:
        for node in nodes:
            if node['data']['id'] == class_id:
                node['data']['module'] = module
                node['data']['isAbstract'] = isAbstract
                node['data']['isInterface'] = isInterface
                break
        return None
    node = {
        "data": {
            "id": class_id,
            "name": class_id,
            "module": module,
            "isAbstract": isAbstract,
            "isInterface": isInterface,
            "bg": '#18202C'
        }
    }
    return node


def getClassId(base):
    """ Obtener el ID de la clase del archivo

    que está siendo leído
    Parameters
    ----------
    base: dict
        diccionario con información del nodo

    Returns
    -------
    str
        id del nodo
    """
    class_name = base['compoundname']
    file_name = class_name.split('.')
    node_id = file_name[0]
    return node_id


def getModule(base):
    """ Obtener el modulo al que pertenece el archivo

    Parameters
    -------
    innerclass: dict
        Diccionario con la informacion del modulo al que pertenece el archivo

    Returns
    -------
    str
        Nombre del modulo
    """
    if 'innerclass' in base:
        route = base['innerclass']['#text'].split('::')
        return route[1]
    elif 'innernamespace' in base:
        innernamespace = base['innernamespace']
        if type(innernamespace) is list:
            route = innernamespace[0]['#text'].split('::')
            return route[len(route) - 1]
        else:
            route = innernamespace['#text'].split('::')
            return route[len(route) - 1]
    else:
        return None


def isInterfaceClass(codeLines):
    """ Determina si la clase recibida a través del xml es una interfaz o no
    Parameters
    ----------
    codeLines: list
        lista con todos los codeLines del xml donde se encuentra contenida la palabra interface
    """
    word = None
    flag = False
    for line in codeLines:
        highlight = line['highlight']
        if type(highlight) is list:
            for h in highlight:
                if '#text' in h:
                    word = h['#text']
                    if word is not None and word == 'interface':
                        flag = True
    return flag


def isAbstractClass(codeLines):
    """ Determina si la clase recibida a través del xml es abstracta o no
    Parameters
    ----------
    codeLines: list
        lista con todos los codeLines del xml donde se encuentra contenida la palabra abstract
    """
    word = None
    flag = False
    for line in codeLines:
        highlight = line['highlight']
        if type(highlight) is list:
            for h in highlight:
                if '#text' in h:
                    word = h['#text']
                    if word is not None:
                        if word == 'abstract':
                            flag = True
    return flag


def handleEdgeCreation(base, edges, nodes, node_set, edge_set):
    """ Manejar la creación de las aristas de un archivo.

    Parameters
    ----------
    base: dict
        diccionario con información del nodo
    nodes: list
        lista con todos los nodos de la arquitectura
    edges: list
        lista con todas las aristas de la arquitectura
    node_set: set
        set para mantener constancia de los nodos ya creados
    edge_set
        set pata mantener constancia de las aristas ya creadas
    """
    codeline = base['programlisting']['codeline']
    for line in codeline:
        highlight = line['highlight']
        if highlight:
            if type(highlight) is list:
                L = len(highlight)
                if '#text' in highlight[L-2]:
                    relation = highlight[L-2]['#text']
                if relation is None:
                    continue
                if relation == 'implements':
                    class_name = getClassName(highlight, L)
                    all_classes = handleClassDivision(class_name)
                    for c in all_classes:
                        if c == "":
                            continue
                        createEdge(base, c, relation,
                                   edges, nodes, node_set, edge_set)
                elif relation == 'extends':
                    class_name = getClassName(highlight, L)
                    if 'implements' not in class_name:
                        all_classes = handleClassDivision(class_name)
                        for c in all_classes:
                            if c == "":
                                continue
                            createEdge(base, c,
                                       relation, edges, nodes, node_set, edge_set)
                    else:
                        classes = class_name.split('implements')
                        all_extends = handleClassDivision(classes[0])
                        all_implements = ''
                        if classes[len(classes)-1] == '':
                            temp_implements = highlight[L-1]['ref']['#text']
                            all_implements = handleClassDivision(
                                temp_implements)
                        else:
                            all_implements = handleClassDivision(classes[1])
                        for c in all_extends:
                            if c == "":
                                continue
                            createEdge(base, c,
                                       relation, edges, nodes, node_set, edge_set)
                        for c in all_implements:
                            if c == "":
                                continue
                            createEdge(base, c,
                                       "implements", edges, nodes, node_set, edge_set)
            else:
                if '#text' in highlight:
                    if checkUse(highlight['#text']):
                        class_name = ''
                        relation = 'use'
                        if highlight['#text'] == 'use;':
                            class_name = getUseClassName(
                                highlight['ref']['#text'])
                        else:
                            class_name = getUseClassName(highlight['#text'])

                        createEdge(base, class_name, relation,
                                   edges, nodes, node_set, edge_set)


def checkUse(base):
    """ Comprobar si la clase está siendo
    utilizada
    Parameters
    ----------
    base: string
        string con la información de la clase
    """
    if len(base) < 3:
        return False
    temp = base[0:3]
    if temp == 'use':
        return True
    else:
        return False


def getUseClassName(base):
    """ Obtener el nombre de la clase de
    tipo use de un nodo

    Parameters
    ----------
    base: string
        string con la información de la clase

    Returns
    -------
    str
        nombre de la clase
    """
    class_name = ""

    for c in base[::-1]:
        if c == "\\":
            break
        class_name = c + class_name

    if class_name[len(class_name)-1] == ';':
        class_name = class_name[0:len(class_name)-1]

    if class_name[0:3] == 'use':
        class_name = class_name[3:len(class_name)]
    # Casos Aislados
    if class_name == "ContainerInterfaceasPsrInterface":
        class_name = 'PsrInterface'

    if class_name == "ContainerInterfaceasPsrContainerInterface":
        class_name = 'PsrInterface'

    if class_name == "ConsoleInputasConsoleInputBase":
        class_name = "ConsoleInputBase"

    if class_name == "ConsoleOutputasConsoleOutputBase":
        class_name = "ConsoleOutputBase"

    return class_name


def getClassName(base, L):
    """ Obtener el nombre de la clase de un nodo

    Parameters
    ----------
    base: list
        lista con la información de la clase
    L: int
        tamaño de la lista

    Returns
    -------
    str
        nombre de la clase
    """
    try:
        class_name = base[L-1]['#text']
        return class_name
    except:
        class_name = base[L-1]['ref']['#text']
        return class_name


def createEdge(base, class_name, relation, edges, nodes, node_set, edge_set):
    """ Creación del objeto arista.

    Parameters
    ----------
    base: dict
        diccionario con información del nodo
    class_name: str
        nombre de la clase
    relation: str
        tipo de relación
    edges: list
        lista con todas las aristas de la arquitectura
    nodes: list
        lista con todos los nodos de la arquitectura
    node_set: set
        set para mantener constancia de los nodos ya creados
    edge_set
        set pata mantener constancia de las aristas ya creadas
    """
    source_class_name = getClassId(base)
    target_class_name = class_name
    if target_class_name not in node_set:
        createNode2(target_class_name, nodes, node_set)
    data = {
        "id": source_class_name + "-" + target_class_name,
        "name": source_class_name + "-" + target_class_name,
        "source": source_class_name,
        "target": target_class_name,
        "bg": '#18202C'

    }
    scratch = {
        "relation": relation
    }
    if data['id'] not in edge_set:
        edges.append({"data": data, "scratch": scratch})
        edge_set.add(data['id'])
    else:
        if scratch['relation'] != 'use':
            for i in range(len(edges)):
                if edges[i]['data'] == data:
                    edges[i]['scratch'] = scratch
                    break


def createNode2(class_name, nodes, node_set):
    """ Creación del objeto nodo e inclusión en el
    arreglo y set de nodos

    Parameters
    ----------
    class_name: str
        nombre de la clase
    nodes: list
        lista con todos los nodos de la arquitectura
    node_set: set
        set para mantener constancia de los nodos ya creados

    Returns
    -------
    dict
        diccionario con el objeto nodo creado
    """
    flag = None
    if "interface" in class_name.lower():
        flag = True
    else:
        flag = False

    node = {
        "data": {
            "id": class_name,
            "name": class_name,
            "module": None,
            "isInterface": flag,
            "bg": '#18202C'
        }
    }
    node_set.add(class_name)
    nodes.append(node)
    return node


def handleClassDivision(class_name):
    """ Obtención de un arreglo con todas las clases
    relacionadas con un nodo

    Parameters
    ----------
    class_name: str
        nombre de la clase

    Returns
    -------
    list
        lista con todas las clases
    """
    if "\\" in class_name:
        return class_name.split("\\")
    return class_name.split(",")


def getNodeIds(nodes):
    """ Obtención del set con todos los nodos de
    una arquitectura.

    Parameters
    ----------
    nodes: list
        lista con todos los nodos de la arquitectura

    Returns
    -------
    set
        set con todos los nodos de la arquitectura sin repetición
    """
    node_ids = set()
    for node in nodes:
        node_ids.add(node['data']['id'])
    return node_ids


def getEdgeIds(edges):
    """" Obtención del set con todas las aristas
    de una arquitectura.

    Parameters
    ----------
    edges: list
        lista con todas las aristas de la arquitectura

    Returns
    -------
    set
        set con todas las aristas de la arquitectura sin repetición
    """
    edge_ids = set()
    for edge in edges:
        edge_ids.add(edge['data']['id'])
    return edge_ids
