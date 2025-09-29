from estructuras.lista_enlazada_simple import ListaEnlazadaSimple

class PlanRiego:
    def __init__(self, nombre):
        self.nombre = nombre
        self.secuencia = ListaEnlazadaSimple()

    def agregar_paso(self, paso):
        self.secuencia.agregar_al_final(paso)

    def __str__(self):
        if self.secuencia.esta_vacia():
            return f"Plan '{self.nombre}': vacío"
        
        resultado = f"Plan '{self.nombre}': "
        primero = True
        for paso in self.secuencia:
            if not primero:
                resultado += ", "
            resultado += str(paso)
            primero = False
        return resultado