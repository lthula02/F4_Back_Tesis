import graphviz
import os
from apps.helpers.diagrams.class_diag.classdata import (
    handleClassData,
)


def initClassDiagram(data):
    name, classdata = handleClassData(data)
    cont = 0

    while os.path.exists(f"C:\\TESISFINAL\\diagrama_de_clases_{name}v{cont}"):
        cont += 1

    filename = f"C:\\TESISFINAL\\diagrama_de_clases_{name}v{cont}"
    
    graph = graphviz.Graph("Diagrama de clases", filename=filename)
    graph.graph_attr["splines"] = "line"
    graph.graph_attr["fontsize"] = "10"
    graph.graph_attr["label"] = f"{name}"
    # graph.attr("splines", "line")
    # Add nodes to the graph

    # Creación de nodos de cada clase

    def bodytotext(body):
        resp = ""
        for b in body:
            resp += b
            resp += "&#92;n"

        return resp

    # Creación de los nodos
    for cl in classdata:
        # print(bodytotext(cl["body"]))
        textlabel = "{" + "\<" + cl["head"] + "\>" + "|" + bodytotext(cl["body"]) + "}"
        graph.node(cl["head"], label=textlabel, shape="record", fontsize="8")

    edgelist = []

    for cl in classdata:
        for req in cl["requires"]:
            tup1 = (cl["head"], req)
            tup2 = (req, cl["head"])

            if tup1 not in edgelist and tup2 not in edgelist:
                graph.edge(cl["head"], req, dir="none", style="solid")
                edgelist.append(tup1)
                edgelist.append(tup2)

    graph.view()
