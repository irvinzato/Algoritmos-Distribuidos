# Este archivo sirve de modelo para la creacion de aplicaciones, i.e. algoritmos concretos
""" Implementa la simulacion del algoritmo de Propagacion de Informacion (Segall) como ejemplo
de aplicacion """

import sys
from event import Event
from model import Model
#from process import Process
#from simulator import Simulator
from simulation import Simulation

class Snap(Model):
    """ La clase Algorithm desciende de la clase Model e implementa los metodos 
    "init()" y "receive()", que en la clase madre se definen como abstractos """
	
    def init(self):
        """ Aqui se definen e inicializan los atributos particulares del algoritmo """
        self.padre = self.id
        self.sinVisitar =  []  
        self.visited = False
        self.primerFoto = True              #Variables para el espia
        self.termineSnap = False            
        self.estadoLocal = []
        self.visitadoChi = []
        self.msj = []
        self.recibChi = [0]*len(self.neighbors)
        print ("inicializo algoritmo")
        for i in range (len(self.neighbors)):       #De esta forma se pueden manipular las listas por aparte
            self.sinVisitar.append(self.neighbors[i])
        for i in range(len(self.neighbors)):        
            self.visitadoChi.append(None)    

    def go(self):
        if(len(self.sinVisitar) != 0 ):
            k = self.sinVisitar.pop(0)
            newevent = Event("DESC", self.clock+1.0, k, self.id)
            print (" Soy el nodo ", self.id, " y mando DESC a mi vecino ", k, " en el tiempo de ", newevent.getTime())
            self.transmit(newevent)
        elif(self.padre != self.id):
            newevent = Event("REG", self.clock+1.0, self.padre, self.id)
            print (" Soy el nodo ", self.id, " y mando REG a mi padre ", self.padre, " en el tiempo de ", newevent.getTime())
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
            if(self.primerFoto == False):            #Ya puede empezar a guardar
                for i in range(len(self.recibChi)):
                    if(event.getSource() == self.recibChi[i][0] and self.recibChi[i][3] == True):
                        if(self.recibChi[i][3] == True):
                            X = self.recibChi[i]
                            X = list(X)
                            if(X[2] == None):
                                aux = []
                                X[2] = aux
                            X[2].append("DESC")
                            X = tuple(X)
                            self.recibChi[i] = X
                            #print("Añadi a recibCHI ", self.recibChi[i])
                            #self.recibChi[i][2].append("DESC")

            self.go() 

        elif(event.getName() == "REG"):
            if(self.primerFoto == False):            #Ya puede empezar a guardar
                for i in range(len(self.recibChi)):
                    if(event.getSource() == self.recibChi[i][0] and self.recibChi[i][3] == True):
                        if(self.recibChi[i][3] == True):
                            X = self.recibChi[i]
                            X = list(X)
                            if(X[2] == None):
                                aux = []
                                X[2] = aux
                            X[2].append("REG")
                            X = tuple(X)
                            self.recibChi[i] = X
                            #print("Añadi a recibCHI ", self.recibChi[i])      
            self.go()

        elif(event.getName() == "AVISO"):       #Solo entra cuando el mensaje es AVISO para eliminar la fuente
            if(event.getSource() in self.sinVisitar):
                self.sinVisitar.remove(event.getSource())
            
            if(self.primerFoto == False):            #Ya puede empezar a guardar
                for i in range(len(self.recibChi)):
                    if(event.getSource() == self.recibChi[i][0] and self.recibChi[i][3] == True):
                        if(self.recibChi[i][3] == True):
                            X = self.recibChi[i]
                            X = list(X)
                            if(X[2] == None):
                                aux = []
                                X[2] = aux
                            X[2].append("AVISO")
                            X = tuple(X)
                            self.recibChi[i] = X
                            #print("Añadi a recibCHI ", self.recibChi[i])

        elif(event.getName() == "FOTO"):
            #print ("SOY EL NODO ", self.id, " MI PADRE ES ", self.padre, " ENTRE A FOTO EN EL TIEMPO ", event.getTime())
            if(self.primerFoto == True):        #es la primera vez que recibe foto
                self.primerFoto = False
                self.estadoLocal.append(self.padre)     #lo primero que hace es guardar su estado local
                self.estadoLocal.append(self.sinVisitar)
                self.estadoLocal.append(self.visited)

                for i in range(len(self.visitadoChi)): #bandera del canal neighbors
                    if(event.getSource() == self.visitadoChi[i]):
                        self.visitadoChi[i] = True         #ya fue visitado el canal

                for t in self.neighbors:                #manda mensaje foto a todos sus vecinos
                    newevent = Event("FOTO", self.clock+1.0, t, self.id)
                    print ("        SOY EL NODO ", self.id, " MANDO MENSAJE FOTO A ", t, " EN EL TIEMPO ", newevent.getTime())
                    self.transmit(newevent)

                if(event.getSource() == self.id):       #caso especial para la semilla
                    self.recibChi = [0]*(len(self.neighbors)+1)  #Para almacenar el valor chi de la semilla
                    self.recibChi[len(self.recibChi)-1] = event.getSource(), self.id, self.msj, True
                    for i in range(len(self.neighbors)):
                        self.recibChi[i] = self.neighbors[i], self.id, None, True

                else:       #No eres la semilla
                    for i in range(len(self.neighbors)):
                        if(event.getSource() == self.neighbors[i]):
                            self.recibChi[i] = event.getSource(), self.id, self.msj, True
                        else:
                            self.recibChi[i] = self.neighbors[i], self.id, None, True
                
                print("     Mi canal es ", self.recibChi, " soy el nodo ", self.id)
                print("     Mi arreglo visitadoChi tiene ", self.visitadoChi , " soy el nodo ", self.id)
                print("     SOY EL NODO", self.id, " MI ESTADO LOCAL ES ", self.estadoLocal)

            else:
                
                for i in range(len(self.neighbors)): #bandera para saber que el nodo ya tiene puros false
                    if(event.getSource() == self.neighbors[i]):
                        self.visitadoChi[i] = False         #ya fue visitado el canal
                    #else:
                    #    self.visitadoChi[i] = False

                for i in range(len(self.neighbors)):
                    if(self.recibChi[i][3] == True ):
                        X = self.recibChi[i]
                        X = list(X)
                        X[3] = False
                        X = tuple(X)
                        self.recibChi[i] = X
                        print("     ||| SOY EL NODO ", self.id, " YA CERRE EL CANAL ", self.recibChi[i][0], 
                        self.recibChi[i][1], " MI REGISTRO ES ", self.recibChi[i][2], " |||")

                for i in range(len(self.visitadoChi)):  #Para saber si todos sus canales ya fueron visitados
                    if(self.visitadoChi[i] == False):   #Todos sus canales ya son falsos
                        self.termineSnap = True
                    else:
                        self.termineSnap = False
                        break
                
                if(self.termineSnap == True):
                    print("     TERMINE SNAP")
                    #print("     ----MI CHI ES ", self.recibChi)
                
                #print("     ****SOY EL NODO", self.id, " MI ARREGLO VISITADOCHI TIENE ", self.visitadoChi)
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
    m = Snap()
    experiment.setModel(m, i)

# inserta un evento semilla en la agenda y arranca
seed = Event("DESC", 0.0, 1, 1)
seed1 = Event("FOTO", 0.9, 3, 3)
experiment.init(seed)
experiment.init(seed1)
experiment.run()

