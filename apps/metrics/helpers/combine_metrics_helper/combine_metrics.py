from firebase_admin import db
from rest_framework.response import Response

def handleCombineMetrics(data):
  """ Calcula la combinación de la métricas y actualiza los parámetros de las aristas con su respectiva Q

  Parameter
  ---------
  edges: list
    lista con todos las aristas de la arquitectura
  """

  uid = data['user_id']
  project_index = data['project_index']
  arch_index = int(data['arch_index'])
  version_index = data['ver_index']
  url = '/users/' + uid + '/projects/' + str(project_index)
  dms_weight= data['weighing']['dms']
  name_resemblance_weight = data['weighing']['name_resemblance']
  coupling_weight = data['weighing']['coupling']
  package_mapping_weight = data['weighing']['package_mapping']
  print('/////////////////////////////')
  print('/////////////////////////////')
  print('/////////////////////////////')
  try:
    combine_metrics = CombineMetrics(url, arch_index, version_index, dms_weight, name_resemblance_weight, coupling_weight, package_mapping_weight)
    return Response(data=combine_metrics)
  except:
    return Response(data=None, status=500)

def CombineMetrics(url, archIndex, versionIndex, dms_weight, name_resemblance_weight, coupling_weight, package_mapping_weight):

  arch_ref = db.reference(url + '/architectures')
  arch_arr = arch_ref.get()
  edges = arch_arr[int(archIndex)]['versions'][int(versionIndex)]['elements']['edges']

  print('/////////////////////////////')
  print('/////////////////////////////')
  print('/////////////////////////////')

  for edge in edges:
    print('/////////////////////////////')
    print('/////////////////////////////')
    print('/////////////////////////////')
    print('/////////////////////////////')
    print('/////////////////////////////')
    print(edge)
