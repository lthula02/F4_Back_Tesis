import graphviz
import os
from firebase_admin import db
from apps.metrics.helpers.variability.data import handleVariabilityData
from apps.metrics.helpers.variability.vardatahandler import handleccdesc
from apps.metrics.helpers.variability.vardatahandler import handlescdesc
from apps.metrics.helpers.variability.vardatahandler import handlemlist


import time


def arrowhead(comp):
    """Define la punta de la flecha dependiendo de si un compomnente es obligatorio o no"""
    if comp:
        return "dot"
    else:
        return "odot"


def line_breaks(string):
    """Agrega saltos de línea cada 6 palabras en un string largo"""

    words = string.split()
    new_string = ""
    for i in range(0, len(words), 4):
        new_string += " ".join(words[i : i + 4]) + "\n"

    return new_string


def styleedge(comp):
    """Define el tipo de línea según el valor lógico dado"""
    if comp == "and":
        return "solid"
    elif comp == "or":
        return "dashed"
    elif comp == "xor":
        return "dashed"


def creategraph(graph, cclist, sclist):
    """Crea nodos a partir de las listas de componentes simples y compuestos creadas anteriormente"""
    # Lista para asegurar que no tenemos edges repetidos
    edgelist = []
    # Descripciones cc

    for cc in cclist:
        graph.node(
            cc["description"],
            cc["description"],
            shape="oval",
            style="filled",
            fillcolor="lightblue",
        )
        edge = {"from": "head", "to": cc["description"]}
        # Revisa que no haya edges repetidos
        if edge in edgelist:
            pass
        else:
            # Edges nivel 1 al 2
            edgelist.append(edge)
            graph.edge(
                "head",
                cc["description"],
                arrowhead=arrowhead(cc["mandatory"]),
                dir="forward",
                style=styleedge(cc["logical"]),
            )

    # Descripciones sc conectadas con su padre
    for sc in sclist:
        if len(sc["description"].split()) > 4:
            des = line_breaks(sc["description"])
        else:
            des = sc["description"]
        graph.node(
            sc["description"],
            des,
            shape="box",
            style="rounded,filled",
            fillcolor="khaki1",
        )
        # Edges nivel 2 al 3 -> Aspecto a descripcion
        edge = {"from": sc["parent"], "to": sc["description"]}
        if edge in edgelist:
            pass
        else:
            edgelist.append(edge)
            graph.edge(
                sc["parent"],
                sc["description"],
                arrowhead=arrowhead(sc["mandatory"]),
                dir="forward",
                style=styleedge(sc["logical"]),
            )

    # SC conectados con su descripción
    for sc in sclist:
        graph.node(
            sc["name"],
            sc["name"],
            shape="box",
            style="filled",
            fillcolor="lightpink",
        )

        edge = {"from": sc["description"], "to": sc["name"]}
        if edge in edgelist:
            pass
        else:
            # Edges nivel 3 al 4
            edgelist.append(edge)
            graph.edge(
                sc["description"],
                sc["name"],
                dir="forward",
                arrowhead=arrowhead(sc["mandatory_name"]),
                style=styleedge(sc["son_logical"]),
            )
            # taillabel=sc['logical']


def initVariabilityDiagram(data):
    uid = data["user_id"]
    project_index = data["project_index"]
    url = "/users/" + uid + "/projects/" + str(project_index)

    architectures_ref = db.reference(url + "/name")
    name = architectures_ref.get()

    # Contador de número de gráficos generados para crear el nombre del pdf
    cont = 0
    while os.path.exists(
        f"C:\\TESISBEHRENSBRICENO\\diagrama_de_variabilidad_{name}v{cont}"
    ):
        cont += 1

    filename = f"C:\\TESISBEHRENSBRICENO\\diagrama_de_variabilidad_{name}v{cont}"
    # Crea el grafo
    graph = graphviz.Graph("Grafo", filename=filename)
    # Tambien sirve 'spline
    graph.graph_attr["splines"] = "polyline"
    graph.graph_attr["rankdir"] = "LR"

    archs = handleVariabilityData(data)
    archs = handlemlist(archs)
    scnodes = handlescdesc(archs)
    ccnodes = handleccdesc(archs)

    # crear nodo cabeza

    # Nombre de arquitectura de referencia (Pedir al usuario seguramente)

    graph.node(
        "head", name.upper(), shape="underline", fontsize="24", fontname="times-bold"
    )
    creategraph(graph, ccnodes, scnodes)

    # Crea subgrafo para la leyenda
    s = graphviz.Graph("Leyenda")

    s.node("por4", " ", shape="plain", fontsize="8", bold="True")
    s.node("pfun4", " ", shape="plain", fontsize="8", bold="True")
    s.node("pasp4", " ", shape="plain", fontsize="8", bold="True")
    s.node("pclass4", " ", shape="plain", fontsize="8")
    s.node("por3", " ", shape="plain", fontsize="8", bold="True")
    s.node("pfun3", " ", shape="plain", fontsize="8", bold="True")
    s.node("pasp3", " ", shape="plain", fontsize="8", bold="True")
    s.node("pclass3", " ", shape="plain", fontsize="8")
    s.node("por2", " ", shape="plain", fontsize="8", bold="True")
    s.node("por1", " ", shape="plain", fontsize="8", bold="True")
    s.node("pfun1", " ", shape="plain", fontsize="8", bold="True")
    s.node("pasp1", " ", shape="plain", fontsize="8", bold="True")
    s.node("pclass1", " ", shape="plain", fontsize="8")

    s.node("and", "  And", shape="plain", fontsize="16", bold="True")
    s.node("pand", " ", shape="plain", fontsize="8", bold="True")

    s.node("pnonmand", " ", shape="plain", fontsize="8")
    s.node("pmand", " ", shape="plain", fontsize="8")

    s.node("por", " ", shape="plain", fontsize="8", bold="True")

    s.node("ley", "LEYENDA", shape="underline", fontsize="24", fontname="times-bold")
    # s.node("pfun", " ", shape="plain", fontsize="8", bold="True")
    # s.node("pasp", " ", shape="plain", fontsize="8", bold="True")
    # s.node("pclass", " ", shape="plain", fontsize="8")

    s.node("mand", "  Obligatorio", shape="plain", fontsize="16")
    s.node("nonmand", "  Opcional", shape="plain", fontsize="16")

    s.node("or", "  Or", shape="plain", fontsize="16", bold="True")

    s.node(
        "fun",
        "Funcionalidad",
        shape="box",
        fontsize="16",
        style="rounded,filled",
        fillcolor="khaki1",
    )
    s.node(
        "asp",
        "Aspecto",
        shape="oval",
        fontsize="16",
        style="filled",
        fillcolor="lightblue",
    )
    s.node(
        "class",
        "Clase",
        shape="box",
        fontsize="16",
        style="filled",
        fillcolor="lightpink",
    )

    # EDGES

    s.edge("por4", "por3", dir="forward", arrowhead="none", style="dotted")
    s.edge("por3", "por2", dir="forward", arrowhead="none", style="dotted")
    s.edge("por2", "por1", dir="forward", arrowhead="none", style="dotted")
    s.edge("por1", "por", dir="forward", arrowhead="none", style="dotted")

    s.edge("nonmand", "pasp1", dir="forward", arrowhead="none", style="invis")
    s.edge("pasp3", "nonmand", dir="forward", arrowhead="odot", style="solid")

    s.edge("mand", "pfun1", dir="forward", arrowhead="none", style="invis")
    s.edge("pfun3", "mand", dir="forward", arrowhead="dot", style="solid")

    s.edge("pfun1", "fun", dir="forward", arrowhead="none", style="invis")

    s.edge("pasp1", "asp", dir="forward", arrowhead="none", style="invis")

    s.edge("or", "pclass1", dir="forward", arrowhead="none", style="invis")
    s.edge("pclass1", "class", dir="forward", arrowhead="none", style="invis")

    s.edge("pclass3", "or", dir="forward", style="dashed", arrowhead="none")
    s.edge("pclass3", "or", dir="forward", style="dashed", arrowhead="none")
    s.edge("pand", "and", dir="forward", style="solid", arrowhead="none")
    s.edge("pand", "and", dir="forward", style="solid", arrowhead="none")
    # s.edge("pclass", "class", dir="forward", arrowhead="none", style="invis")
    # s.edge("pasp", "asp", dir="forward", arrowhead="none", style="invis")
    # s.edge("pfun", "fun", dir="forward", arrowhead="none", style="invis")

    j = graph.subgraph(graph=s)

    graph.view()

    # time.sleep(3)
    # os.remove(f'{filename}')
    # os.remove(f'{filename}.pdf')
