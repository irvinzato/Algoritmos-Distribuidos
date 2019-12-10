# Este archivo sirve de modelo para la creacion de aplicaciones, i.e. algoritmos concretos
""" Implementa la simulacion del algoritmo de Propagacion de Informacion (Segall) como ejemplo
de aplicacion """

import sys
from event import Event
from model import Model
from simulation import Simulation

class PIF(Model):
    """ La clase Algorithm desciende de la clase Model e implementa los metodos 
    "init()" y "receive()", que en la clase madre se definen como abstractos """
	
    def init(self):
        """ Aqui se definen e inicializan los atributos particulares del algoritmo """
        self.padre = self.id
        self.visited = False
        self.sinVisitar = self.neighbors[:]
        self.recibi =  []
        for i in range(len(self.neighbors)):       
            self.recibi.append(False)                           #La casilla de su vecino la inicializo en False   
        
        print ("inicializo algoritmo")

    def receive(self, event):
        if event.getName() == "Mensaje":
            for t in range(len(self.neighbors)):                #Para poner en verdadero su estado
                if event.getSource() == self.neighbors[t]:
                    self.recibi[t] = True
            if self.visited == False:
                self.visited = True
                self.padre = event.getSource()
                if (event.getSource() in self.sinVisitar):              #Si la fuente esta en sinVisitar se quita de allo
                    self.sinVisitar.remove(event.getSource())
                for i in self.sinVisitar:                               #Manda mensaje a todos sus vecinos menos a su padre
                    newevent = Event("Mensaje", self.clock+1.0, i, self.id)
                    print (" Soy el nodo ", self.id, " y mando MENSAJE a mi vecino: ", i, " en el tiempo ", newevent.getTime())
                    self.transmit(newevent)
            alerta=True
            for r in range(len(self.neighbors)):                #Reviso si todos los vecinos ya tienen verdadero en su estado de recibi
                if self.recibi[r] == False:
                    alerta = False
            if alerta == True:                              #Si ya es verdadera toda su lista de vecinos y el padre es diferente del que soy mando mensaje
                if self.padre != self.id:
                    newevent = Event("Mensaje", self.clock+1.0, self.padre, self.id)
                    print (" Soy el nodo ", self.id, " y mando MENSAJE a mi padre ", self.padre, " en el tiempo ", newevent.getTime())
                    self.transmit(newevent)
                        
                        

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
    m = PIF()
    experiment.setModel(m, i)

# inserta un evento semilla en la agenda y arranca
seed = Event("Mensaje", 0.0, 1, 1)
experiment.init(seed)
experiment.run()