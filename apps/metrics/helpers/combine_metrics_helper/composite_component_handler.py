from firebase_admin import db
from rest_framework.response import Response


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
      for t in list_t:
        if t['name'] == composite_component:
          t['composite_component'].append(nodeData)
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

# TODO
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

  try:
      for item in list_t:
        for edge in edges:
          # Dependencias salientes
          ce = calculate_ce(edge, edges, nodes)
          # Dependencias entrantes
          ca = 0


      print(0)
  except print(0):
      pass



def calculate_ce(edge, edges, nodes):
   ce = []

   nodeSource =  edge['data']['source']
   nodeTarget =  edge['data']['target']




# TODO
# ? Hace falta limpiar las tablas
# Edita la descripción de los componentes compuestos
def handleEditCompositeComponentDescription(data):
  uid = data['user_id']
  project_index = data['project_index']
  arch_index = int(data['arch_index'])
  version_index = data['ver_index']
  url = '/users/' + uid + '/projects/' + str(project_index)
  try:
      print(0)
  except print(0):
      pass
