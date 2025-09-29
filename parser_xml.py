import xml.etree.ElementTree as ET
from modelos.dron import Dron
from modelos.planta import Planta
from modelos.invernadero import Invernadero
from modelos.plan_riego import PlanRiego
from estructuras.lista_enlazada_simple import ListaEnlazadaSimple

def cargar_configuracion(ruta_archivo):
    try:
        tree = ET.parse(ruta_archivo)
        root = tree.getroot()

        # Drones globales - usando nuestra lista enlazada
        drones_globales = ListaEnlazadaSimple()
        lista_drones_elem = root.find('listaDrones')
        if lista_drones_elem is not None:
            for dron_elem in lista_drones_elem.findall('dron'):
                id_dron = int(dron_elem.get('id'))
                nombre = dron_elem.get('nombre')
                drones_globales.agregar_al_final(Dron(id_dron, nombre))

        lista_invernaderos = ListaEnlazadaSimple()
        lista_invernaderos_elem = root.find('listaInvernaderos')
        
        if lista_invernaderos_elem is None:
            return lista_invernaderos

        for invernadero_elem in lista_invernaderos_elem.findall('invernadero'):
            nombre_inv = invernadero_elem.get('nombre')
            num_hileras = int(invernadero_elem.find('numeroHileras').text)
            plantas_x_hilera = int(invernadero_elem.find('plantasXhilera').text)
            
            invernadero = Invernadero(nombre_inv, num_hileras, plantas_x_hilera)

            # Plantas
            lista_plantas_elem = invernadero_elem.find('listaPlantas')
            if lista_plantas_elem is not None:
                for planta_elem in lista_plantas_elem.findall('planta'):
                    hilera = int(planta_elem.get('hilera'))
                    posicion = int(planta_elem.get('posicion'))
                    litros = int(planta_elem.get('litrosAgua'))
                    gramos = int(planta_elem.get('gramosFertilizante'))
                    tipo = planta_elem.text.strip() if planta_elem.text else "Desconocido"
                    invernadero.agregar_planta(Planta(hilera, posicion, litros, gramos, tipo))

            # Asignación de drones - buscar en nuestra lista enlazada
            asignacion_drones_elem = invernadero_elem.find('asignacionDrones')
            if asignacion_drones_elem is not None:
                for asignacion in asignacion_drones_elem.findall('dron'):
                    id_dron = int(asignacion.get('id'))
                    hilera_asignada = int(asignacion.get('hilera'))
                    
                    # Buscar dron por ID en nuestra lista enlazada
                    dron_encontrado = None
                    for dron in drones_globales:
                        if dron.id == id_dron:
                            dron_encontrado = dron
                            break
                    
                    if dron_encontrado:
                        # Crear nueva instancia para este invernadero
                        nuevo_dron = Dron(dron_encontrado.id, dron_encontrado.nombre)
                        nuevo_dron.asignar_a_hilera(hilera_asignada)
                        invernadero.agregar_dron(nuevo_dron)

            # Planes de riego
            planes_elem = invernadero_elem.find('planesRiego')
            if planes_elem is not None:
                for plan_elem in planes_elem.findall('plan'):
                    nombre_plan = plan_elem.get('nombre')
                    plan = PlanRiego(nombre_plan)
                    texto = plan_elem.text
                    print(f"Plan '{nombre_plan}' cargado con pasos:")
                    for i, paso in enumerate(plan.secuencia):
                        print(f"  Paso {i+1}: {paso}")
                    
                    if texto:
                        # Limpieza manual sin split()
                        texto_limpio = ""
                        for char in texto:
                            if char not in [' ', '\n', '\t', '\r']:
                                texto_limpio += char
                        
                        # Parsear pasos manualmente
                        if texto_limpio:
                            paso_actual = ""
                            for char in texto_limpio:
                                if char == ',':
                                    if paso_actual:
                                        plan.agregar_paso(paso_actual)
                                        paso_actual = ""
                                else:
                                    paso_actual += char
                            
                            # Último paso
                            if paso_actual:
                                plan.agregar_paso(paso_actual)
                    
                    invernadero.agregar_plan_riego(plan)

            lista_invernaderos.agregar_al_final(invernadero)

        return lista_invernaderos

    except Exception as e:
        print(f"ERROR: {e}")
        return ListaEnlazadaSimple()