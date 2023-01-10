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

  try:
    for t in list_t:
      if t['name'] == old_name:
        t['name'].update({
        'name': str(new_name).upper()
        })
        break

  # Se actualiza la lista t
    arch_arr[int(arch_index)]['versions'][int(version_index)]['elements']['list_t'] = list_t

  # Se actualiza la bd
    arch_arr[int(arch_index)]['versions'][int(version_index)]['elements'] = elements
    project_ref.update({
      'architectures': arch_arr
  })
    # return Response(data=None)
  except Exception as e:
    print('Error:', e)
    # return Response(data=None, status=500)


def handleEditNodeCompositeComponent(data):
  uid = data['user_id']
  project_index = data['project_index']
  arch_index = int(data['arch_index'])
  version_index = data['ver_index']
  url = '/users/' + uid + '/projects/' + str(project_index)

  node = data['node']
  composite_component =  data['composite_component']

  arch_ref = db.reference(url + '/architectures')
  arch_arr = arch_ref.get()

  list_t = arch_arr[int(arch_index)]['versions'][int(version_index)]['elements']['list_t']

  try:
      for t in list_t:
        if t['name'] == composite_component:
          t['composite_component'].push(node)


      arch_arr[int(arch_index)]['versions'][int(version_index)]['elements']['list_t'] = list_t


      arch_arr[int(arch_index)]['versions'][int(version_index)]['elements'] = elements
      project_ref.update({
      'architectures': arch_arr
        })

  except Exception as e:
      print(e)
