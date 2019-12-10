# Alumno: Jorge Eduardo Valenca Loyola, Matricula:2153012841
""" Implementa la simulacion del algoritmo de Propagacion de informacion con retro
    (PIF) de Segall y con profundidad limitada"""

import sys
from message import Message
from model import Model
from simulation import Simulation

class AlgorithmPIFL(Model):
    """ La clase AlgorithmPIFL desciende de la clase Model e implementa los metodos 
    "init()" y "receive()", que en la clase madre se definen como abstractos """
	
    def init(self):
        """ Aqui se definen e inicializan los atributos particulares del algoritmo """
        self.visitado = False
        self.padre = self.id
        self.recibi = self.neighbors[:]
        self.profundidad = None

    def receive(self, event):
        """ Aqui se definen las acciones concretas que deben ejecutarse cuando se
        recibe un evento """
        if self.profundidad == 0:
            print "NIVEL -",self.profundidad,": Soy el nodo",self.id,"y recibi un",event.name, "a las",event.time,"del nodo", event.source
            evento = Message("M", self.clock+1.0, event.source, self.id,None)
            self.transmit(evento)
        else:
            for i,x in enumerate(self.recibi):
                if x == event.source:
                    self.recibi[i]=True
            if self.visitado == False:
                self.visitado = True
                self.padre = event.source
                self.profundidad = event.profundidad
                if self.profundidad > 0:
                    for t in self.neighbors:
                        if t != self.padre:
                            evento = Message("M", self.clock+1.0, t, self.id,self.profundidad-1)
                            self.transmit(evento)
                else:
                    for i,x in enumerate(self.recibi):
                        if type(x) is int:
                            self.recibi[i]=False
            print "NIVEL -",self.profundidad,": Soy el nodo",self.id,"y recibi un",event.name, "a las",event.time,"del nodo", event.source
            for t in self.recibi:
                if type(t) is int:
                    return
            if self.id != self.padre:
                evento = Message("MR", self.clock+1.0, self.padre, self.id,None)
                self.transmit(evento)

# ----------------------------------------------------------------------------------------
# "main()"
# ----------------------------------------------------------------------------------------

# construye una instancia de la clase Simulation recibiendo como parametros el nombre del 
# archivo que codifica la lista de adyacencias de la grafica y el tiempo max. de simulacion
if len(sys.argv) != 2:
    print "Por favor escriba el nombre del archivo del grafo donde desea correr el algoritmo"
    raise SystemExit(1)
experiment = Simulation(sys.argv[1], 50)

# asocia un pareja proceso/modelo con cada nodo de la grafica
for i in range(1,len(experiment.graph)+1):
    m = AlgorithmPIFL()
    experiment.setModel(m, i)

# inserta un evento semilla en la agenda y arranca
seed = Message("M", 0.0, 2,2,4)
experiment.init(seed)
experiment.run()