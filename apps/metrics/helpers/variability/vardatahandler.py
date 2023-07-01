def createccnames(mlist):
    """
    Retorna un array auxiliar de diccionarios con nombre y descripción de los componentes compuestos

    """
    ccnames = []

    for i in range(len(mlist)):
        for j in range(len(mlist[i])):
            # Accedo al nombre de los carros
            name = mlist[i][j]["name"]
            desc = mlist[i][j]["description"]
            ccnames.append({"name": name, "description": desc})

    return ccnames


def createscnames(mlist):
    """Retorna: Lista con diccionarios que contienen nombre, descripción y padre de los componentes simples"""
    scnames = []
    for i in range(len(mlist)):
        for j in range(len(mlist[i])):
            # Accedo a la información de cada carro
            desc = mlist[i][j]["description"]
            for comp in mlist[i][j]["composite_component"]:
                comp["parent"] = desc
                comp["source"] = f"arq{i}"
                scnames.append(comp)

    return scnames


def ismandatory(mlist, auxlist, item):
    """
    Define si un componente es obligatorio o no
    Recibe: Lista de arquitecturas
            Lista auxiliar con X de un componente
            Item que se desea conocer su obligatoreidad
    """
    if auxlist.count(item) == len(mlist):
        return True
    else:
        return False


def handleccdesc(mlist):
    """Genera lista de diccionarios que contienen los nombres de componentes compuestos, su descripción y si son obligatorios"""
    mainlist = []
    descriptions = []
    ccnames = createccnames(mlist)

    for name in ccnames:
        descriptions.append(name["description"])

    auxdescriptions = list(set(descriptions))

    for description in auxdescriptions:
        mandatory = ismandatory(mlist, descriptions, description)
        components = []
        for comp in ccnames:
            if description == comp["description"]:
                if comp["description"] in components:
                    pass
                else:
                    components.append(comp["description"])
                    quant = descriptions.count(comp["description"])

        auxdic = {
            "description": description,
            "components": components,
            "mandatory": mandatory,
            "quantity": quant,
        }
        mainlist.append(auxdic)

        logical = ""

        if len(mlist) == 1:
            logical = "and"

        cont = 0
        for d in mainlist:
            if d["quantity"] == len(mlist):
                cont += 1

        if cont == len(mainlist):
            logical = "and"

        if logical == "":
            xor = True
            for d in mainlist:
                if d["quantity"] != 1:
                    xor = False

            if xor:
                logical = "xor"
            else:
                logical = "or"

        for e in mainlist:
            e["logical"] = logical

    return mainlist


def handlesclogical(sclist, mlist):
    """
    Agrega el valor lógico para las conexiones aspecto - funcionalidad
    """
    parentlist = []
    parentson = []
    sons = []

    for s in sclist:
        parentlist.append(s["parent"])

    for s in sclist:
        sons.append(s["description"])

    # Eliminamos padres repetidos
    parentlist = list(set(parentlist))
    # print(f"PARENTLIST => {parentlist}")

    for p in parentlist:
        sonlist = []
        for s in sclist:
            if s["parent"] == p:
                for i in range(s["son_count"]):
                    sonlist.append(
                        {"description": s["description"], "source": s["source"]}
                    )

        dic = {"parent": p, "son_list": sonlist, "source": s["source"]}
        parentson.append(dic)

    for sc in sclist:
        # recorremos lista de componentes simples
        for p in parentson:
            # recorremos lista de padre-hijo

            for son in p["son_list"]:
                # recorremos la lista de hijos de cada padre
                if sc["description"] == son["description"]:
                    # Hacemos el match del componente simple con el hijo

                    if len(p["son_list"]) == 1:
                        sc["logical"] = "and"

                    elif len(mlist) == sons.count(son["description"]):
                        sc["logical"] = "and"

                    else:
                        xor = True
                        # TODO
                        sources = []
                        for i in p["son_list"]:
                            sources.append(i["source"])
                            if p["son_list"].count(i) != 1:
                                xor = False
                        # print("------------------------------------")
                        # print(sc["description"])
                        # print(list(set(sources)))
                        # print("------------------------------------")
                        if xor and (len(list(set(sources))) > 1):
                            sc["logical"] = "xor"

                        elif len(list(set(sources))) == 1:
                            sc["logical"] = "and"
                        else:
                            sc["logical"] = "or"


def handlescdesc(mlist):
    """Genera lista de diccionarios con los nombres de los componentes simples, su padre, su descripción y si son únicos"""
    compclist = handleccdesc(mlist)
    scnames = createscnames(mlist)

    descriptions = []
    for name in scnames:
        descriptions.append(name["description"])

    # elimino descripciones repetidas
    auxdescriptions = list(set(descriptions))

    # creación de lista auxiliar de componente compuesto con sus hijos (componentes simples)
    parentson = []
    parentlist = []
    for p in scnames:
        parentlist.append(p["parent"])
    parentlist = list(set(parentlist))

    for parent in parentlist:
        sonlist = []
        for comp in scnames:
            if comp["parent"] == parent:
                sonlist.append(comp["name"])

        dic = {"parent": parent, "son_list": sonlist}
        parentson.append(dic)

    for description in auxdescriptions:
        for comp in scnames:
            if description == comp["description"]:
                for cm in parentson:
                    for c in cm["son_list"]:
                        if c == comp["name"]:
                            # if descriptions.count(description)
                            mandatory = ismandatory(mlist, descriptions, description)
                            comp["mandatory"] = mandatory

    components = []
    for sc in scnames:
        if sc in components:
            pass
        else:
            components.append(sc)

    handlescname(components, mlist)
    handlesclogical(components, mlist)

    return components


def handlescname(sclist, mainlist):
    parentlist = []
    parentson = []

    namelist = []
    for m in mainlist:
        for c in m:
            for h in c["composite_component"]:
                namelist.append(h["name"])
    # for sc in sclist:
    #     namelist.append(sc['name'])

    uniquenames = list(set(namelist))
    for sc in sclist:
        for name in uniquenames:
            if sc["name"] == name:
                mandatory = ismandatory(mainlist, namelist, name)
                sc["mandatory_name"] = mandatory
                sc["son_count"] = namelist.count(name)

    for sc in sclist:
        parentlist.append(sc["description"])
    parentlist = list(set(parentlist))

    for parent in parentlist:
        sonlist = []
        for comp in sclist:
            if comp["description"] == parent:
                sonlist.append(
                    {
                        "name": comp["name"],
                        "mandatory": comp["mandatory_name"],
                        "count": comp["son_count"],
                    }
                )

        dic = {"parent": parent, "son_list": sonlist, "mand": 0}
        parentson.append(dic)

    for ps in parentson:
        for son in ps["son_list"]:
            # Contador de cuántos hijos obligatorios hay

            if son["mandatory"]:
                ps["mand"] += 1

    for ps in parentson:
        for sc in sclist:
            if sc["description"] == ps["parent"]:
                # Actualiza valor lógico para hijos
                xor = False
                if len(ps["son_list"]) == 1:
                    sc["son_logical"] = "and"

                elif ps["mand"] == len(ps["son_list"]):
                    sc["son_logical"] = "and"
                else:
                    xor = True

                    for son in ps["son_list"]:
                        num = son["count"]

                        if num != 1:
                            xor = False
                    if xor:
                        sc["son_logical"] = "xor"
                    else:
                        sc["son_logical"] = "or"

                # elif ps['mand'] == 0:
                #     sc['logical'] = 'xor'
                # else:
                #     sc['logical'] = 'or'
