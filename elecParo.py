# Este archivo sirve de modelo para la creacion de aplicaciones, i.e. algoritmos concretos
""" Implementa la simulacion del algoritmo de Propagacion de Informacion (Segall) como ejemplo
de aplicacion """

import sys
from mensaje import Mensaje
from model import Model
from simulation import Simulation

class Fallas(Model):
    """ La clase Algorithm desciende de la clase Model e implementa los metodos 
    "init()" y "receive()", que en la clase madre se definen como abstractos """
	
    def init(self):
        """ Aqui se definen e inicializan los atributos particulares del algoritmo """
        self.activo = False
        self.sinVisitar = self.neighbors[:]
        self.estado = "NO_LIDER"
        self.OK = []
        self.flagLid = self.id
        self.flagTime = False
        self.Paro = False
        self.flagEstado = False

    def receive(self, event):
        if(self.Paro == False):
            if(self.estado == "NO_LIDER"):                       
                if(event.getName()=="EXPIRAT2" and self.flagTime):
                    self.flagTime = False
                    return
                if(event.getName()=="EXPIRAT2"):
                    newMessage = Mensaje("EXPIRAT2", self.clock+3.0, self.id,self.id,None)
                    self.transmit(newMessage)
                    self.estado = "ALERTA"
                    return
                print("NO_LIDER -> Soy el nodo", self.id, "y recibi un",event.getName(), "a las",event.getTime(),"del nodo", event.getSource())
                
                if(event.getName()=="HB"):
                    self.flagTime = True
                    newMessage = Mensaje("EXPIRAT2", self.clock+3.0, self.id,self.id,None)
                    self.transmit(newMessage)
                    
                    newMessage = Mensaje("OK", self.clock+1.0, self.flagLid,self.id,None)
                    self.transmit(newMessage)
                    print ("OKOKOK Soy el nodo", self.id," MANDE OK al nodo",self.flagLid," en el tiempo",self.clock)
                    self.estado = "NO_LIDER"

                if(event.getName()=="ELECCION"):
                    if(int(event.getCandidato())>self.id):
                        self.flagLid = int(event.getCandidato())
                    else:
                        self.flagLid = self.id
                    for i in self.sinVisitar:
                        newMessage = Mensaje("ELECCION", self.clock+1.0,i,self.id,self.flagLid)
                        self.transmit(newMessage)
                        print ("**Soy el nodo ", self.id," MANDE ELECCION de",self.flagLid," al nodo ",i," en el tiempo",event.getTime()+1 )
                    
                    newMessage = Mensaje("EXPIRAT3", self.clock+3.0, self.id,self.id,None)
                    self.transmit(newMessage)
                    self.estado = "ELECCION"

            if(event.getName()=="FALLA"):
                self.flagEstado = self.estado
                self.Paro = True

            elif(self.estado=="ALERTA"):
                print ("-- ALERTA -> Soy el nodo ", self.id, " recibi un",event.getName(), " en el tiempo",event.getTime(),"del nodo", event.getSource())
                if(event.getName()=="EXPIRAT2"):
                    self.flagLid = self.id
                    for i in range(len(self.sinVisitar)):
                        newMessage = Mensaje("ELECCION", self.clock+1.0,self.sinVisitar[i],self.id,self.flagLid)
                        self.transmit(newMessage)
                        print ("**Soy el nodo ", self.id," MANDE ELECCION de",self.flagLid," al nodo ",self.sinVisitar[i]," en el tiempo",self.clock )
                    
                    newMessage = Mensaje("EXPIRAT3",self.clock+3.0,self.id,self.id,None)
                    self.transmit(newMessage)
                    self.estado = "ELECCION"
                if(event.getName() == "ELECCION"):
                    if(event.getCandidato()>self.id):
                        self.flagLid = event.getCandidato()
                    else:
                        self.flagLid = self.id
                    for i in range(len(self.sinVisitar)):
                        newMessage = Mensaje("ELECCION", self.clock+1.0,self.sinVisitar[i],self.id,self.flagLid)
                        self.transmit(newMessage)
                        print ("**Soy el nodo ", self.id," MANDE ELECCION de",self.flagLid," al nodo ",self.sinVisitar[i]," en el tiempo",self.clock )
                    
                    newMessage = Mensaje("EXPIRAT3",self.clock+3.0,self.id,self.id,None)
                    self.transmit(newMessage)
                    self.estado = "ELECCION"
                if(event.getName()=="HB"):
                    self.flagTime = True
                    newMessage = Mensaje("EXPIRAT2",self.clock+3.0,self.id,self.id,None)
                    self.transmit(newMessage)
                
                    newMessage = Mensaje("OK",self.clock+1.0,self.flagLid,self.id,None)
                    self.transmit(newMessage)
                    self.estado = "NO_LIDER"

            elif(self.estado=="ELECCION"):
                if(event.getName()=="HB" or event.getName()=="OK" ):
                    self.estado = "ELECCION"
                    return
                if(event.getName()=="ELECCION"):
                    if(event.getCandidato()>self.flagLid):
                        self.flagLid = event.getCandidato()
                    self.estado = "ELECCION"
                    return
                print ("!! ELECCION -> Soy el nodo ", self.id, " recibi un",event.getName(), "a las",event.getTime(),"del nodo", event.getSource())

                if(event.getName()=="EXPIRAT3"):
                    if(self.flagLid == self.id):
                        print("     SOY EL NODO", self.id," SOY EL NUEVO LIDER")
                        newMessage = Mensaje("EXPIRAT1",self.clock+2.0,self.id,self.id,None)
                        self.transmit(newMessage)
                        self.estado = "LIDER"
                    else:
                        newMessage = Mensaje("EXPIRAT2",self.clock+3.0,self.id,self.id,None)
                        self.transmit(newMessage)
                        self.estado = "NO_LIDER"
                
            elif(self.estado == "LIDER"):
                print ("|||| LIDER -> Soy el nodo ", self.id, " recibi un",event.getName(), "a las",event.getTime(),"del nodo", event.getSource())
                if(event.getName()=="EXPIRAT1"):
                    self.OK= []
                    for i in range(len(self.sinVisitar)):
                        newMessage = Mensaje("HB",self.clock+1.0,self.sinVisitar[i],self.id,None)
                        self.transmit(newMessage)
                    newMessage = Mensaje("EXPIRAT1",self.clock+2.0,self.id,self.id,None)
                    self.transmit(newMessage)
                    self.estado = "LIDER"
                if(event.getName()=="OK"):
                    self.OK.append(event.getSource())
                if(event.getName() == "HB"):
                    if(event.getSource()>self.flagLid):
                        self.flagLid = event.getSource()
                    if(self.flagLid == self.id):
                        print("     SOY EL NODO ", self.id," SOY EL NUEVO LIDER")
                        self.estado = "LIDER"
                        newMessage = Mensaje("HB",self.clock+1.0,event.getSource(),self.id,None)
                        self.transmit(newMessage)
                    else:
                        self.estado = "NO_LIDER"
                
                if(event.getName() == "ELECCION"):
                    if(event.getCandidato()>self.flagLid):
                        self.flagLid = event.getCandidato()
                    for i in range(len(self.sinVisitar)):
                        newMessage = Mensaje("ELECCION", self.clock+1.0,self.sinVisitar[i],self.id,self.flagLid)
                        self.transmit(newMessage)
                        print ("**Soy el nodo ", self.id," MANDE ELECCION de",self.flagLid," al nodo ",self.sinVisitar[i]," en el tiempo",self.clock )
                    newMessage = Mensaje("EXPIRAT3",self.clock+3.0,self.id,self.id,None)
                    self.transmit(newMessage)
                    self.estado = "ELECCION"    
        elif(self.Paro):
            print("     SOY EL NODO ",self.id," ESTOY EN FALLA")
            newMessage = Mensaje("EXPIRAT4",self.clock+100.0,self.id,self.id,None)
            self.transmit(newMessage)
            self.Paro = self.estado
            self.estado = "FALLA"
        if(self.estado =="FALLA"):
            if(event.getName()=="EXPIRAT4"):
                print("     SOY EL NODO: ",self.id," Y YA ESTOY VIVO")
                self.estado = self.flagEstado
                self.Paro = False

                
       
       
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
    m = Fallas()
    experiment.setModel(m, i)

#inserta un evento semilla en la agenda y arranca
seed = []
for j in range(1,len(experiment.graph)+1):
    seed.append(Mensaje("EXPIRAT2",0.0,j,j,0))
    experiment.init(seed[j-1])

#seed2 = Mensaje("FALLA", 15.0, 5, 5,0)
#experiment.init(seed2)
experiment.run()
