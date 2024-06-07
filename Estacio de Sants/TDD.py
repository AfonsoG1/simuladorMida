from esdeveniment import *
from passatger import *
from tren import *
from motorEventsDiscrets import *

'''
Podeu canviar el contingut de la funció de sota i així poder tenir el vostre propi banc de proves, no soc molt
de test així que us poso la versió cutre.
'''

def TDDMola(motor):
    pax=passatger()#el meu passatge, si necessita atributs doncs...
    pax.propietats["PMR"]=True #per exemple
    tog=tren()#si necessito un tren el tinc aquí (en noruec) però tampoc té atributs :(
    tog.propietats["pugen"]=100
    temps=0 #expressats en segons
    event=TipusEvent.Arribada
    elmeuobjecte=motor.donamObjecte("AV1")#està clar que AV1 és el nom del meu objecte
    for i in range(0,3):
        motor.donamObjecte("AV1").programarEsdeveniment(temps+i,event,pax,elmeuobjecte)
    