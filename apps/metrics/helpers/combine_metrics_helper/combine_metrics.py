from firebase_admin import db
from rest_framework.response import Response

import random

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
  try:
    combine_metrics = CombineMetrics(url, arch_index, version_index, dms_weight, name_resemblance_weight, coupling_weight, package_mapping_weight)
    return Response(data=combine_metrics)
  except Exception as e:
    print('Error:', e)
    return Response(data=None, status=500)

def CombineMetrics(url, archIndex, versionIndex, dms_weight, name_resemblance_weight, coupling_weight, package_mapping_weight):

  arch_ref = db.reference(url + '/architectures')
  arch_arr = arch_ref.get()
  edges = arch_arr[int(archIndex)]['versions'][int(versionIndex)]['elements']['edges']


  for i, edge in enumerate(edges):
    dms_value = edge['metrics']['DMS']['value']
    name_resemblance_value = edge['metrics']['nameRessemblance']['value']
    coupling_value = edge['metrics']['coupling']['value']
    package_mapping_value = edge['metrics']['packageMapping']['value']

    sumatoria_x_w = name_resemblance_weight*name_resemblance_value + coupling_weight*coupling_value + package_mapping_weight*package_mapping_value

    sumatoria_w = name_resemblance_weight + coupling_weight + package_mapping_weight + dms_weight

    q = (sumatoria_x_w - (dms_value*dms_weight))/sumatoria_w
    _q = '%.3f' % q

    qVariable = {
      'overall_score_q': {
        'value': _q
      }
    }

    edge['metrics'].update(qVariable)

    arch_arr[int(archIndex)]['versions'][int(versionIndex)]['elements']['edges'] = edges
    project_ref = db.reference(url)
    project_ref.update({
        'architectures': arch_arr
    })
  return edges

def handleCreateCompositeComponent(data):
  uid = data['user_id']
  project_index = data['project_index']
  arch_index = int(data['arch_index'])
  version_index = data['ver_index']
  url = '/users/' + uid + '/projects/' + str(project_index)
  umbral_q = data['umbral_q']

  try:
    composite_components = CreateCompositeComponent(arch_index, version_index, url, umbral_q)
    return Response(data=composite_components)
  except Exception as e:
    print('Error:', e)
    return Response(status=500)


def CreateCompositeComponent(arch_index, version_index, url, umbral_q):
  arch_ref = db.reference(url + '/architectures')
  arch_arr = arch_ref.get()
  edges = arch_arr[int(arch_index)]['versions'][int(version_index)]['elements']['edges']
  nodes = arch_arr[int(arch_index)]['versions'][int(version_index)]['elements']['nodes']
  elements =  arch_arr[int(arch_index)]['versions'][int(version_index)]['elements']
  update_nodes = CreateListS(nodes, edges, umbral_q)
  arch_arr[int(arch_index)]['versions'][int(version_index)]['elements']['nodes'] = update_nodes
  project_ref = db.reference(url)
  list_t = CreateListT(nodes)
  elements.update({
    'list_t': list_t
  })
  arch_arr[int(arch_index)]['versions'][int(version_index)]['elements'] = elements
  project_ref.update({
      'architectures': arch_arr
  })
  return list_t


def CreateListS(nodes, edges, umbral_q):
  for node in nodes:
    list_S = []
    for edge in edges:
      source = edge['data']['source']
      q = edge['metrics']['overall_score_q']['value']
      if source == node['data']['id']:
        if float(q) >= umbral_q:
          list_S.append(edge['data']['target'])
    lista = {
      'list_s': list_S
    }
    node.update(lista)
  return nodes


def SearchNodeListS(id, nodes):
  for index, node in enumerate(nodes):
    if id == node['data']['id']:
      return index, node['list_s']

  return index, []

def SearchNode(id, nodes):
  for index, node in enumerate(nodes):
    if id == node['data']['id']:
      return node

  return []

def generateColor(colors):
  hexadecimal = "#"+''.join([random.choice('ABCDEF0123456789') for i in range(6)])
  if hexadecimal not in colors:
    colors.append(hexadecimal)
  else:
    generateColor(colors)
  return hexadecimal

def asigneColorCC(list_t, nodes):
  colors = ['#18202C']
  for item in list_t:
    color = generateColor(colors)
    for item2 in item['composite_component']:
      node = SearchNode(item2, nodes)
      node['data'].update({
        'bg': color,
        'composite': item['name']
      })


def CreateListT (nodes):
  list_T = []
  nodes_aux = []
  nodes_aux.extend(nodes)
  for index, node_aux in enumerate(nodes_aux):
    list_s = node_aux['list_s']
    if len(list_s) > 0:
      nodes_aux.pop(index)
      for item in list_s:
        index2, item_list_s = SearchNodeListS(item, nodes_aux)
        if len(item_list_s) > 0:
          nodes_aux.pop(index2)
          for item2 in item_list_s:
            if item2 not in list_s:
              list_s.append(item2)
      list_s.append(node_aux['data']['id'])
      composite_component = {
        "name": node_aux['data']['id'],
        "composite_component": list_s
      }
      list_T.append(composite_component)
  asigneColorCC(list_T, nodes)
  print('------------------FINAL----------------------')
  print(list_T)
  print(len(nodes))

  return list_T





