class tren:
    '''
    estaria bé que tots els trens tinguessin un id únic i totes les propietats mínimes que s'han de poder
    consultar, jo us recomanaria una estructura de l'estil diccionari que seria més escalable
    propietats={}
    propietats["baixen"]=100
    propietats["pugen"]=50 #això podria ser perfectament un valor d'una uniforme entre 50 i 100 per exemple
    propietats["via"]=...
    '''
    id=0
    propietats={}
    def __init__(self) -> None:
       pass