from django.db import models

# Create your models here.


class AllMetrics(object):

    def __init__(self):
        self.coupling = Metric('Coupling', None, 'nij', 'ni')


#solo para metricas con 2 variables
class Metric(object): #acoplamiento, abtsraccion

    def __init__(self, name, umbral, nameVariable1, nameVariable2):
        self.name = name
        self.umbral = umbral
        self.var1 = Variable(nameVariable1)
        self.var2 = Variable(nameVariable2)
        self.result = None


class Variable(object):

    def __init__(self, name):
        self.name = name
        self.value = None
 


