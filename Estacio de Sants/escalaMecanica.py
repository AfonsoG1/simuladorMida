from objecteSimulacio import *
from motorEventsDiscrets import *
import json
import random

class escalaMecanica(objecteSimulacio):
    #variables membres o propietats del vostre element de simulació
    darrer_estat=None
    def __init__(self,motor,parametres, instanciasenar):
        super(escalaMecanica, self).__init__(motor,parametres, instanciasenar)
        #recuperar els meus paràmetres des del meu arxiu de configuració ESME5301.cfg (escalaMecanica)
        with open('ESME5301.cfg', 'r') as file:
            data_loaded = json.load(file)

        pujada = False
        #i senar = pujada
        if (instanciasenar): pujada=True
        
        dades = data_loaded["Propietats"][self._nom]

        # propietats del objecte 
        self.temps = dades.get("temps", 0)
        self.longitud = dades.get("longitud", 0)
        self.graons = dades.get("graons", 0)
        self.capacitatMax = dades.get("capacitat", 0)
        self.velocitat = dades.get("velocitat", 0)
        #self.pujada = dades.get("pujada", False)
        self.seguent = dades.get("seguent", "")
        self.pujada = pujada
        self.cua = []
        self.ocupants = 0
        self.ocupantsEsquerra = 0
        

    def __repr__(self):
        return self._nom
        
    def tractarEsdeveniment(self, event):
        #print("entra tract")
        self.darrer_estat = self._estat
        if self.get_estat() == Estat.DISPONIBLE:
            if event.tipus == TipusEvent.Arribada:
                self.processarArribadaDisponible(event)
            # elif event.tipus == TipusEvent.FiDisponible:
            #     self.processarEstropeada(event)

        elif self.get_estat() == Estat.BLOQUEADA:
            if event.tipus == TipusEvent.Arribada:
                self.processarArribadaBloqueada(event)
            # elif event.tipus == TipusEvent.FiBloqueo:
            #     self.processarEstropeada(event)

        elif self.get_estat() == Estat.ESPATLLAT:
            if event.tipus == TipusEvent.Arribada:
                self.processarArribadaBloqueada(event)
            if event.tipus == TipusEvent.DemanarOperari:
                self.processarDemanarOperari(event)

        elif self.get_estat() == Estat.ESPERAROPERARI:
            # if event.tipus == TipusEvent.Arribada:
            #     self.processarArribadaBloqueada(event)
            if event.tipus == TipusEvent.ArribaOperari:
                self.processarArribaOperari(event)

        elif self.get_estat() == Estat.REPARANT:
            # if event.tipus == TipusEvent.Arribada:
            #     self.processarArribadaBloqueada(event)
            if event.tipus == TipusEvent.FiReparacio:
                self.processarFiReparacio(event)        
                

                
        else: print("oops falta handling estat")
        


    def processarArribadaDisponible(self, event):
        #si es puja els de la esquerra pujen mes 2x rapid
        if self.pujada:
            #utilitzar grao esquerra, 60% que utilicen escaleras izquierda  si no esta lleno O si no hay espacio a la derecha
            if (((random.uniform(0, 1)) < 0.6) and (self.ocupantsEsquerra < (self.capacitatMax / 2)) ) or ((self.ocupants)-(self.ocupantsEsquerra)) >= ((self.capacitatMax / 2)): 
                delta = random.normalvariate(self.temps/2, 2)#com avancen 2x mes rapid fem que tardi 2x menys de base
                self.ocupantsEsquerra+=1
                self.total_passengers_esquerra+=1
                self.ocupants+=1
                self.total_passengers +=1
                self.total_time_on_escalator+=delta
                event.entitat.propietats['GraoEsquerra']=True
                self.programarEsdeveniment(delta, TipusEvent.Arribada, event.entitat, self._successors)

            #si va por la derecha y no esta lleno
            else:
                delta = random.normalvariate(self.temps, 2)
                self.ocupants+=1
                self.total_passengers +=1
                self.total_time_on_escalator+=delta
                self.programarEsdeveniment(delta, TipusEvent.Arribada, event.entitat, self._successors)
        


        #Si es de baixada
        else:
            delta = random.normalvariate(self.temps, 2)
            #utilitzar grao esquerra, 50% que utilicen escaleras izquierda  si no esta lleno o si no hay espacio a la derecha
            if (random.uniform(0, 1) < 0.5 and self.ocupantsEsquerra < (self.capacitatMax / 2) ) or (self.ocupants-self.ocupantsEsquerra) >= (self.capacitatMax / 2): 
                #print("baixada entro esquerra")
                #print(self.ocupants)
                self.ocupantsEsquerra +=1
                self.total_passengers_esquerra+=1
                self.ocupants+=1
                self.total_passengers +=1
                self.total_time_on_escalator+=delta
                event.entitat.propietats['GraoEsquerra']=True
                self.programarEsdeveniment(delta, TipusEvent.Arribada, event.entitat, self._successors)

            #si va por la derecha y no esta lleno
            else:
                #print("baixada entro dreta")
                self.ocupants+=1
                self.total_passengers +=1
                self.total_time_on_escalator+=delta
                self.programarEsdeveniment(delta, TipusEvent.Arribada, event.entitat, self._successors)
            
        

        #probabilitat espatllar 1% cada 50
        if self.total_passengers % 50 == 0:
            if random.uniform(0, 1) < 0.01:  # 1% chance 
                self.statsVegadesEspatllat+=1
                self.statsManutencio+=delta
                self.set_estat(Estat.ESPATLLAT)
                self.programarEsdeveniment(delta, TipusEvent.DemanarOperari, event.entitat, self)

        #stats teps espera cua
        if event.entitat.propietats['tempsEsperaCua'] > self.statsPaxAmbMajorEsperaCua:
            self.statsPaxAmbMajorEsperaCua = event.entitat.propietats['tempsEsperaCua']

        #canviem d'estat si esta a maxima ocupacio
        #print(self.ocupants)
        if self.ocupants >= self.capacitatMax: 
            self.set_estat(Estat.BLOQUEADA)
            #print("lleno")





    
    def processarArribadaBloqueada(self, event):
        #al llegar un nuevo pax(o uno que esta esperando) confirmamos si sigue ocupada, si ya no esta pasamos a disponible y enviamos pax 
        if (self.ocupants < self.capacitatMax) and not ( (self.get_estat() ==Estat.ESPATLLAT) or (self.get_estat() ==Estat.ESPERAROPERARI) or (self.get_estat() ==Estat.REPARANT) ):
            #print("hay hueco")
            self.set_estat(Estat.DISPONIBLE)
            if event.entitat.id in self.cua:
                self.cua.remove(event.entitat.id)

        #si sigue lleno o esta estropeado
        else: 
            #print(len(self.cua))
            if event.entitat not in self.cua:
                self.cua.append(event.entitat.id)


        if (len(self.cua)) > self.max_queue_length: self.max_queue_length=len(self.cua)
        #enviar pax a escalera, 2s de delay para que el evento se añada con un poco de delay(si es 0 se ejecuta todo el rato ya que vuelve a entrar al evento hasta que haya hueco)
        event.entitat.propietats["tempsEsperaCua"] += 2
        self.programarEsdeveniment(2, TipusEvent.Arribada, event.entitat, self)



    def processarDemanarOperari(self, event):
        #print("entra1")
        delta = random.normalvariate(5, 10)#hasta que llega el operario OP2  normalvariate(5*60, 60)
        self.statsManutencio+=delta
        self.set_estat(Estat.ESPERAROPERARI)
        self.programarEsdeveniment(delta, TipusEvent.ArribaOperari, event.entitat, self)
        #self.motor.donamObjecte(OP2) Assumeixo que no juntem coses...
        #he create una clase custom de andanes i torniquets 

    def processarArribaOperari(self, event):
        #print("entra2")
        delta = random.normalvariate(10, 15) # normalvariate(40*60, 10*60)
        self.statsManutencio+=delta
        self.set_estat(Estat.REPARANT)
        self.programarEsdeveniment(delta, TipusEvent.FiReparacio, event.entitat, self)

    def processarFiReparacio(self, event):
        #print("entra3")
        delta = random.normalvariate(20, 10) #normalvariate(60, 10)
        self.statsManutencio+=delta
        if len(self.cua) > 0:
            self.set_estat(Estat.BLOQUEADA)
        else:
            self.set_estat(Estat.DISPONIBLE)
        self.programarEsdeveniment(delta, TipusEvent.Desbloqueig, event.entitat, None)

        
    def iniciSimulacio(self):
        super(escalaMecanica, self).iniciSimulacio()
        self._successors=self.motor.donamObjecte(self.seguent)
        self.set_estat(Estat.DISPONIBLE)
        random.seed(4273)
        # Variables per les estadistiques
        self.total_passengers = 0
        self.total_passengers_esquerra = 0
        self.total_passengers_in_queue = 0
        self.total_time_on_escalator = 0
        self.max_queue_length = 0
        self.max_ocupacio_stat = 0
        self.statsPaxAmbMajorEsperaCua = 0
        self.statsVegadesEspatllat = 0
        self.statsManutencio = 0
        #self.programarEsdeveniment(0, TipusEvent.Cicle, None, self)

    def summary(self):
        stats = (
            f"Model: {self._nom} \n"
            f"Estat actual: {self.get_estat()} \n"
            f"Es de Pujada: {self.pujada} \n"
            f"Total passengers: {self.total_passengers} \n"
            f"Total passengers grao esquerra: {self.total_passengers_esquerra} \n"
            f"Total temps a escala: {self.total_time_on_escalator} \n"
            f"Primig temps pax a escala: {self.total_time_on_escalator/self.total_passengers} \n"
            f"Max Temps Que Un Pax Va Esperar A Cua: {self.statsPaxAmbMajorEsperaCua} segons\n"
            f"Tamany Maxim Cua: {self.max_queue_length} persones\n"
            f"Vegades Espatllat: {self.statsVegadesEspatllat} \n"
            f"Temps En Manutencio: {self.statsManutencio} \n"
        )
        print(stats)
        return stats   
    
    def trace(self,esdeveniment):
        return "Temps {} ".format(esdeveniment.tempsExecucio)+" "+str(self)+" a "+str(self.darrer_estat)+ " rep "+ str(esdeveniment.tipus)+" passa a "+str(self.get_estat()) 






class torniquet(objecteSimulacio):
    def __init__(self,motor,parametres, instanciasenar):
        super(torniquet, self).__init__(motor,parametres, instanciasenar)

    def tractarEsdeveniment(self, event):
        #print("quitando pax escalera")
        #pax que llegan de la escalera, permite quitarlos de las escaleras cuando acaben de subir/bajarlas o sea cuando llegan al prox event
        self.motor.donamObjecte("E7").ocupants-=1
        if event.entitat.propietats['GraoEsquerra']: self.motor.donamObjecte("E7").ocupantsEsquerra-=1


    def trace(self,esdeveniment):
        return 


class andana(objecteSimulacio):
    def __init__(self,motor,parametres, instanciasenar):
        super(andana, self).__init__(motor,parametres, instanciasenar)  

    def tractarEsdeveniment(self, event):
        #print("quitando pax escalera")
    #pax que llegan de la escalera
        self.motor.donamObjecte("E8").ocupants-=1
        if event.entitat.propietats['GraoEsquerra']: 
            self.motor.donamObjecte("E8").ocupantsEsquerra-=1
            

    def trace(self,esdeveniment):
        return           
