# Este archivo sirve de modelo para la creacion de aplicaciones, i.e. algoritmos concretos
""" Implementa la simulacion del algoritmo de Propagacion de Informacion (Segall) como ejemplo
de aplicacion """

import sys
from event import Event
from model import Model
#from process import Process
#from simulator import Simulator
from simulation import Simulation

class PIF(Model):
    """ La clase Algorithm desciende de la clase Model e implementa los metodos 
    "init()" y "receive()", que en la clase madre se definen como abstractos """
	
    def init(self):
        """ Aqui se definen e inicializan los atributos particulares del algoritmo """
        self.padre = self.id
        self.visited = False
        self.sinVisitar = self.neighbors[:]
        self.pesoNodo = None
        self.recibi =  []
        for i in range(len(self.neighbors)):       
            self.recibi.append(False)                           #La casilla de su vecino la inicializo en False   
    
        self.iniciarPesos()
        self.valorMinimo = self.pesoNodo
        self.camino = self.id
        print ("inicializo algoritmo")

    def iniciarPesos(self):                                     #Poner pesos a cada nodo
        self.pesoNodo = input(f"Dame el peso para el nodo --> {self.id}    ")
    
    def receive(self, event):
        #print(f"Soy el nodo {self.id} y mi peso es de {self.pesoNodo}")
        if event.getName() == "INICIO":
            for t in range(len(self.neighbors)):                #Para poner en verdadero el estado del nodo
                if event.getSource() == self.neighbors[t]:
                    self.recibi[t] = True
            if self.visited == False:
                self.visited = True
                self.padre = event.getSource()                          #De quien recibe el mensaje es la fuente
                if (event.getSource() in self.sinVisitar):              #Si la fuente esta en sinVisitar se quita
                    self.sinVisitar.remove(event.getSource())
                for i in self.sinVisitar:                               #Manda INICIO a todos sus vecinos menos a su padre
                    newevent = Event("INICIO", self.clock+1.0, i, self.id, self.pesoNodo)
                    print (" Soy el nodo ", self.id," tengo un peso de ", self.pesoNodo , "mi padre es: ", self.padre ," y mando INICIO a mi vecino: ", i, " en el tiempo ", newevent.getTime())
                    self.transmit(newevent)
            alerta=True                                         #Para saber si ya son verdaderos sus estados
            for r in range(len(self.neighbors)):                #Reviso si todos los vecinos ya tienen verdadero en su estado de recibi
                if self.recibi[r] == False:
                    alerta = False
            if alerta == True:                              #Si ya es verdadera toda su lista de vecinos y el padre es diferente del que soy mando INICIO
                if self.padre != self.id:
                    newevent = Event("REPORTE", self.clock+1.0, self.padre, self.id, self.pesoNodo)
                    print (" Soy el nodo ", self.id, " y mando REPORTE a mi padre ", self.padre, " en el tiempo ", newevent.getTime())
                    self.transmit(newevent)
                
        if event.getName() == "REPORTE":
            #print(f"Ya soy una hoja con peso {self.pesoNodo} y soy el nodo {self.id} y me llega de {event.getSource()} con valor en peso de {event.getPeso()}")
            #print(f"El reporte de mi hijo {event.getSource()} es con peso de {event.getPeso()}")
            for t in range(len(self.neighbors)):                #Para poner en verdadero el estado del nodo
                if event.getSource() == self.neighbors[t]:
                    self.recibi[t] = True
            
            if self.padre != self.id:                   #Es un nodo intermedio, reporta el peso minimo 2       
                if int(self.pesoNodo) < int(event.getPeso()):
                    self.valorMinimo = self.pesoNodo
                    self.pesoNodo = self.valorMinimo        #Ahora tiene un nuevo menor
                    if int(self.pesoNodo) > int(event.getPeso()):
                        self.camino = self.id                   #El es el camino
                else:
                    self.valorMinimo = event.getPeso()
                    self.pesoNodo = self.valorMinimo
                    self.camino = event.getSource()         #El camino es de quien te llego   
                print(f"El peso menor del nodo {self.id} y el nodo {event.getSource()} es --> {self.valorMinimo}")
                
                alerta2=True                                         #Para saber si ya son verdaderos sus estados
                for r in range(len(self.neighbors)):                #Reviso si todos los vecinos ya tienen verdadero en su estado de recibi
                    if self.recibi[r] == False:
                        alerta2 = False
                if alerta2 == True:
                    newevent = Event("REPORTE", self.clock+1.0, self.padre, self.id, self.valorMinimo)
                    print (" Soy el nodo ", self.id, " y mando REPORTE a mi padre ", self.padre, " en el tiempo ", newevent.getTime())
                    self.transmit(newevent)
        
            if self.padre == self.id:               #El nodo ya es el del inicio
                print("Entre al padre es igual al id")
                if int(self.valorMinimo) < int(event.getPeso()):
                    self.valorMinimo = self.valorMinimo
                    #self.camino = self.id                   #El es el camino
                else:
                    self.valorMinimo = event.getPeso()
                    self.camino = event.getSource()         #El camino es de quien te llego
                print(f"El peso menor del nodo {self.id} y el nodo {event.getSource()} es --> {self.valorMinimo}")
                
                alerta2=True                                         #Para saber si ya son verdaderos sus estados
                for r in range(len(self.neighbors)):                #Reviso si todos los vecinos ya tienen verdadero en su estado de recibi
                    if self.recibi[r] == False:
                        alerta2 = False
                if alerta2 == True:
                    newevent = Event("CAMBIA", self.clock+1.0, self.camino, self.id, self.valorMinimo)
                    print (" Soy el nodo ", self.id, " y mando CAMBIA a mi camino ", self.camino, " en el tiempo ", newevent.getTime())
                    self.transmit(newevent)
        
        if event.getName() == "CAMBIA":
            if self.id != self.camino:
                newevent = Event("CAMBIA", self.clock+1.0, self.camino, self.id, self.valorMinimo)
                print (" Soy el nodo ", self.id, " y mando CAMBIA a mi camino ", self.camino, " en el tiempo ", newevent.getTime())
                self.transmit(newevent)
            else:
                print(f"Soy el nodo {self.id} y soy el que tiene el peso minimo, el cual es {self.valorMinimo} y lo incremento a {int(self.valorMinimo) + 1}")
                
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

#iniciar pesos de los nodos

# inserta un evento semilla en la agenda y arranca
seed = Event("INICIO", 0.0, 2, 2, m.pesoNodo)
experiment.init(seed)
experiment.run()