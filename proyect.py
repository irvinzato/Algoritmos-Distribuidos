# Este archivo sirve de modelo para la creacion de aplicaciones, i.e. algoritmos concretos
""" Implementa la simulacion del algoritmo de Propagacion de Informacion (Segall) como ejemplo
de aplicacion """

import sys
import random
from event import Event
from model import Model
#from process import Process
#from simulator import Simulator
from simulation import Simulation

class DFSCidol(Model):
    """ La clase Algorithm desciende de la clase Model e implementa los metodos 
    "init()" y "receive()", que en la clase madre se definen como abstractos """
	
    def init(self):
        """ Aqui se definen e inicializan los atributos particulares del algoritmo """
        self.padre = self.id
        self.sinVisitar =  []  
        self.visited = False
        self.guardado = []
        self.banderaAleatorio = True
        print ("inicializo algoritmo")
        for i in range (len(self.neighbors)):       #De esta forma se pueden manipular las listas por aparte
            self.sinVisitar.append(self.neighbors[i])

    def go(self):
        if(len(self.sinVisitar) != 0 ):
          
            aleatorio = random.randint(0, len(self.sinVisitar))    #selecciona un numero aleatorio
            print("El vecino aleatorio es ", self.sinVisitar[aleatorio])
            
            for i in range(len(self.guardado)):
                if(aleatorio == self.guardado[i]):
                    break
                else:
                    self.guardado.append(aleatorio)
            
            #primero = self.sinVisitar.pop(0)
            newevent = Event("DESC", self.clock+1.0, self.sinVisitar[aleatorio], self.id)
            print (" Soy el nodo ", self.id, " y mando DESC a mi vecino ", self.sinVisitar[aleatorio], " en el tiempo de ", self.clock)
            self.transmit(newevent)
        elif(self.padre != self.id):
            newevent = Event("REG", self.clock+1.0, self.padre, self.id)
            print (" Soy el nodo ", self.id, " y mando REG a mi padre ", self.padre, " en el tiempo de ", self.clock)
            self.transmit(newevent)

    def receive(self, event):
        if(event.getName() == "DESC"):  #Al momento de ser despertado manda un mensaje descubre
            for t in self.neighbors: 
                newevent = Event("AVISO", self.clock+1.0, t, self.id)
                print (" Soy el nodo ", self.id, " y mando aviso a todos mis vecinos ", t, " en el tiempo ", newevent.getTime())
                self.transmit(newevent)
        
            if(event.getSource() in self.sinVisitar):       #Quitamos al nodo que manda el mensaje
                self.sinVisitar.remove(event.getSource())
            
            #print ("Mis vecinos son ", self.sinVisitar, "Fuente = ", event.getSource())
            self.visited = True
            self.padre = event.getSource()
            self.go()
                
        elif(event.getName() == "REG"):         
            self.go()
        else:                                   #Solo entra cuando el mensaje es AVISO para eliminar la fuente
            if(event.getSource() in self.sinVisitar):
                self.sinVisitar.remove(event.getSource())

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
    m = DFSCidol()
    experiment.setModel(m, i)

# inserta un evento semilla en la agenda y arranca
seed = Event("DESC", 0.0, 1, 1)
experiment.init(seed)
#seed2 = Event("DESC", 0.0, 2,2)
#experiment.init(seed2)
experiment.run()