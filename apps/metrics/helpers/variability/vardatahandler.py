def handlemlist(mlist):
    '''
    Elimina los aspectos repetidos y relaciona todos los nodos a su respectivo aspecto, en cada arquitectura
    '''
    newlist =[]
    desclist=[]

    for i in mlist:
        newlist.append([])
        desclist.append([])


    for i in range(len(mlist)):
        for comp in mlist[i]:
            if comp['description'] in desclist[i]:
                for newcomp in newlist[i]:
                    if newcomp['description'] == comp['description']:
                        for k in comp['composite_component']:
                            if not (k in newcomp['composite_component']):
                                newcomp['composite_component'].append(k)
            else:
                desclist.append(comp['description'])
                newlist[i].append(comp)


    return newlist
                            
def createccnames(mlist):
    '''
    Retorna un array auxiliar de diccionarios con nombre y descripción de los componentes compuestos
    
    '''
    ccnames = []

    for i in range(len(mlist)):
        for j in range(len(mlist[i])):
            # Accedo al nombre de los carros
            name = (mlist[i][j]['name'])
            desc = (mlist[i][j]['description'])
            ccnames.append({'name': name, 'description': desc})

    return ccnames

def createscnames(mlist):
    '''
    Retorna la lista con diccionarios que contienen nombre, descripción y padre de los componentes simples
    '''
    
    scnames = []
    for i in range(len(mlist)):
        for j in range(len(mlist[i])):
            #Accedo a la información de cada carro
            desc =mlist[i][j]['description']
            for comp in (mlist[i][j]['composite_component']):
                comp['parent'] = desc
                comp['source'] = f'arq{i}'
                scnames.append(comp)

    return scnames

def ismandatory(mlist, auxlist, item):
    '''
    Define si un componente es obligatorio o no
    Recibe: Lista de arquitecturas
            Lista auxiliar con X de un componente
            Item que se desea conocer su obligatoreidad
    Retorna True si el componente es obligatorio y false si no
    '''
    if auxlist.count(item) >= len(mlist):
        return True
    else:
        return False

def handleccdesc(mlist):
    '''
    Genera lista de diccionarios que contienen los nombres de componentes compuestos, su descripción, si son obligatorios y su valor lógico
    '''
    mainlist = []
    descriptions = []
    ccnames = createccnames(mlist)


    for name in ccnames:
        descriptions.append(name['description'])

    auxdescriptions = list(set(descriptions))


    for description in auxdescriptions:
        mandatory = ismandatory(mlist, descriptions, description)
        components = []
        for comp in ccnames:
            
            if description == comp['description']:
                if comp['description'] in components:
                    pass
                else:
                    components.append(comp['description'])
                    quant = descriptions.count(comp['description'])

        auxdic = {
            "description": description,
            # "components": components,
            "mandatory": mandatory,
            "quantity": quant
        }
        mainlist.append(auxdic)

        logical = ''

        if len(mlist) == 1:
                logical = 'and'

        cont = 0
        for d in mainlist:
            if d['quantity'] == len(mlist):
                cont +=1

        if cont == len(mainlist):
            logical = 'and'

        if logical == '':
            xor = True
            for d in mainlist:
                if d['quantity']!=1:
                    xor = False
        
            if xor:
                logical = 'xor'
            else:
                logical = 'or'

        for e in mainlist:
            e['logical'] = logical

    return mainlist

def handlesclogical(sclist, mlist):
    '''
    Agrega el valor lógico para las conexiones aspecto - funcionalidad
    '''
    parentlist = []
    parentson = []
    sons = []


    for s in sclist:
        
        parentlist.append(s['parent'])

    for s in sclist:
        sons.append(s['description'])

    #Eliminamos padres repetidos
    parentlist = list(set(parentlist))

    for p in parentlist:
        sonlist = []
        for s in sclist:
            if s['parent'] == p:
                for i in range(s['son_count']):
                    aux = {'description': s['description'], 'source': s['source']}
                    if aux in sonlist:
                        pass
                    else:
                        sonlist.append(aux)
                

        dic = {
            'parent': p,
            'son_list': sonlist,
        }
        parentson.append(dic)


    # Recorremos lista de padre-hijo
    for p in parentson:
        #Contador de cantidad de veces que está presente un aspecto en las arquitecturas
        cont=0
        for arq in mlist:
            for asp in arq:
                if asp['description'] ==p['parent']:
                    cont+=1
        #Si todos los hijos de p, son de una arquitectura distinta, entonces, la lógica para ellos debe ser xor
        #Si todos los hijos están en las dos arquitecturas, la lógica es and

        source_list =[]
        auxson = []
        for s in p['son_list']:
            source_list.append(s['source'])
            if s['description'] in auxson:
                pass
            else:
                auxson.append(s['description'])
        
        

        for son in p['son_list']:

            #Creamos lista para hijos sin repetir
            auxlist = []
            for x in p['son_list']:
                if x['description'] in auxlist:
                    pass
                else:
                    auxlist.append(x['description'])
            #si la lista tiene un solo hijo, es and
            if len(auxlist) ==1:
                for sc in sclist:
                    if sc['description'] == son['description']:
                        sc['logical'] = 'and'


            #cada hijo tiene un source, y si sale de 2 sources, es que está repetido.
            #si la cantidad de sources es igual a la cantidad de hijos * la cantidad arquitecturas, es and
           
            elif len(source_list) == (len(auxson)*cont):
                for sc in sclist:
                    if sc['description'] == son['description']:
                        sc['logical'] = 'and'

            #Si todos los hijos son del mismo source, es and
            elif len(list(set(source_list))) ==1:
                for sc in sclist:
                    if sc['description'] == son['description']:
                        sc['logical'] = 'and'


            #Si la cantidad de hijos es igual a la cantidad de sources sin repetir, entonces es xor
            elif len(p['son_list']) == len(list(set(source_list))):
                for sc in sclist:
                    if sc['description'] == son['description']:
                        sc['logical'] = 'xor'

            
            
            #Si no es and, ni xor, es or
            else:
                for sc in sclist:
                    if sc['description'] == son['description']:
                        sc['logical'] = 'or'
            
                  
def handlescdesc(mlist):
    '''
    Genera lista de diccionarios con los nombres de los componentes simples, su padre, su descripción y si son únicos
    '''

    scnames = createscnames(mlist)

    #creo lista de diccionarios con todas las descripciones y la arquitectura de la que provienen, evitando a las descripciones repetidas de la misma arquitectura
    start_descriptions = []
    for name in scnames:
        aux = {'desc': name['description'], 'source': name['source']}
        if aux in start_descriptions:
            pass
        else:
            start_descriptions.append(aux)
    

    #Creo la lista de descripciones, que va a tener las descripciones repetidas asegurándose de que vengan de distinta arquitectura
    descriptions =[]
    for d in start_descriptions:
        descriptions.append(d['desc'])


    #Elimino descripciones repetidas
    auxdescriptions = list(set(descriptions))

    #creación de lista auxiliar de componente compuesto con sus hijos (componentes simples)
    parentson = []
    parentlist = []
    for p in scnames:
        parentlist.append(p['parent'])
    parentlist = list(set(parentlist))

    for parent in parentlist:
        sonlist = []
        for comp in scnames:
            if comp['parent'] ==parent:
                sonlist.append(comp['name'])

        dic = {
            'parent': parent,
            'son_list': sonlist
        }
        parentson.append(dic)

    


    for description in auxdescriptions:
        for comp in scnames:
            if description == comp['description']:
                for cm in parentson:
                    for c in cm['son_list']:
                        if c == comp['name']:
                            mandatory = ismandatory(mlist, descriptions, description)
                            comp['mandatory'] = mandatory
    
    components = []
    for sc in scnames:
        if sc in components:
            pass
        else:
            components.append(sc)

    handlescname(components, mlist)
    #Agrega valor lógico a la relación aspecto - funcionalidad
    handlesclogical(components, mlist)

    return components
                    
def handlescname(sclist, mainlist):

    parentlist = []
    parentson = []

    namelist = []
    for m in mainlist:
        for c in m:
            for h in c['composite_component']:
                namelist.append(h['name'])

    uniquenames = list(set(namelist))
    for sc in sclist:
        for name in uniquenames:
            if sc['name']==name:

                mandatory = ismandatory(mainlist, namelist, name)
                sc['mandatory_name'] = mandatory
                sc['son_count'] = namelist.count(name)


    for sc in sclist:
        parentlist.append(sc['description'])
    parentlist = list(set(parentlist))

    for parent in parentlist:
        sonlist = []
        for comp in sclist:
            if comp['description'] ==parent:
                sonlist.append({'name': comp['name'],'mandatory': comp['mandatory_name'], 'count': comp['son_count'], 'source': comp['source']})

        dic = {
            'parent': parent,
            'son_list': sonlist,
            'mand': 0
        }
        parentson.append(dic)



    for p in parentson:
        #Contador de cantidad de veces que está presente un aspecto en las arquitecturas
        cont=0
        for arq in mainlist:
            for asp in arq:
                if asp['description'] ==p['parent']:
                    cont+=1
        
        #Si todos los hijos de p, son de una arquitectura distinta, entonces, la lógica para ellos debe ser xor
        #Si todos los hijos están en las dos arquitecturas, la lógica es and

        source_list =[]
        auxson = []
        for s in p['son_list']:
            source_list.append(s['source'])
            if s['name'] in auxson:
                pass
            else:
                auxson.append(s['name'])

        #Crear lista de hijos sin repetir
        for son in p['son_list']:
            auxlist = []
            for s in p['son_list']:
                if s['name'] not in auxlist:
                    auxlist.append(s['name'])

            #Si la lista tiene un solo hijo, es and
            if len(auxlist) ==1:
                for sc in sclist:
                    if sc['name'] == son['name']:
                        sc['son_logical'] = 'and'

            # cada hijo tiene un source, y si sale de 2 sources, es que está repetido.
            #si la cantidad de sources es igual a la cantidad de hijos * la cantidad arquitecturas, es and
           
            elif len(source_list) == (len(auxson)*cont):
                for sc in sclist:
                    if sc['name'] == son['name']:
                        sc['son_logical'] = 'and'

            #Si todos los hijos son del mismo source, es and
            elif len(list(set(source_list))) ==1:
                for sc in sclist:
                    if sc['name'] == son['name']:
                        sc['son_logical'] = 'and'

            #Si la cantidad de hijos es igual a la cantidad de sources sin repetir, entonces es xor
            elif len(p['son_list']) == len(list(set(source_list))):
                for sc in sclist:
                    if sc['name'] == son['name']:
                        sc['son_logical'] = 'xor'
 
            #Si no es and, ni xor, es or
            else:
                for sc in sclist:
                    if sc['name'] == son['name']:
                        sc['son_logical'] = 'or'

def handlescarq(mlist, name, mandatory):
    '''
    Agrega al nodo donde se crea el componente simple, un string que indica el nombre de las arquitecturas en las que está presente
    Recibe: Lista de aquitecturas (array), nombre del componente (string) y si es obligatorio o no (bool)
    Retorna: String con arquitecturas a la que pertenece el componente
    '''

    aux = ''

    if mandatory:
        return aux
    else:
        aux+='\n('
        for arq in mlist:
            for asp in arq:
                for comp in asp['composite_component']:
                    if comp['name'] ==name:
                        if aux =='\n(':
                            aux+=asp['arq_name']
                            break
                        else:
                            aux+=f', {asp["arq_name"]}'
                            break
        aux +=')'
        return aux