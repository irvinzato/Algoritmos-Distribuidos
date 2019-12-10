from event import Event           #Herencia
#class Tarjeta(Event):

class Eleccion(Event):

    def __init__(self, name, time, target, source, electo):
        #super().__init__(name, time, target, source)
        self.name   = name
        self.time   = time        
        self.target = target        
        self.source = source
        self.electo = electo

    def getName(self):
        """ Devuelve el nombre del evento """
        return (self.name)
		
    def getTime(self):
        """ Devuelve el tiempo en el que debe ocurrir el evento """
        return (self.time)
		
    def getTarget(self):
        """ Devuelve la identidad del proceso al que va dirigido """
        return (self.target)
		
    def getSource(self):
        """ Devuelve la identidad del proceso que origina el evento """
        return (self.source)

    def getElecto(self):
        """ Devuelve la identidad del proceso que origina el evento """
        return (self.electo)