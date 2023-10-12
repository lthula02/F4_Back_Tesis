from fuzzywuzzy import fuzz

def claculate_nameResemblance(edges, name_ressemblance_umbral):
    for edge in edges:
        word1 = edge['data']['source']
        word2 = edge['data']['target']
        ratio = fuzz.ratio(word1, word2)
        value = 0

        if word1 in word2 or word2 in word1:
            value = 1
        elif ratio > int(name_ressemblance_umbral):
            value = 1
            
        ratio = str(ratio) + "%"

        nameRessemblance = name_ressemblance_serializer(value, ratio, name_ressemblance_umbral)

        edge['metrics'].update(nameRessemblance)



def name_ressemblance_serializer(value, ratio, name_ressemblance_umbral):
    return {
            'nameRessemblance': {
                'value': value,
                'ratio': ratio,
                'umbral': name_ressemblance_umbral,
            }
        }   