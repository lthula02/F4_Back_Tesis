import graphviz
import os
from firebase_admin import db
from apps.metrics.helpers.component_diag.compdata import (
    handleComponentData,
)  # De aquí se extraen los datos
from apps.metrics.helpers.component_diag.compdatahandler import count_aspects

# Create a graph object
"""Para crear este grafo necesitamos una lista de componentes con sus relaciones
    importante no crearlo con el name (id) sino con la descripción que le da el arquitecto (nombre de aspecto)
Ej.
{'name': 'Transmision', 'relates_to': ['Confort', 'Entretenimiento'] }

"""


def initComponentDiagram(data):
    uid = data["user_id"]
    project_index = data["project_index"]
    url = "/users/" + uid + "/projects/" + str(project_index)

    architectures_ref = db.reference(url + "/name")
    name = architectures_ref.get()

    cont = 0

    while os.path.exists(
        f"C:\\TESISBEHRENSBRICENO\\diagrama_de_componentes_{name}v{cont}"
    ):
        cont += 1

    filename = f"C:\\TESISBEHRENSBRICENO\\diagrama_de_componentes_{name}v{cont}"
    graph = graphviz.Graph("Diagrama de componentes", filename=filename)
    graph.graph_attr["splines"] = "ortho"
    # graph.attr("splines", "line")
    # Add nodes to the graph

    archs_compdata = handleComponentData(data)
    compdata = count_aspects(archs_compdata)

    # Creación de nodos

    for comp in compdata:
        graph.node(comp["name"], comp["name"], shape="component", fontsize="12")
        if len(comp["requires"]) > 0:
            for i, compr in enumerate(comp["requires"]):
                graph.node(
                    f'aux{comp["name"]}{i}',
                    " ",
                    shape="point",
                    style="filled",
                    fillcolor="white",
                    width="0.1",
                )
                graph.edge(
                    comp["name"],
                    f'aux{comp["name"]}{i}',
                    dir="forward",
                    style="plain",
                    arrowhead="icurve",
                )

    for comp in compdata:
        for i, req in enumerate(comp["requires"]):
            # graph.edge(comp['name'], req, dir='both', style='plain', arrowhead='curve', arrowtail='odot')
            graph.edge(
                f'aux{comp["name"]}{i}',
                req,
                dir="forward",
                style="plain",
                arrowhead="none",
            )

    # graph.node('dist' , '                   ', shape="plain")
    # graph.node('c3' , 'c3', shape="component", fontsize='12', style='filled', fillcolor='orange')
    # graph.node('c4' , 'c4', shape="component", fontsize='12', style='filled', fillcolor='yellow1')
    # graph.node('c5' , 'c5', shape="component", fontsize='12', style='filled', fillcolor='wheat1')
    # graph.node('c6' , 'c6', shape="component", fontsize='12', style='filled', fillcolor='red')

    # graph.node('c7' , ' ', shape="plain", fontsize='1')

    # graph.edge('c1', 'c7', dir='forward', style='plain', arrowhead='odot')
    # graph.edge('c2', 'c7',  dir='forward', style='plain', arrowhead='icurve')

    # graph.edge('c1', 'c2',  dir='forward', style='dashed')
    # graph.edge('c1', 'c5',  dir='forward', style='dashed')
    # graph.edge('c5', 'c3',  dir='forward', style='dashed')
    # graph.edge('c6', 'c2',  dir='forward', style='dashed')
    # graph.edge('c5', 'c6',  dir='forward', style='dashed')
    # graph.edge('c4', 'c2',  dir='forward', style='dashed')
    # graph.edge('c4', 'c1',  dir='forward', style='dashed')

    # Crea subgrafo para la leyenda
    s = graphviz.Graph("Leyenda")
    auxtext = "\n\nCantidad de veces presente en las arquitecturas estudiadas\n\n"
    for d in compdata:
        name = d["name"]
        cnt = str(d["count"])
        total = len(archs_compdata)
        auxtext += f"{name}: {cnt}/{total}\n"

    graph.graph_attr["fontsize"] = "8"
    graph.graph_attr["label"] = auxtext

    # s.node('l0' , '                                   ', shape="plain", fontsize='8')
    # s.node('l1' , auxtext, shape="plain", fontsize='8')

    # s.edge('l0', 'l01',  dir='both', style='invis')
    # s.edge('l1', 'l3',  dir='both', style='invis')
    # s.edge('l2', 'l4',  dir='both', style='invis')
    # s.edge('l1', 'l2',  dir='both', style='invis')
    s.node("l2", "Consume de interfaz", shape="plain", fontsize="8")
    # s.edge('l2', 'l3',  dir='both', style='plain', arrowhead='curve', arrowtail='odot')
    graph.node(
        "aux", " ", shape="point", width="0.1", style="filled", fillcolor="white"
    )
    s.edge("l2", "aux", dir="forward", style="plain", arrowhead="icurve")
    s.edge("aux", "l3", dir="back", style="plain", arrowtail="none")

    s.node("l3", "Interfaz proporcionada", shape="plain", fontsize="8")

    j = graph.subgraph(graph=s)

    graph.view()
