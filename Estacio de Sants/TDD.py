from esdeveniment import *
from passatger import *
from tren import *
from motorEventsDiscrets import *

'''
Podeu canviar el contingut de la funció de sota i així poder tenir el vostre propi banc de proves, no soc molt
de test així que us poso la versió cutre.
'''

def TDDMola(motor):
    temps=0 #expressats en segons
    event=TipusEvent.Arribada
    elmeuobjecte=motor.donamObjecte("E7")#elmeu objecte puja
    elmeuobjecte2=motor.donamObjecte("E8")#elmeu objecte
    for i in range(0,10000):
        pax=passatger()#el meu passatge, si necessita atributs doncs...
        pax.propietats["PMR"]=False
        pax.propietats["GraoEsquerra"]=False
        motor.donamObjecte("AD4").programarEsdeveniment(temps+i/5,event,pax,elmeuobjecte)#sube, o sea viene de la andana hacia torniquets
        motor.donamObjecte("TO1").programarEsdeveniment(temps+i/5,event,pax,elmeuobjecte2)#baja, o sea viene de torniquets hacia andana



    