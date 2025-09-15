import xml.etree.ElementTree as ET
from modelos import Invernadero, Dron, Planta, PlanRiego

def cargar_configuracion(ruta_archivo):
    from estructuras.lista_enlazada_simple import ListaEnlazadaSimple
    lista_invernaderos = ListaEnlazadaSimple()
    tree = ET.parse(ruta_archivo)
    root = tree.getroot() 
    drones_globales = ListaEnlazadaSimple()  
    for dron_elem in root.find('listaDrones').findall('dron'):
        id_dron = int(dron_elem.get('id'))
        nombre = dron_elem.get('nombre')
        nuevo_dron = Dron(id_dron, nombre)
        drones_globales.agregar_al_final(nuevo_dron)

    for invernadero_elem in root.find('listaInvernaderos').findall('invernadero'):
        nombre_inv = invernadero_elem.get('nombre')
        num_hileras = int(invernadero_elem.find('numeroHileras').text)
        plantas_x_hilera = int(invernadero_elem.find('plantasXhilera').text)

        invernadero = Invernadero(nombre_inv, num_hileras, plantas_x_hilera)

        for planta_elem in invernadero_elem.find('listaPlantas').findall('planta'):
            hilera = int(planta_elem.get('hilera'))
            posicion = int(planta_elem.get('posicion'))
            litros = int(planta_elem.get('litrosAgua'))
            gramos = int(planta_elem.get('gramosFertilizante'))
            tipo = planta_elem.text.strip() if planta_elem.text else "Desconocido"

            nueva_planta = Planta(hilera, posicion, litros, gramos, tipo)
            invernadero.agregar_planta(nueva_planta)

        asignacion_elem = invernadero_elem.find('asignacionDrones')
        if asignacion_elem is not None:
            for asignacion_dron in asignacion_elem.findall('dron'):
                id_dron = int(asignacion_dron.get('id'))
                hilera_asignada = int(asignacion_dron.get('hilera'))
                dron_a_asignar = drones_globales.buscar(lambda d: d.id == id_dron)
                if dron_a_asignar:
                    dron_a_asignar.asignar_a_hilera(hilera_asignada)
                    invernadero.agregar_dron(dron_a_asignar) 

        planes_elem = invernadero_elem.find('planesRiego')
        if planes_elem is not None:
            for plan_elem in planes_elem.findall('plan'):
                nombre_plan = plan_elem.get('nombre')
                plan = PlanRiego(nombre_plan)
                secuencia_texto = plan_elem.text.strip() if plan_elem.text else ""
                pasos = secuencia_texto.split(',')

                for paso in pasos:
                    paso_limpio = paso.strip()
                    if paso_limpio:  
                        plan.agregar_paso(paso_limpio)

                invernadero.agregar_plan_riego(plan)

        lista_invernaderos.agregar_al_final(invernadero)

    return lista_invernaderos