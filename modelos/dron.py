from estructuras.lista_enlazada_simple import ListaEnlazadaSimple

class Dron:
    def __init__(self, id_dron, nombre):
        self.id = id_dron
        self.nombre = nombre
        self.hilera_asignada = None
        self.posicion_actual = 0
        self.litros_agua_utilizados = 0
        self.gramos_fertilizante_utilizados = 0
        self.instrucciones = ListaEnlazadaSimple()
        self.riegos_pendientes = ListaEnlazadaSimple() 
        self.riegos_completados = 0 

    def asignar_a_hilera(self, numero_hilera):
        self.hilera_asignada = numero_hilera

    def agregar_instruccion(self, accion):
        self.instrucciones.agregar_al_final(accion)

    def obtener_instruccion_en_segundo(self, segundo):
        if segundo < len(self.instrucciones):
            return self.instrucciones.obtener_en_indice(segundo)
        else:
            return "FIN"

    def __str__(self):
        return f"Dron {self.nombre}, Hilera: {self.hilera_asignada}, Pos: {self.posicion_actual}"