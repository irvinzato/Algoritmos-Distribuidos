# Este archivo sirve de modelo para la creacion de aplicaciones, i.e. algoritmos concretos
""" Implementa la simulacion del algoritmo de Propagacion de Informacion (Segall) como ejemplo
de aplicacion """

import sys
from event import Event
from model import Model
#from process import Process
#from simulator import Simulator
from simulation import Simulation

class DFSChange(Model):
    """ La clase Algorithm desciende de la clase Model e implementa los metodos 
    "init()" y "receive()", que en la clase madre se definen como abstractos """
	
    def init(self):
        """ Aqui se definen e inicializan los atributos particulares del algoritmo """
        self.padre = self.id
        self.sinVisitar =  self.neighbors
        self.visited = False
        print ("inicializo algoritmo")

    def go(self):
        if(len(self.sinVisitar) != 0 ):
                k = self.sinVisitar.pop(0)
                newevent = Event("DESC", self.clock+1.0, k, self.id)
                print (" Soy el nodo ", self.id, " y mando DESC a mi vecino ", k, " en el tiempo de ", self.clock)
                self.transmit(newevent)
        elif(self.padre != self.id):
            newevent = Event("REG", self.clock+1.0, self.padre, self.id)
            print (" Soy el nodo ", self.id, " y mando REG a mi padre ", self.padre, " en el tiempo de ", self.clock)
            self.transmit(newevent)

    def receive(self, event):
        #print (event.getName(), "Padre = ", self.padre, "Fuente = ", event.getSource())
        if(event.getName() == "DESC"):
            if(event.getSource() in self.sinVisitar):
                self.sinVisitar.remove(event.getSource())
            if(self.visited):
                newevent = Event("RECHAZO", self.clock+1.0, event.getSource(), self.id)
                print (" Soy el nodo ", self.id, " y mando RECHAZO a ", event.getSource(), " en el tiempo de ", self.clock)
                self.transmit(newevent)
            else:
                self.visited = True
                self.padre = event.getSource()
                self.go()     
        else:
            self.go()
                


        """
        Aqui se definen las acciones concretas que deben ejecutarse cuando se
        recibe un evento
        if self.visited == False:
            print ("soy ", self.id, " recibo mensaje a las ", self.clock, " desde ", event.getSource())
            self.visited = True
            for t in self.neighbors: 
                newevent = Event("C", self.clock+1.0, t, self.id)
                print (" proximo evento a las ", newevent.getTime())
                self.transmit(newevent)
        """
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
    m = DFSChange()
    experiment.setModel(m, i)

# inserta un evento semilla en la agenda y arranca
seed = Event("DESC", 0.0, 1, 1)
experiment.init(seed)
experiment.run()
