from .nodo import Nodo

class ListaEnlazadaSimple:
    def __init__(self):
        self.cabeza = None      
        self.tamanio = 0       

    def esta_vacia(self):
        return self.cabeza is None

    def agregar_al_final(self, dato):
        nuevo_nodo = Nodo(dato)
        if self.esta_vacia():
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza
            while actual.siguiente is not None:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo
        self.tamanio += 1

    def obtener_en_indice(self, indice):
        if indice < 0 or indice >= self.tamanio:
            return None
        actual = self.cabeza
        for _ in range(indice):
            actual = actual.siguiente
        return actual.dato

    def buscar(self, criterio):
        actual = self.cabeza
        while actual is not None:
            if criterio(actual.dato):
                return actual.dato
            actual = actual.siguiente
        return None

    def __iter__(self):
        actual = self.cabeza
        while actual is not None:
            yield actual.dato
            actual = actual.siguiente

    def __len__(self):
        return self.tamanio

    def __str__(self):
        if self.esta_vacia():
            return "[]"
        resultado = ""
        primero = True
        for dato in self:
            if not primero:
                resultado += " -> "
            resultado += str(dato)
            primero = False
        return "[" + resultado + "]"