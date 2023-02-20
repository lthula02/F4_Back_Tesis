from firebase_admin import db
from rest_framework.response import Response
from apps.metrics.helpers.combine_metrics_helper.combine_metrics import SearchNode

def handleEditName(data):
  uid = data['user_id']
  project_index = data['project_index']
  arch_index = int(data['arch_index'])
  version_index = data['ver_index']
  url = '/users/' + uid + '/projects/' + str(project_index)

  old_name = data['old_name']
  new_name = data['new_name']

  arch_ref = db.reference(url + '/architectures')
  arch_arr = arch_ref.get()

  list_t = arch_arr[int(arch_index)]['versions'][int(version_index)]['elements']['list_t']
  nodes = arch_arr[int(arch_index)]['versions'][int(version_index)]['elements']['nodes']
  try:
    for t in list_t:
      if t['name'] == old_name:
        t.update({
        'name': str(new_name).upper()
        })
        for node in nodes:
          if(node['data']['id'] in t['composite_component']):
            print(node['data']['id'])
            node['data'].update({
              'composite': str(new_name).upper()
            })
        break


  # Se actualiza la lista t
    arch_arr[int(arch_index)]['versions'][int(version_index)]['elements']['list_t'] = list_t
    arch_arr[int(arch_index)]['versions'][int(version_index)]['elements']['nodes'] = nodes
  # Se actualiza la bd
    # arch_arr[int(arch_index)]['versions'][int(version_index)]['elements'] = elements
    project_ref = db.reference(url)
    project_ref.update({
      'architectures': arch_arr
  })

    return Response(data={"ok": True})
  except Exception as e:
    print('Error:', e)
    return Response({"ok":False})


# Permite editar el componente compuesto al que pertenece un nodo
def handleEditNodeCompositeComponent(data):
  uid = data['user_id']
  project_index = data['project_index']
  arch_index = int(data['arch_index'])
  version_index = data['ver_index']
  url = '/users/' + uid + '/projects/' + str(project_index)

  nodeData = data['node']
  composite_component =  data['new_name']

  arch_ref = db.reference(url + '/architectures')
  arch_arr = arch_ref.get()

  list_t = arch_arr[int(arch_index)]['versions'][int(version_index)]['elements']['list_t']
  nodes = arch_arr[int(arch_index)]['versions'][int(version_index)]['elements']['nodes']

  try:
      fullNode = SearchNode(nodeData, nodes) # me quede sin nombres jeje

      aux = False
      for t in list_t:
        # Si el nodo pertenece con anterioridad a otro componente compuesto entonces lo saco de esa lista t
        if 'composite' in fullNode['data'] and not aux:
           print('pertenecia a otro componente')
           for lt in list_t:
              for index, cc in enumerate(lt['composite_component']):
                if cc == fullNode['data']['name']:
                  print('antes 1')
                  print(lt['composite_component'])
                  print(lt['name'])
                  print('se deberia quitar el componente')
                  lt['composite_component'].pop(index)
                  aux = True
                  print('despues 1')
                  print(lt['composite_component'])
                  break
              if aux:
                 print('BREAK')
                 break

        if t['name'] == composite_component:
          print('antes 1')
          print(t['composite_component'])
          print(t['name'])
          t['composite_component'].append(nodeData)
          print('antes 2')
          print(t['composite_component'])
          for node in nodes :
            if(node['data']['id'] == nodeData):
              # if('composite' in node):
              node['data'].update({
                'composite': t['name'],
                'bg': t['bg']
              })
              # else:
              #   node['data'].append({
              #     'composite': t['name']
              #   })
      arch_arr[int(arch_index)]['versions'][int(version_index)]['elements']['list_t'] = list_t
      arch_arr[int(arch_index)]['versions'][int(version_index)]['elements']['nodes'] = nodes


      project_ref = db.reference(url)
      project_ref.update({
      'architectures': arch_arr
        })
      return Response(data={'ok': True})
  except Exception as e:
      print(e)
      return Response(data={'ok': False})

# Genera la tabla de los componentes compuestos
def handleCompositeComponentBoard(data):
  uid = data['user_id']
  project_index = data['project_index']
  arch_index = int(data['arch_index'])
  version_index = data['ver_index']
  url = '/users/' + uid + '/projects/' + str(project_index)

  arch_ref = db.reference(url + '/architectures')
  arch_arr = arch_ref.get()

  edges = arch_arr[int(arch_index)]['versions'][int(version_index)]['elements']['edges']
  nodes = arch_arr[int(arch_index)]['versions'][int(version_index)]['elements']['nodes']
  list_t = arch_arr[int(arch_index)]['versions'][int(version_index)]['elements']['list_t']

  print(len(edges))
  print(len(nodes))
  print(len(list_t))
  try:
      for item in list_t:
        # Required interfaces
        ca = []
        # Provided interfaces
        ce = []

        for component in item['composite_component']:
          for edge in edges:
            sourceNode = SearchNode(edge['data']['source'], nodes)
            targetNode = SearchNode(edge['data']['target'], nodes)

            if component == sourceNode['data']['id']:
               if 'composite' not in targetNode['data']:
                  composite = ''
               else:
                  composite = targetNode['data']['composite']
               if sourceNode['data']['composite'] != composite:
                  if edge['scratch']['index'] not in ce and edge['scratch']['index'] not in ca:
                    ce.append(edge['scratch']['index'])


            if component == targetNode['data']['id']:
               if 'composite' not in sourceNode['data']:
                  composite = ''
               else:
                  composite = sourceNode['data']['composite']

               if targetNode['data']['composite'] != composite:
                  if edge['scratch']['index'] not in ca and edge['scratch']['index'] not in ce:
                    ca.append(edge['scratch']['index'])

        print('--------NEXT---------')
        item.update({
            'required_interfaces': ca,
            'provided_interfaces': ce,
            'description': ''
        })

      # Actualizo la lista t
      arch_arr[int(arch_index)]['versions'][int(version_index)]['elements']['list_t'] = list_t
      project_ref = db.reference(url)
      # Actualizo los datos en la base de datos
      project_ref.update({
      'architectures': arch_arr
        })

      return Response(data={'ok': True})
  except Exception as e:
      print(e)
      return Response(data={'ok': False})

# TODO
# ? Hace falta limpiar las tablas
# Edita la descripción de los componentes compuestos
def handleEditCompositeComponentDescription(data):
  uid = data['user_id']
  project_index = data['project_index']
  arch_index = int(data['arch_index'])
  version_index = data['ver_index']
  url = '/users/' + uid + '/projects/' + str(project_index)

  cc_name = data['name']
  description = data['description']

  arch_ref = db.reference(url + '/architectures')
  arch_arr = arch_ref.get()

  list_t = arch_arr[int(arch_index)]['versions'][int(version_index)]['elements']['list_t']

  try:
      for item in list_t:
        if item['name'] == cc_name:
           item.update({
              'description': description
           })
      arch_arr[int(arch_index)]['versions'][int(version_index)]['elements']['list_t'] = list_t
      project_ref = db.reference(url)
      # Actualizo los datos en la base de datos
      project_ref.update({
      'architectures': arch_arr
        })
      return Response(data={'ok': True})
  except Exception as e:
      print(e)
      return Response(data={'ok': False})
