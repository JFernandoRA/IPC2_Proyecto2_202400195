from ..estructuras.lista_enlazada_simple import ListaEnlazadaSimple
from .dron import Dron
from .planta import Planta
from .plan_riego import PlanRiego

class Invernadero:
    def __init__(self, nombre, numero_hileras, plantas_x_hilera):
        self.nombre = nombre
        self.numero_hileras = numero_hileras
        self.plantas_x_hilera = plantas_x_hilera
        self.plantas = ListaEnlazadaSimple()    
        self.drones = ListaEnlazadaSimple()     
        self.planes_riego = ListaEnlazadaSimple() 

    def agregar_planta(self, planta):
        self.plantas.agregar_al_final(planta)

    def agregar_dron(self, dron):
        self.drones.agregar_al_final(dron)

    def agregar_plan_riego(self, plan):
        self.planes_riego.agregar_al_final(plan)

    def buscar_dron_por_id(self, id_dron):
        return self.drones.buscar(lambda dron: dron.id == id_dron)

    def buscar_planta_por_ubicacion(self, hilera, posicion):
        return self.plantas.buscar(lambda planta: planta.hilera == hilera and planta.posicion == posicion)

    def __str__(self):
        return f"Invernadero: {self.nombre} ({self.numero_hileras} hileras x {self.plantas_x_hilera} plantas)"