# Este archivo sirve de modelo para la creacion de aplicaciones, i.e. algoritmos concretos
""" Implementa la simulacion del algoritmo de Propagacion de Informacion (Segall) como ejemplo
de aplicacion """

import sys
from mensajeprof import Mensaje
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
        self.prof = None
        self.banderaMensaje = False
        for i in range(len(self.neighbors)):       
            self.recibi.append(False)                           #La casilla de su vecino la inicializo en False   
        print ("inicializo algoritmo")

    def receive(self, event):
        if self.prof == 0:
            self.banderaMensaje = True
            print ("Soy el nodo",self.id,"y recibi un",event.name,"del nodo", event.source, "PROFUNDIDAD ",self.prof , "a las",event.time)
            evento = Mensaje("Mensaje", self.clock+1.0, event.source, self.id,None)
            self.transmit(evento)
        else:
            for t in range(len(self.neighbors)):                #Para poner en verdadero su estado
                if event.getSource() == self.neighbors[t]:
                    self.recibi[t] = True
            if self.visited == False:
                self.visited = True
                self.padre = event.source
                self.prof = event.profundidad
                if self.prof > 0:
                    for t in self.neighbors:
                        if t != self.padre:
                            evento = Mensaje("Mensaje", self.clock+1.0, t, self.id,self.prof-1)
                            self.transmit(evento)
                else:
                    for t in range(len(self.neighbors)):                #Para poner en verdadero su estado
                        if event.getSource() == self.neighbors[t]:
                            self.recibi[t] = False
            

            print ("Soy el nodo ",self.id,"y recibi un",event.name, "del nodo", event.source, " con profundidad ", self.prof,"a las",event.time)
            
            if self.id != self.padre and self.banderaMensaje == False:
                self.banderaMensaje = True
                evento = Mensaje("MENSAJE REGRESO", self.clock+1.0, self.padre, self.id,None)
                self.transmit(evento)
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
print("Hola, dame el valor de la profundida que deseas")
profundi = int(input())
seed = Mensaje("Mensaje", 0.0, 1, 1, profundi)
experiment.init(seed)
experiment.run()