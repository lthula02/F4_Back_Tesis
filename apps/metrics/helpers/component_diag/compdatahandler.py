"""Aca se van a crear las funciones para manejar la data que crea los diagramas de componentes"""


def count_aspects(compdata):  # (mlist, compdata)
    namelist = []
    """
    for c in mlist:
        for a in c:
            namelist.append(a['description'])
        
    print('NAMELIST ---------------------------------')
    print(namelist)
    """
    for comp in compdata:
        comp["count"] = namelist.count(comp["name"])
        print(comp["count"])
