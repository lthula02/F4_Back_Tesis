import graphviz
import os
from apps.metrics.helpers.variability.data import handleVariabilityDiagram
from apps.metrics.helpers.variability.vardatahandler import handleccdesc
from apps.metrics.helpers.variability.vardatahandler import handlescdesc


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
    for i in range(0, len(words), 6):
        new_string += " ".join(words[i : i + 6]) + "\n"

    return new_string


def styleedge(comp):
    """Define el tipo de línea según el valor lógico dado"""
    if comp == "and":
        return "solid"
    elif comp == "or":
        return "dashed"
    elif comp == "xor":
        return "dotted"


def creategraph(graph, cclist, sclist):
    """Crea nodos a partir de las listas de componentes simples y compuestos creadas anteriormente"""
    # Lista para asegurar que no tenemos edges repetidos
    edgelist = []
    # Descripciones cc

    for cc in cclist:
        graph.node(
            cc["description"],
            cc["description"],
            shape="box",
            style="rounded,filled",
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
        if len(sc["description"].split()) > 6:
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
        # Edges nivel 2 al 3
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
            style="rounded,filled",
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
    name = "Prueba"
    # Contador de número de gráficos generados para crear el nombre del pdf
    cont = 0
    while os.path.exists(
        f"C:\\TESISBEHRENSBRICENO\\diagrama_de_variabilidad_{name}v{cont}"
    ):
        cont += 1

    filename = f"C:\\TESISBEHRENSBRICENO\\diagrama_de_variabilidad_{name}v{cont}"
    # Crea el grafo
    graph = graphviz.Graph("Grafo", filename=filename)

    archs = handleVariabilityDiagram(data)
    scnodes = handlescdesc(archs)
    ccnodes = handleccdesc(archs)

    # crear nodo cabeza

    # Nombre de arquitectura de referencia (Pedir al usuario seguramente)

    graph.node("head", name, shape="box", fontsize="18", bold="True", style="rounded")
    creategraph(graph, ccnodes, scnodes)

    # Crea subgrafo para la leyenda
    s = graphviz.Graph("Leyenda")

    s.node("pnonmand4", " ", shape="plain", fontsize="8")
    s.node("pmand4", " ", shape="plain", fontsize="8")
    s.node("pand4", " ", shape="plain", fontsize="8", bold="True")
    s.node("por4", " ", shape="plain", fontsize="8", bold="True")
    s.node("pxor4", " ", shape="plain", fontsize="8")
    s.node("pfun4", " ", shape="plain", fontsize="8", bold="True")
    s.node("pasp4", " ", shape="plain", fontsize="8", bold="True")
    s.node("pclass4", " ", shape="plain", fontsize="8")

    s.node("pnonmand3", " ", shape="plain", fontsize="8")
    s.node("pmand3", " ", shape="plain", fontsize="8")
    s.node("pand3", " ", shape="plain", fontsize="8", bold="True")
    s.node("por3", " ", shape="plain", fontsize="8", bold="True")
    s.node("pxor3", " ", shape="plain", fontsize="8")
    s.node("pfun3", " ", shape="plain", fontsize="8", bold="True")
    s.node("pasp3", " ", shape="plain", fontsize="8", bold="True")
    s.node("pclass3", " ", shape="plain", fontsize="8")

    s.node("pnonmand2", " ", shape="plain", fontsize="8")
    s.node("pmand2", " ", shape="plain", fontsize="8")
    s.node("pand2", " ", shape="plain", fontsize="8", bold="True")
    s.node("por2", " ", shape="plain", fontsize="8", bold="True")
    s.node("pxor2", " ", shape="plain", fontsize="8")
    s.node("pfun2", " ", shape="plain", fontsize="8", bold="True")
    s.node("pasp2", " ", shape="plain", fontsize="8", bold="True")
    s.node("pclass2", " ", shape="plain", fontsize="8")

    s.node("pnonmand1", " ", shape="plain", fontsize="8")
    s.node("pmand1", " ", shape="plain", fontsize="8")
    s.node("pand1", " ", shape="plain", fontsize="8", bold="True")
    s.node("por1", " ", shape="plain", fontsize="8", bold="True")
    s.node("pxor1", " ", shape="plain", fontsize="8")
    s.node("pfun1", " ", shape="plain", fontsize="8", bold="True")
    s.node("pasp1", " ", shape="plain", fontsize="8", bold="True")
    s.node("pclass1", " ", shape="plain", fontsize="8")

    s.node("pnonmand", " ", shape="plain", fontsize="8")
    s.node("pmand", " ", shape="plain", fontsize="8")
    s.node("pand", " ", shape="plain", fontsize="8", bold="True")
    s.node("por", " ", shape="plain", fontsize="8", bold="True")
    s.node("pxor", " ", shape="plain", fontsize="8")
    s.node("pfun", " ", shape="plain", fontsize="8", bold="True")
    s.node("pasp", " ", shape="plain", fontsize="8", bold="True")
    s.node("pclass", " ", shape="plain", fontsize="8")

    s.node("mand", "Obligatorio", shape="plain", fontsize="10")
    s.node("nonmand", "Opcional", shape="plain", fontsize="10")
    s.node("and", "And", shape="plain", fontsize="10", bold="True")
    s.node("or", "Or", shape="plain", fontsize="10", bold="True")
    s.node("xor", "Alternativa", shape="plain", fontsize="10")

    s.node(
        "fun",
        "Funcionalidad",
        shape="box",
        fontsize="10",
        style="rounded,filled",
        fillcolor="khaki1",
    )
    s.node(
        "asp",
        "Aspecto",
        shape="box",
        fontsize="10",
        style="rounded,filled",
        fillcolor="lightblue",
    )
    s.node(
        "class",
        "Clase",
        shape="box",
        fontsize="10",
        style="rounded,filled",
        fillcolor="lightpink",
    )

    # s.node('ley', 'Leyenda', shape='plain', fontsize='24')

    # s.edge('asp', 'fun', dir='forward', arrowhead='none', style='invis' )
    # s.edge('fun', 'class', dir='forward', arrowhead='none', style='invis' )

    # s.edge('ley', 'asp', arrowhead='none', style='invis')
    # s.edge('ley', 'fun', arrowhead='none', style='invis')
    # s.edge('ley', 'class', arrowhead='none', style='invis')
    s.edge("pnonmand4", "pnonmand3", dir="forward", arrowhead="none", style="invis")
    s.edge("pnonmand3", "pnonmand2", dir="forward", arrowhead="none", style="invis")
    s.edge("pnonmand2", "pnonmand1", dir="forward", arrowhead="none", style="invis")
    s.edge("pnonmand1", "pnonmand", dir="forward", arrowhead="none", style="invis")

    s.edge("pmand4", "pmand3", dir="forward", arrowhead="none", style="invis")
    s.edge("pmand3", "pmand2", dir="forward", arrowhead="none", style="invis")
    s.edge("pmand2", "pmand1", dir="forward", arrowhead="none", style="invis")
    s.edge("pmand1", "pmand", dir="forward", arrowhead="none", style="invis")

    s.edge("pand4", "pand3", dir="forward", arrowhead="none", style="invis")
    s.edge("pand3", "pand2", dir="forward", arrowhead="none", style="invis")
    s.edge("pand2", "pand1", dir="forward", arrowhead="none", style="invis")
    s.edge("pand1", "pand", dir="forward", arrowhead="none", style="invis")

    s.edge("por4", "por3", dir="forward", arrowhead="none", style="invis")
    s.edge("por3", "por2", dir="forward", arrowhead="none", style="invis")
    s.edge("por2", "por1", dir="forward", arrowhead="none", style="invis")
    s.edge("por1", "por", dir="forward", arrowhead="none", style="invis")

    s.edge("pxor4", "pxor3", dir="forward", arrowhead="none", style="invis")
    s.edge("pxor3", "pxor2", dir="forward", arrowhead="none", style="invis")
    s.edge("pxor2", "pxor1", dir="forward", arrowhead="none", style="invis")
    s.edge("pxor1", "pxor", dir="forward", arrowhead="none", style="invis")

    # s.edge('pfun4', 'pfun3', dir='forward', arrowhead='none', style='invis' )
    s.edge("pfun3", "pfun2", dir="forward", arrowhead="none", style="invis")
    s.edge("pfun2", "pfun1", dir="forward", arrowhead="none", style="invis")
    s.edge("pfun1", "pfun", dir="forward", arrowhead="none", style="invis")

    # s.edge('pasp4', 'pasp3', dir='forward', arrowhead='none', style='invis' )
    s.edge("pasp3", "pasp2", dir="forward", arrowhead="none", style="invis")
    s.edge("pasp2", "pasp1", dir="forward", arrowhead="none", style="invis")
    s.edge("pasp1", "pasp", dir="forward", arrowhead="none", style="invis")

    # s.edge('pclass4', 'pclass3', dir='forward', arrowhead='none', style='invis' )
    s.edge("pclass3", "pclass2", dir="forward", arrowhead="none", style="invis")
    s.edge("pclass2", "pclass1", dir="forward", arrowhead="none", style="invis")
    s.edge("pclass1", "pclass", dir="forward", arrowhead="none", style="invis")

    s.edge("pmand", "mand", dir="forward", arrowhead="dot", style="solid")
    s.edge("pnonmand", "nonmand", dir="forward", arrowhead="odot", style="solid")
    s.edge("pand", "and", dir="forward", style="solid", arrowhead="none")
    s.edge("por", "or", dir="forward", style="dashed", arrowhead="none")
    s.edge("pxor", "xor", dir="forward", style="dotted", arrowhead="none")
    s.edge("pand", "and", dir="forward", style="solid", arrowhead="none")
    s.edge("por", "or", dir="forward", style="dashed", arrowhead="none")
    s.edge("pxor", "xor", dir="forward", style="dotted", arrowhead="none")
    s.edge("pclass", "class", dir="forward", arrowhead="none", style="invis")
    s.edge("pasp", "asp", dir="forward", arrowhead="none", style="invis")
    s.edge("pfun", "fun", dir="forward", arrowhead="none", style="invis")

    j = graph.subgraph(graph=s)

    graph.view()

    # time.sleep(3)
    # os.remove(f'{filename}')
    # os.remove(f'{filename}.pdf')
