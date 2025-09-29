from estructuras.lista_enlazada_simple import ListaEnlazadaSimple

def generar_instrucciones_para_plan(invernadero, nombre_plan):
    plan_obj = None
    for p in invernadero.planes_riego:
        if p.nombre == nombre_plan:
            plan_obj = p
            break

    if plan_obj is None:
        return 0

    for d in invernadero.drones:
        d.instrucciones = ListaEnlazadaSimple()
        d.posicion_actual = 0
        d.litros_agua_utilizados = 0
        d.gramos_fertilizante_utilizados = 0
        d.riegos_completados = 0

    asignaciones = asignar_riegos_por_dron(invernadero, plan_obj)
    tiempo_actual = 0
    activo = True

    while activo:
        activo = False
        riego_en_curso = False

        for dron in invernadero.drones:
            if len(asignaciones[dron.nombre]) > dron.riegos_completados or dron.posicion_actual > 0:
                activo = True

        if not activo:
            break

        for dron in invernadero.drones:
            if len(asignaciones[dron.nombre]) > dron.riegos_completados:
                riego_actual = asignaciones[dron.nombre][dron.riegos_completados]
                pos_destino = riego_actual['posicion']
                
                if dron.posicion_actual < pos_destino:
                    dron.posicion_actual += 1
                    dron.agregar_instruccion(f"Adelante (H{dron.hilera_asignada}P{dron.posicion_actual})")
                elif dron.posicion_actual > pos_destino:
                    dron.posicion_actual -= 1
                    dron.agregar_instruccion(f"Atrás (H{dron.hilera_asignada}P{dron.posicion_actual})")
                else:
                    if not riego_en_curso:
                        planta = invernadero.buscar_planta_por_ubicacion(dron.hilera_asignada, pos_destino)
                        if planta:
                            dron.litros_agua_utilizados += planta.litros_agua
                            dron.gramos_fertilizante_utilizados += planta.gramos_fertilizante
                            dron.agregar_instruccion(f"Regar (H{dron.hilera_asignada}-P{pos_destino})")
                            dron.riegos_completados += 1
                            riego_en_curso = True
                        else:
                            dron.agregar_instruccion("Esperar")
                    else:
                        dron.agregar_instruccion("Esperar")
            else:
                if dron.posicion_actual > 0:
                    dron.posicion_actual -= 1
                    if dron.posicion_actual > 0:
                        dron.agregar_instruccion(f"Atrás (H{dron.hilera_asignada}P{dron.posicion_actual})")
                    else:
                        dron.agregar_instruccion("FIN")
                else:
                    dron.agregar_instruccion("FIN")

        tiempo_actual += 1

    max_len = 0
    for d in invernadero.drones:
        if len(d.instrucciones) > max_len:
            max_len = len(d.instrucciones)

    for d in invernadero.drones:
        while len(d.instrucciones) < max_len:
            d.agregar_instruccion("FIN")

    return max_len

def asignar_riegos_por_dron(invernadero, plan_obj):
    asignaciones = {}
    
    for dron in invernadero.drones:
        asignaciones[dron.nombre] = []

    for paso in plan_obj.secuencia:
        if not isinstance(paso, str):
            continue

        paso_limpio = paso.strip().replace(' ', '').replace('-', '')
        
        try:
            hilera_str = ""
            pos_str = ""
            encontro_p = False

            for char in paso_limpio:
                if char == 'H':
                    continue
                elif char == 'P':
                    encontro_p = True
                    continue
                else:
                    if not encontro_p:
                        hilera_str += char
                    else:
                        pos_str += char

            if hilera_str and pos_str:
                hilera = int(hilera_str)
                pos = int(pos_str)
                
                dron_activo = None
                for d in invernadero.drones:
                    if d.hilera_asignada == hilera:
                        dron_activo = d
                        break

                if dron_activo is None:
                    continue

                planta = invernadero.buscar_planta_por_ubicacion(hilera, pos)
                if planta is None:
                    continue

                riego = {
                    'hilera': hilera,
                    'posicion': pos,
                    'litros': planta.litros_agua,
                    'gramos': planta.gramos_fertilizante
                }
                asignaciones[dron_activo.nombre].append(riego)

        except Exception as e:
            continue

    return asignaciones