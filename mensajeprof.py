from event import Event

class Mensaje(Event):

    def __init__(self, name, time, target, source, profundidad):
        self.name=name
        self.time=time
        self.target=target
        self.source=source
        self.profundidad=profundidad
		
    def getProfundidad(self):
        """ Devuelve el profundidad o valor especial del evento """
        return (self.profundidad)