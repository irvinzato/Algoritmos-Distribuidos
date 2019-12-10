import sys
from message import Message
from model import Model
from simulation import Simulation

class EleccionParo(Model):
    """ La clase AlgorithmFallo desciende de la clase Model e implementa los metodos 
    "init()" y "receive()", que en la clase madre se definen como abstractos """
	
    def init(self):
        """ Aqui se definen e inicializan los atributos particulares del algoritmo """
        self.listaOK = []
        self.soyLider = False
        self.liderId = self.id
        self.candidato = self.id
        self.estado = "NO_LIDER"
        self.banderaIgn = False

    def receive(self, event):

        if self.estado == "NO_LIDER":
            if event.name=="EXPIRAT2" and self.banderaIgn:
                self.banderaIgn = False
                return
            print ("NO_LIDER:Soy el nodo", self.id, "y recibi un",event.name, "a las",event.time,"del nodo", event.source)
            if event.name == "EXPIRAT2":
                evento = Message("EXPIRAT2", self.clock+3.0, self.id,self.id,None)
                self.transmit(evento)
                self.estado = "ALERTA"
            elif event.name == "HB":
                self.banderaIgn = True
                evento = Message("EXPIRAT2", self.clock+3.0, self.id,self.id,None)
                self.transmit(evento)
                evento = Message("OK", self.clock+1.0 , self.liderId, self.id,None)
                self.transmit(evento)

        elif self.estado == "ALERTA":
            print ("ALERTA:Soy el nodo", self.id, "y recibi un",event.name, "a las",event.time,"del nodo", event.source)
            if event.name == "EXPIRAT2":
                self.liderId = self.id
                for t in self.neighbors:
                    evento = Message("CANDIDATO", self.clock+1.0 , t, self.id,self.liderId)
                    self.transmit(evento)
                evento = Message("EXPIRAT3", self.clock+3.0, self.id,self.id,None)
                self.transmit(evento)
                self.estado = "ELECCION"
            elif event.name == "CANDIDATO":
                if self.liderId < event.candidato:
                    self.liderId = event.candidato
                for t in self.neighbors:
                    evento = Message("CANDIDATO", self.clock+1.0 , t, self.id,self.liderId)
                    self.transmit(evento)
                evento = Message("EXPIRAT3", self.clock+3.0, self.id,self.id,None)
                self.transmit(evento)
                self.estado = "ELECCION"
            elif event.name == "HB":
                self.banderaIgn = True
                evento = Message("EXPIRAT2", self.clock+3.0, self.id,self.id,None)
                self.transmit(evento)
                evento = Message("OK", self.clock+1.0 , self.liderId, self.id,None)
                self.transmit(evento)
                self.estado = "NO_LIDER"

        elif self.estado == "ELECCION":
            print ("ELECCION:Soy el nodo", self.id, "y recibi un",event.name, "a las",event.time,"del nodo", event.source)
            if event.name == "CANDIDATO":
                if self.liderId < event.candidato:
                    self.liderId = event.candidato
            elif event.name == "EXPIRAT3":
                if self.id == self.liderId:
                    self.estado = "LIDER"
                    print ("soy el nodo",self.id,"soy el lider")
                    evento = Message("EXPIRAT1", self.clock+2.0, self.id,self.id,None)
                    self.transmit(evento)
                else:
                    self.estado="NO_LIDER"
                    print ("Soy el nodo",self.id,"no soy el lider, el lider es",self.liderId)
                    evento = Message("EXPIRAT2", self.clock+4.0, self.id,self.id,None)
                    self.transmit(evento)
                    
        elif self.estado == "LIDER":
            print ("LIDER:Soy el nodo", self.id, "y recibi un",event.name, "a las",event.time,"del nodo", event.source)
            if event.name == "EXPIRAT1":
                self.listaOK= []
                for t in self.neighbors:
                    evento = Message("HB", self.clock+1.0 , t, self.id,None)
                    self.transmit(evento)
                evento = Message("EXPIRAT1", self.clock+2.0 , self.id, self.id,None)
                self.transmit(evento)
            if event.name == "OK":
                self.listaOK.append(event.source)


# ----------------------------------------------------------------------------------------
# "main()"
# ----------------------------------------------------------------------------------------

# construye una instancia de la clase Simulation recibiendo como parametros el nombre del 
# archivo que codifica la lista de adyacencias de la grafica y el tiempo max. de simulacion
if len(sys.argv) != 2:
    print ("Por favor escriba el nombre del archivo del grafo donde desea correr el algoritmo")
    raise SystemExit(1)
experiment = Simulation(sys.argv[1], 100)

# asocia un pareja proceso/modelo con cada nodo de la grafica
for i in range(1,len(experiment.graph)+1):
    m = EleccionParo()
    experiment.setModel(m, i)

# inserta un evento semilla en la agenda y arranca
for t in range(1,len(experiment.graph)+1):
    event = Message("EXPIRAT2", 3.0, t, t,None)
    experiment.init(event)

experiment.run()



