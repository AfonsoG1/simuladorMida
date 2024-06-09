import bisect
from esdeveniment import *


from passatger import *
from tren import *
from escalaMecanica import *
from TDD import *

'''
Inicieu el vostre motor de simulació a partir d'aquesta classe
'''

class motorEventsDiscrets:
    _tempsSimulacio = 0
    _llistaEsdeveniments = []
    _dictionariElements = {}
    
    def __init__(self):
        primerEsdeveniment=esdeveniment(self,0,TipusEvent.IniciSimulacio,None)
        self._llistaEsdeveniments.append(primerEsdeveniment)

    def now(self):
        return self._tempsSimulacio
    
    def __repr__(self):
        return "Soc el motor d'esdeveniments discrets"

    def trace(self,esdeveniment):
        return "Soc el motor d'esdeveniments discrets"

    def run(self,stdscr):
        self.carregarModel()
        #Sempre iniciem la simulació en temps 0
        self._tempsSimulacio=0
        #bucle de simulacio (condicio fi simulacio llista buida)
        while len(self._llistaEsdeveniments)>0:
            #recuperem esdeveniment simulacio
            properEsdeveniment=self._llistaEsdeveniments.pop(0)
            # sols per entendre com funciona el simulador d'esdeveniments discrets
            #actualitzem el rellotge de simulacio
            self._tempsSimulacio=properEsdeveniment.tempsExecucio;
            # deleguem l'accio a realitzar de l'esdeveniment a l'objecte que l'ha generat
            properEsdeveniment.perA.tractarEsdeveniment(properEsdeveniment)
            # la traça de l'esdeveniment, per tant no cal que la feu
            #print(properEsdeveniment.perA.trace(properEsdeveniment))

        #recollida d'estadistics
        self.fiSimulacio()
        
    def afegirEsdeveniment(self,event):
        if (event.tempsExecucio<self._tempsSimulacio):
            #no podem inserir un esdeveniment d'un temps ja passat
            return
            #assert(False)
        #inserir esdeveniment de forma ordenada
        bisect.insort(self._llistaEsdeveniments, event)
        a=10

    def donamObjecte(self,nomObjecte):
        
        if (len(nomObjecte)>0):
            return self._dictionariElements[nomObjecte]
        else:
            return None
        
    def carregarModel(self):
        index=0
        
        with open('model.txt') as f:
            linies = f.readlines()
            i=0
            for linia in linies:
                if i==0:
                    i=i+1
                    continue
                itms=len(self._dictionariElements)
                self.instanciar(linia)
                if (itms==len(self._dictionariElements)):
                    print("Si veus això és que no has pogut crear el "+linia)
                    assert(False)

    def temps(self):
        return self._tempsSimulacio

    #A completar per cadascun de vosaltres, heu d'instanciar el vostre element
    def instanciar(self,activitat):
        params=activitat.split(",")
        if '16'==params[0]:
            #split per identificar si tinc que crear més d'una referència del meu objecte
            instancies=params[3].split(";")
            instanciasenar=False
            for i in range(0,len(instancies)):
                #Les escales creades amb i senar seran de pujades altrament seran de baixades (hauríeu d'afegir un paràmetre adicional a la vostra creació)
                #Els torniquets creats amb i senar serna de sortida i altrament seran d'entrada (hauríeu d'afegir un paràmetre adicional a la vostra creació)
                #act=params[0]+","+","+instancies[i]+","+params[3]+","+params[4] + "," + i
                act=params[0]+","+instancies[i]+","+params[3]+","+params[4]
                instanciasenar=not instanciasenar
                self._dictionariElements[instancies[i]]=escalaMecanica(self,act, instanciasenar)
        if '20'==params[0]:
            instancies=params[3].split(";")
            instanciasenar=False
            for i in range(0,len(instancies)):
                act=params[0]+","+instancies[i]+","+params[3]+","+params[4]
                instanciasenar=not instanciasenar
                self._dictionariElements[instancies[i]]=torniquet(self,act, instanciasenar)   
        if '58'==params[0]:
            instancies=params[3].split(";")
            instanciasenar=False
            for i in range(0,len(instancies)):
                act=params[0]+","+instancies[i]+","+params[3]+","+params[4]
                instanciasenar=not instanciasenar
                self._dictionariElements[instancies[i]]=andana(self,act, instanciasenar)                 
        
    def iniciSimulacio(self):
        for element in self._dictionariElements.values():
            if element != None:
                element.iniciSimulacio()
        #Per tal que funcioni el bucle insereixo una arribada
        TDDMola(self)
        
    def tractarEsdeveniment(self,esdevenimentActual):
        if (esdevenimentActual.tipus==TipusEvent.IniciSimulacio):
            self.iniciSimulacio()

    def fiSimulacio(self):
        for element in self._dictionariElements.values():
            if element != None:
                element.summary()
    
            
