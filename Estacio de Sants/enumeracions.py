from enum import Enum

#Amplieu amb aquells estats que detecteu per a cada objecte
class Estat(Enum):
    NONE = 0
    LLIURE = 1
    SERVEI = 2

#Amplieu amb aquells tipus d'events que considereu necessaris.
class TipusEvent(Enum):
    IniciSimulacio=1 #en el motor que us passo no s'enviarà com un event si no que invoco el mètode directe
    FiSimulacio=2    #en el motor que us passo no s'enviarà com un event si no que invoco el mètode directe
    Arribada=3


#Amplieu per si voleu usar alhora de treure una traça dels events.
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKRARO= '\033[97m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
