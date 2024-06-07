from enumeracions import *

class esdeveniment:
    def __init__(self,perA,temps,tipus,entitat=None,desde=None,prioritat=1):
            # inicialitzar element de simulacio
        self.tipus=tipus
        self.perA=perA
        self.tempsExecucio=temps
        self.entitat=entitat
        self.desde=desde
        self.prioritat=prioritat

    def __repr__(self):
        return str(self.tempsExecucio)+' '+str(self.type)

    def __gt__(self, esdeveniment):
        # Si tenen la mateixa prioritat, el que té menys temps d'execució té prioritat
        if self.tempsExecucio == esdeveniment.tempsExecucio:
            return self.prioritat > esdeveniment.prioritat
        
        return self.tempsExecucio > esdeveniment.tempsExecucio