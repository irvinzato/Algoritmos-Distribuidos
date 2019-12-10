# Este archivo sirve de modelo para la creacion de aplicaciones, i.e. algoritmos concretos
""" Implementa la simulacion del algoritmo de Propagacion de Informacion (Segall) como ejemplo
de aplicacion """

import sys
from event import Event
from model import Model
#from process import Process
#from simulator import Simulator
from simulation import Simulation

class LCR(Model):
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
            #mensaje = "CANDIDATO,1".split(',')
            m1 = "CANDIDATO"
            m2 = str(event.getSource())
            mensaje = (m1+","+m2).split(",")
            print(f"el mensaje tiene en mensaje {mensaje[0]} y en nodo {mensaje[1]}")
            #print(f"{mensaje}"  
            if mensaje[0] == "CANDIDATO":
                if int(mensaje[1]) > self.id:
                    #mensaje = ("CANDIDATO,"+candidato)       #Guardar mensaje con candidato
                    mensaje[0] = "CANDIDATO"
                    #candidato = str(mensaje[1])
                    #mensaje[1] = candidato
                    #print(f"La casilla uno tiene {mensaje[0]} y la casilla dos tiene {mensaje[1]}")
                    newevent = Event(mensaje, self.clock+1.0, self.sinVisitar[0] , self.id)
                    print (" Soy el nodo ", self.id, " y mando al CANDIDATO --> ", mensaje[1] ,"a mi vecino: ", self.sinVisitar[0], " en el tiempo ", newevent.getTime())
                    self.transmit(newevent)
                else:
                    if int(mensaje[1]) <= self.id and self.visited != True:
                        print("El id es mayor que la fuente")
                        candidato = str(self.id)
                        mensaje[0] = "CANDIDATO"
                        mensaje[1] = candidato
                        newevent = Event(mensaje, self.clock+1.0, self.sinVisitar[0], self.id)
                        print (" Soy el nodo ", self.id, " y mando al CANDIDATO --> ", mensaje[1]  ,"a mi vecino: ", self.sinVisitar[0], " en el tiempo ", newevent.getTime())
                        self.transmit(newevent)    
                        self.visited = True          
                    elif int(mensaje[1]) == self.id:
                        print("la fuente es igual que el id")
                        mensaje[0] = "ELECTO"
                        #electo = str(self.id)
                        #mensaje[1] = electo
                        newevent = Event(mensaje, self.clock+1.0, self.sinVisitar[0], self.id)
                        print (" Soy el nodo ", self.id, " y mando al nodo ELECTO --> ", mensaje[1] ,"a mi vecino: ", self.sinVisitar[0], " en el tiempo ", newevent.getTime())
                        self.transmit(newevent)
                #self.visited = True
            elif mensaje[0] == "ELECTO":
                #print("El mensaje que recibi ya es lider")
                self.lider = mensaje[1]             #Ya tenemos lider
                if int(mensaje[1]) != self.id:           #Tiene que avisar que es lider a los otros nodos
                    newevent = Event(mensaje, self.clock+1.0, self.sinVisitar[0], self.id)
                    print (" Soy el nodo ", self.id, " y mando mensaje que ya fue ELECTO --> ", mensaje[1] ,"a mi vecino: ", self.sinVisitar[0], " en el tiempo ", newevent.getTime())
                    self.transmit(newevent)
        if event.getName()[0] == "CANDIDATO":
            if int(event.getName()[1]) > self.id:
                event.getName()[0] ="CANDIDATO"
                newevent = Event(event.getName(), self.clock+1.0, self.sinVisitar[0] , self.id)
                print (" Soy el nodo ", self.id, " y mando al CANDIDATO --> ", event.getName()[1] ,"a mi vecino: ", self.sinVisitar[0], " en el tiempo ", newevent.getTime())
                self.transmit(newevent)
            else:
                if int(event.getName()[1]) <= self.id and self.visited != True:
                    event.getName()[0] = "CANDIDATO"
                    event.getName()[1] = self.id
                    newevent = Event(event.getName(), self.clock+1.0, self.sinVisitar[0], self.id)
                    print (" Soy el nodo ", self.id, " y mando al CANDIDATO --> ", event.getName()[1]  ,"a mi vecino: ", self.sinVisitar[0], " en el tiempo ", newevent.getTime())
                    self.transmit(newevent)    
                    self.visited = True  
                elif int(event.getName()[1]) == self.id:
                    event.getName()[0] = "ELECTO"
                    newevent = Event(event.getName(), self.clock+1.0, self.sinVisitar[0], self.id)
                    print (" Soy el nodo ", self.id, " y mando al nodo ELECTO --> ", event.getName()[1] ,"a mi vecino: ", self.sinVisitar[0], " en el tiempo ", newevent.getTime())
                    self.transmit(newevent)
        if event.getName()[0] == "ELECTO":
            self.lider = event.getName()[1]
            if int(event.getName()[1]) != self.id:
                newevent = Event(event.getName(), self.clock+1.0, self.sinVisitar[0], self.id)
                print (" Soy el nodo ", self.id, " y mando mensaje que ya fue ELECTO --> ", event.getName()[1] ,"a mi vecino: ", self.sinVisitar[0], " en el tiempo ", newevent.getTime())
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
    m = LCR()
    experiment.setModel(m, i)

# inserta un evento semilla en la agenda y arranca
#mensaje = "CANDIDATO,1".split(',')
#mensaje = "CANDIDATO,7".split(',')

#seed1 = Event("DESPIERTA", 0.0, 1, 1)
#seed2 = Event("DESPIERTA", 0.0, 2, 2)
#seed3 = Event("DESPIERTA", 0.0, 3, 3)
#seed4 = Event("DESPIERTA", 0.0, 4, 4)
#seed5 = Event("DESPIERTA", 0.0, 5, 5)
#seed6 = Event("DESPIERTA", 0.0, 6, 6)
#seed7 = Event("DESPIERTA", 0.0, 7, 7)
seed8 = Event("DESPIERTA", 0.0, 8, 8)

#experiment.init(seed1)
#experiment.init(seed2)
#experiment.init(seed3)
#experiment.init(seed4)
#experiment.init(seed5)
#experiment.init(seed6)
#experiment.init(seed7)
experiment.init(seed8)

experiment.run()