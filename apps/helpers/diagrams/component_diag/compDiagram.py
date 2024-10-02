import graphviz
import os
from firebase_admin import db
from apps.helpers.diagrams.component_diag.compdata import (
    handleComponentData,
)  # De aquí se extraen los datos
from apps.helpers.diagrams.component_diag.compdatahandler import count_aspects


def initComponentDiagram(data):
    """
    Creación del diagrama de componentes
    """

    uid = data["user_id"]
    project_index = data["project_index"]
    url = "/users/" + uid + "/projects/" + str(project_index)

    architectures_ref = db.reference(url + "/name")
    name = architectures_ref.get()

    cont = 0

    while os.path.exists(
        f"C:\\TESISFINAL\\diagrama_de_componentes_{name}v{cont}"
    ):
        cont += 1

    filename = f"C:\\TESISFINAL\\diagrama_de_componentes_{name}v{cont}"
    graph = graphviz.Graph("Diagrama de componentes", filename=filename)
    graph.graph_attr["splines"] = "line"
    # graph.graph_attr["splines"] = "ortho"

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
            graph.edge(
                f'aux{comp["name"]}{i}',
                req,
                dir="forward",
                style="plain",
                arrowhead="none",
            )

    # Crea subgrafo para la leyenda
    # s = graphviz.Graph("Leyenda")

    # Crea texto de pie de grafo
    auxtext = "\n\nCantidad de arquitecturas en las que está presente\n\n"
    for d in compdata:
        name = d["name"]
        cnt = str(d["count"])
        total = len(archs_compdata)
        auxtext += f"{name}: {cnt}/{total}\n"

    graph.graph_attr["fontsize"] = "8"
    graph.graph_attr["label"] = auxtext

    # s.node("l2", auxtext, shape="plain", fontsize="8")

    # j = graph.subgraph(graph=s)

    graph.view()
