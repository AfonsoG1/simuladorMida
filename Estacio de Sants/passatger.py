


class passatger:
    id = 0

    def __init__(self) -> None:
        self.id = passatger.id
        passatger.id += 1
        
        self.propietats = {}
        self.propietats["posicio"] = 0
        self.propietats["tempsEsperaCua"] = 0
        self.propietats["PMR"] = False
        self.propietats["GraoEsquerra"] = False

    def __repr__(self):
        return f"Passatger {self.id} - Propietats: {self.propietats}"











# class passatger:
#     '''
#     estaria bé que tots els paxs tinguessin un id únic i totes les propietats mínimes que s'han de poder
#     consultar, jo us recomanaria una estructura de l'estil diccionari que seria més escalable
#     propietats={}
#     propietats["baixen"]=100
#     propietats["pugen"]=50 #això podria ser perfectament un valor d'una uniforme entre 50 i 100 per exemple
#     propietats["PMR"]=...
#     '''
#     id=0
#     propietats={}
#     def __init__(self) -> None:
#         pass
