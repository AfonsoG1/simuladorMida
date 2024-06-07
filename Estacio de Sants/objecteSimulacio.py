'''
Doncs aquí estem en l'objecte pare de la vostra jerarquia d'elements pel vostre simulador a mida
Treballar amb programació orientat a objectes quan desenvolupem un simulador a mida té les seves avantatge:
1.- Reaprofitament de les classes bases, normalment un element que proveeix d'entitats sempre proveirà més o menys de la mateixa, un recurs estarà o no disponible...
2.- Els mètodes abstractes que sobreescrivim en faciliten la comprensió del codi
3.- i totes les avantatges que us han explicat a la carrera
'''
from enumeracions import *
from esdeveniment import *

#Fa molt que no programo en python, així que potser ho seu seria fer una interficie o alguna cosa d'aquests que feu el jovent...
class objecteSimulacio:
    #necessiteu afegir algun métode o propietat a la classe objecteSimulacio?
    _estat=None
    _nom=""
    _id=-1
    #una referencia al motor de simulacio
    motor=None
    
    def __init__(self,motor,parameters):
        #Inicialment els vostres objectes no tenen un estat definit l'heu de definir vosaltres en el vostre init
        self.set_estat(Estat.NONE)
        #Identificador únic
        params=parameters.split(",")
        self._id=int(params[0])
        self._nom=params[2]
        self.motor=motor
        
    def __repr__(self):
        return self._nom

    def tractarEsdeveniment(self, event):
        #Que ha de fer el vostre element en funció de l'estat en el que es troba i el tipus d'event
        assert (False)    

    #Programar un esdeveniment, el tempsExecució és el temps relatiu (el temps que trigueu a fer una acció: preparar entrepà, atendre a algú, aneu en compte els que processeu esdeveniments associats a un temps absolut)
    def programarEsdeveniment(self,tempsExecucio,tipusEsdeveniment,entitat,desti):
        if (desti==None):
            #Considerem None com un punt on s'eliminarà l'entitat temporal
            # Heu de fer alguna cosa per eliminar memòria?
            return 
        #esdeveniment que programeu que s'inserirà a la llista d'esdeveniment
        #Es guarda en el objecte que ha intentat enviar la entitat (origen)
        event=esdeveniment(desti,self.motor._tempsSimulacio+tempsExecucio,tipusEsdeveniment,entitat,self)
        self.motor.afegirEsdeveniment(event)
                
    #Sobrecarregueu aquesta funció per a inicialitzar el vostre objecte i, per exemple, poder recuperar els successors i predecessors (si s'escau)
    def iniciSimulacio(self):
        #self._successor[...]=self.motor.donamObjecte(identificador sucessor)
        self.estat=Estat.LLIURE
        #Inicialitzar les estructures que siguin necessàries
    
    def fiSimulacio(self):
        self.summary()
    
    '''
    centralitzar el canvi d'estat us pot anar molt bé per a registrar estadístics i controlar millor el codi
    eviteu fer self._state a qualsevol lloc
    '''
    def set_estat(self,estat):
        self._estat = estat;
    
    def get_estat(self):
        return self._estat;
    
    def id(self):
        return self._id;

    #sobrecarregueu aquest element per tal que mostreu un resum dels vostres estadístics
    def summary(self):
        print("mnty")
        assert (False)
        
        
