from ..estructuras.lista_enlazada_simple import ListaEnlazadaSimple

class PlanRiego:
    def __init__(self, nombre):
        self.nombre = nombre
        self.secuencia = ListaEnlazadaSimple()  

    def agregar_paso(self, paso):
        self.secuencia.agregar_al_final(paso)

    def obtener_pasos(self):
        return iter(self.secuencia)

    def __str__(self):
        if len(self.secuencia) == 0:
            pasos_str = ""
        else:
            pasos_str = ""
            primero = True
            for paso in self.secuencia:
                if not primero:
                    pasos_str += ", "
                pasos_str += str(paso)
                primero = False
        return f"Plan '{self.nombre}': {pasos_str}"