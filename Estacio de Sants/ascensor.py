from objecteSimulacio import *
from motorEventsDiscrets import *
import json
import random

class ascensor(objecteSimulacio):
    #variables membres o propietats del vostre element de simulació
    darrer_estat=None
    def __init__(self,motor,parametres):
        super(ascensor, self).__init__(motor,parametres)
        #recuperar els meus paràmetres des del meu arxiu de configuració ascensor.cfg
        with open('ascensor.cfg', 'r') as file:
            data_loaded = json.load(file)

        dades = data_loaded["Propietats"][self._nom]

        # Aquest és un exemple de dues propietats del meu objecte tonto
        self.temps = dades["temps"] #usaré per calcular una uniforme +-3
        self.seguent = dades["seguent"]
        
    def __repr__(self):
        return self._nom
        
    def tractarEsdeveniment(self, event):
        #És molt habitual establir una primera selecció de l'estat en que em trobo i després fer una selecció de l'event
        #pel meu ascensor no faig res
        self.darrer_estat=self._estat
        if (self.get_estat()==Estat.LLIURE):
            if (event.tipus==TipusEvent.Arribada):
                self.processarArribadaLliure(event) 
                return
        
        if (self.get_estat()==Estat.SERVEI): #una mica més de complicació però sense fer res
            if (event.tipus==TipusEvent.Arribada):
                self.processarArribadaLliure(event) 
                return
        pass      

    #processar Arribada seria tot el diagrama de fluxe que penja de l'estat Lliure quan rep un event arribada
    def processarArribadaLliure(self,event):
        #el meu objecte és molt tonto i sols propaga l'entitat cap a endavant programant una arribada
        delta= random.uniform(self.temps-3, self.temps+3)
        self.programarEsdeveniment(delta,TipusEvent.Arribada,event.entitat,self.motor.donamObjecte(self.seguent))
        self.set_estat(Estat.SERVEI)
        
    #recordeu que aquí heu de programar tot el que heu representat en el diagrama de processos per l'estat no definit
    def iniciSimulacio(self):
        super(ascensor, self).iniciSimulacio()
        #per simplificar exemple, considero que el meu successor serà un sol i que serà l'objecte amb _id=_id+1 
        self._successors=self.motor.donamObjecte(self.seguent) #base 0 però identificador en base 1
        self.set_estat(Estat.LLIURE)
         #Això és molt important recordar de poder fixar la llavor
        random.seed(5)

    #Al final de la simulació el motor us cridarà aquest mètode i mostrareu els vostres estadístics i l'estat en el que us trobeu
    def summary(self):
        return str(self.get_estat()) + " temps estat_abans event estat_actual estadistic1 estadístic 2 ..."
        
    def trace(self,esdeveniment):
        return "Temps {} ".format(esdeveniment.tempsExecucio)+" "+str(self)+" a "+str(self.darrer_estat)+ " rep "+ str(esdeveniment.tipus)+" passa a "+str(self.get_estat()) 
