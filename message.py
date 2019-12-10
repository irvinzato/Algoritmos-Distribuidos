from event import Event

class Message(Event):

    def __init__(self, name, time, target, source, candidato):
        self.name=name
        self.time=time
        self.target=target
        self.source=source
        self.candidato=candidato
		
    def getCandidato(self):
        """ Devuelve el candidato o valor especial del evento """
        return (self.candidato)