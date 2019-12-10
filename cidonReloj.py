# Este archivo sirve de modelo para la creacion de aplicaciones, i.e. algoritmos concretos
""" Implementa la simulacion del algoritmo de Propagacion de Informacion (Segall) como ejemplo
de aplicacion """

import sys
from event import Event
from eventTarjeta import Tarjeta
from model import Model
#from process import Process
#from simulator import Simulator
from simulation import Simulation

class CidonReloj(Model):
    """ La clase Algorithm desciende de la clase Model e implementa los metodos 
    "init()" y "receive()", que en la clase madre se definen como abstractos """
	
    def init(self):
        #self.sinVisitar = self.neighbors[:]
        """ Aqui se definen e inicializan los atributos particulares del algoritmo """
        self.padre = self.id
        self.sinVisitar =  []  
        self.visited = False
        self.etiqueta = [0]*3
        self.cont = 0
        print ("inicializo algoritmo")
        for i in range (len(self.neighbors)):       #De esta forma se pueden manipular las listas por aparte
            self.sinVisitar.append(self.neighbors[i])

    def go(self,event):
        if(len(self.sinVisitar) != 0 ):
            self.etiqueta = event.getEtiqueta()[:]
            self.cont +=1                           #Nos dice el momento en que llego
            self.etiqueta[self.id-1] = self.cont
            k = self.sinVisitar.pop(0)
            newevent = Tarjeta("DESC", self.clock+1.0, k, self.id, self.etiqueta)
            print (" Soy el nodo ", self.id, " y mando DESC a mi vecino ", k, " en el tiempo de ", self.clock, "con la etiqueta: ", self.etiqueta)
            self.transmit(newevent)
        elif(self.padre != self.id):
            self.etiqueta = event.getEtiqueta()[:]
            self.cont +=1                           #Nos dice el momento en que llego
            self.etiqueta[self.id-1] = self.cont
            newevent = Tarjeta("REG", self.clock+1.0, self.padre, self.id, self.etiqueta)
            print (" Soy el nodo ", self.id, " y mando REG a mi padre ", self.padre, " en el tiempo de ", self.clock, "con la etiqueta: ", self.etiqueta)
            self.transmit(newevent)

    def receive(self, event):
        if(event.getName() == "DESC"):  #Al momento de ser despertado manda un mensaje descubre
            self.etiqueta = event.getEtiqueta()[:]
            self.cont +=1                           #Nos dice el momento en que llego
            self.etiqueta[self.id-1] = self.cont 
            print (" Soy el nodo ", self.id, " y recibi descubre de ", event.getSource(), " en el tiempo ", event.getTime(), "con la etiqueta: ", self.etiqueta)
            self.cont +=1                           #Nos dice el momento en que llego
            self.etiqueta[self.id-1] = self.cont 
            for t in self.neighbors: 
                newevent = Tarjeta("AVISO", self.clock+1.0, t, self.id, self.etiqueta)
                print (" Soy el nodo ", self.id, " y mando aviso a todos mis vecinos ", t, " en el tiempo ", newevent.getTime(), "con la etiqueta: ", self.etiqueta)
                self.transmit(newevent)
        
            if(event.getSource() in self.sinVisitar):       #Quitamos al nodo que manda el mensaje
                self.sinVisitar.remove(event.getSource())
            
            #print ("Mis vecinos son ", self.sinVisitar, "Fuente = ", event.getSource())
            self.visited = True
            self.padre = event.getSource()
            self.go(event)
                
        elif(event.getName() == "REG"):  
            self.etiqueta = event.getEtiqueta()[:]
            self.cont +=1                           #Nos dice el momento en que llego
            self.etiqueta[self.id-1] = self.cont        
            print (" Soy el nodo ", self.id, " y recibi REGRESO de mi vecino ", event.getSource(), " en el tiempo ", event.getTime(), "con la etiqueta: ", self.etiqueta)
            self.go(event)

        else:                                   #Solo entra cuando el mensaje es AVISO para eliminar la fuente
            self.etiqueta = event.getEtiqueta()[:]
            self.cont += 1
            self.etiqueta[self.id-1] = self.cont
            print (" Soy el nodo ", self.id, " y recibi aviso de mi vecino ", event.getSource(), " en el tiempo ", event.getTime(), "con la etiqueta: ", self.etiqueta)
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
    m = CidonReloj()
    experiment.setModel(m, i)
etiqueta = [0]*3

# inserta un evento semilla en la agenda y arranca
seed = Tarjeta("DESC", 0.0, 1, 1, etiqueta)
experiment.init(seed)
experiment.run()
