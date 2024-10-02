import graphviz
import os
from firebase_admin import db
from apps.helpers.diagrams.variability.data import handleVariabilityData
from apps.helpers.diagrams.variability.vardatahandler import (
    handleccdesc,
    handlescdesc,
    handlemlist,
    handlescarq,
)


def arrowhead(comp):
    """Define la punta de la flecha dependiendo de si un compomnente es obligatorio o no"""
    if comp:
        return "dot"
    else:
        return "odot"


def line_breaks(string):
    """Agrega saltos de línea cada 4 palabras en un string largo"""

    words = string.split()
    new_string = ""
    for i in range(0, len(words), 4):
        new_string += " ".join(words[i : i + 4]) + "\n"

    return new_string


def styleedge(comp):
    """
    Define el tipo de línea según el valor lógico dado
    """

    if comp == "and":
        return "solid"
    elif comp == "or":
        return "dashed"
    elif comp == "xor":
        return "dotted"


def creategraph(graph, cclist, sclist, mlist):
    """
    Crea nodos a partir de las listas de componentes simples y compuestos creadas anteriormente
    """

    # Lista para asegurar que no tenemos edges repetidos
    edgelist = []
    # Descripciones de aspectos

    for cc in cclist:
        # Crea nodos para los componentes compuestos
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

    # Descripciones nodos conectadas con su padre
    for sc in sclist:
        if len(sc["description"].split()) > 4:
            des = line_breaks(sc["description"])
        else:
            des = sc["description"]
        # Crea nodos para las funcionalidades
        graph.node(
            sc["description"],
            des,
            shape="box",
            style="rounded,filled",
            fillcolor="khaki1",
        )
        # Edges nivel 2 al 3 -> Aspecto a funcionalidad
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

    # Nodos conectados con su descripción
    for sc in sclist:
        # Crea nodos para las clases
        graph.node(
            sc["name"],
            f'{sc["name"] + handlescarq(mlist, sc["name"], sc["mandatory_name"])}',
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


def initVariabilityDiagram(data):
    """
    Función principal para crear el diagrama
    """
    uid = data["user_id"]
    project_index = data["project_index"]
    url = "/users/" + uid + "/projects/" + str(project_index)

    architectures_ref = db.reference(url + "/name")
    name = architectures_ref.get()

    # Contador de número de gráficos generados para crear el nombre del pdf
    cont = 0
    while os.path.exists(
        f"C:\\TESISFINAL\\diagrama_de_variabilidad_{name}v{cont}"
    ):
        cont += 1

    filename = f"C:\\TESISFINAL\\diagrama_de_variabilidad_{name}v{cont}"

    # Crea el grafo
    graph = graphviz.Graph("Grafo", filename=filename)
    graph.graph_attr["splines"] = "polyline"
    graph.graph_attr["rankdir"] = "LR"

    # Funciones para el manejo de la data
    archs = handleVariabilityData(data)
    archs = handlemlist(archs)
    scnodes = handlescdesc(archs)
    ccnodes = handleccdesc(archs)

    # Nodo del título
    graph.node(
        "head", name.upper(), shape="underline", fontsize="24", fontname="times-bold"
    )
    creategraph(graph, ccnodes, scnodes, archs)

    # Se crea la leyenda, a partir de un subgrafo

    # Crea subgrafo
    s = graphviz.Graph("Leyenda")

    # Nodos auxiliares transparentes
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
    s.node("pand", " ", shape="plain", fontsize="8", bold="True")
    s.node("pxor", " ", shape="plain", fontsize="8", bold="True")
    s.node("pnonmand", " ", shape="plain", fontsize="8")
    s.node("pmand", " ", shape="plain", fontsize="8")
    s.node("por", " ", shape="plain", fontsize="8", bold="True")

    # Nodos con contenido
    s.node("xor", "  Alternativa", shape="plain", fontsize="16", bold="True")
    s.node("and", "  And", shape="plain", fontsize="16", bold="True")
    s.node("ley", "LEYENDA", shape="underline", fontsize="24", fontname="times-bold")
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
    s.edge("pxor", "xor", dir="forward", style="dotted", arrowhead="none")
    s.edge("pxor", "xor", dir="forward", style="dotted", arrowhead="none")

    j = graph.subgraph(graph=s)

    graph.view()
