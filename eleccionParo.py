# Este archivo sirve de modelo para la creacion de aplicaciones, i.e. algoritmos concretos
""" Implementa la simulacion del algoritmo de Propagacion de Informacion (Segall) como ejemplo
de aplicacion """

import sys
from event import Event
from eventEleccion import Eleccion
from model import Model
#from process import Process
#from simulator import Simulator
from simulation import Simulation

class eleccionParo(Model):
    """ La clase Algorithm desciende de la clase Model e implementa los metodos 
    "init()" y "receive()", que en la clase madre se definen como abstractos """
	
    def init(self):
        """ Aqui se definen e inicializan los atributos particulares del algoritmo """
        self.visited = False
        self.lider = None
        self.sinVisitar = self.neighbors[:]
        print ("inicializo algoritmo")

    def receive(self, event):
        if event.getName() == "DESPIERTA":
            if(event.getElecto() < self.id):
                for i in range(len(self.neighbors)):
                    newevent = Eleccion("DESPIERTA", self.clock+1.0, i, self.id, self.id)
                    print (" Soy el nodo ", self.id, " y mando que soy el lider a mi vecino: ", self.neighbors[i], " en el tiempo ", self.time)
                    self.transmit(newevent)
            else:
                self.lider = event.getElecto()
                print("Soy el lider ", self.id)
                
# ----------------------------------------------------------------------------------------
# "main()"
# ----------------------------------------------------------------------------------------

# construye una instancia de la clase Simulation recibiendo como parametros el nombre del 
# archivo que codifica la lista de adyacencias de la grafica y el tiempo max. de simulacion
if len(sys.argv) != 2:
    print ("Please supply a file name")
    raise SystemExit(1)
experiment = Simulation(sys.argv[1], 100)  

# asocia un pareja proceso/modelo con cada nodo de la grafica
for i in range(1,len(experiment.graph)+1):
    m = eleccionParo()
    experiment.setModel(m, i)

# inserta un evento semilla en la agenda y arranca
seed = Eleccion("DESPIERTA", 0.0, 1, 1, 0)
experiment.init(seed)
experiment.run()