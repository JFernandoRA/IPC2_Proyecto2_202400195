from estructuras.lista_enlazada_simple import ListaEnlazadaSimple

def generar_instrucciones_para_plan(invernadero, nombre_plan):
    print(f"\n=== GENERANDO INSTRUCCIONES PARA PLAN: {nombre_plan} ===")
    
    # Buscar el plan
    plan_obj = None
    for p in invernadero.planes_riego:
        if p.nombre == nombre_plan:
            plan_obj = p
            break
    
    if plan_obj is None:
        print(f"ERROR: No se encontró el plan {nombre_plan}")
        return 0

    print(f"Plan encontrado: {nombre_plan} con {len(plan_obj.secuencia)} pasos")
    for i, paso in enumerate(plan_obj.secuencia):
        print(f"  Paso {i+1}: {paso}")

    # REINICIAR DRONES COMPLETAMENTE para este plan
    for d in invernadero.drones:
        d.instrucciones = ListaEnlazadaSimple()
        d.posicion_actual = 0
        d.litros_agua_utilizados = 0
        d.gramos_fertilizante_utilizados = 0

    # Segundo 1: todos avanzan a P1
    for d in invernadero.drones:
        d.posicion_actual = 1
        d.agregar_instruccion(f"Adelante (H{d.hilera_asignada}P1)")

    # Procesar cada paso del plan en ORDEN
    for paso_num, paso in enumerate(plan_obj.secuencia):
        if not isinstance(paso, str):
            continue
        
        s = paso.strip()
        if s == "" or not s.startswith('H'):
            continue
        
        print(f"Procesando paso {paso_num+1}: {s}")
        
        try:
            # Parsear formato "H1-P2" o "H1P2"
            s_limpio = s.replace(' ', '').replace('-', '')
            hilera_str = ""
            pos_str = ""
            encontro_p = False
            
            for char in s_limpio:
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
                print(f"  Interpretado: Hilera {hilera}, Posición {pos}")
            else:
                print(f"  ERROR: No se pudo interpretar {s}")
                continue
                
        except Exception as e:
            print(f"  ERROR parseando {s}: {e}")
            continue

        # Encontrar dron para esta hilera
        dron_activo = None
        for d in invernadero.drones:
            if d.hilera_asignada == hilera:
                dron_activo = d
                break
        
        if dron_activo is None:
            print(f"  ERROR: No hay dron asignado a hilera {hilera}")
            continue

        # Buscar planta
        planta = invernadero.buscar_planta_por_ubicacion(hilera, pos)
        if planta is None:
            print(f"  ERROR: No se encontró planta en H{hilera}P{pos}")
            continue

        print(f"  Planta encontrada: {planta.tipo}, Agua: {planta.litros_agua}L, Fert: {planta.gramos_fertilizante}g")

        # Mover dron activo a la posición
        print(f"  Dron {dron_activo.nombre} en posición {dron_activo.posicion_actual}, moviendo a {pos}")
        
        while dron_activo.posicion_actual < pos:
            dron_activo.posicion_actual += 1
            for d in invernadero.drones:
                if d == dron_activo:
                    d.agregar_instruccion(f"Adelante (H{hilera}P{d.posicion_actual})")
                else:
                    d.agregar_instruccion("Esperar")
            print(f"    Avanzó a posición {dron_activo.posicion_actual}")
        
        while dron_activo.posicion_actual > pos:
            dron_activo.posicion_actual -= 1
            for d in invernadero.drones:
                if d == dron_activo:
                    d.agregar_instruccion(f"Atras (H{hilera}P{d.posicion_actual})")
                else:
                    d.agregar_instruccion("Esperar")
            print(f"    Retrocedió a posición {dron_activo.posicion_actual}")

        # Regar
        print(f"  REGANDO: Dron {dron_activo.nombre} agrega {planta.litros_agua}L y {planta.gramos_fertilizante}g")
        dron_activo.litros_agua_utilizados += planta.litros_agua
        dron_activo.gramos_fertilizante_utilizados += planta.gramos_fertilizante
        
        for d in invernadero.drones:
            if d == dron_activo:
                d.agregar_instruccion(f"Regar (H{hilera}-P{pos})")
            else:
                d.agregar_instruccion("Esperar")

    # Alinear con FIN
    max_len = 0
    for d in invernadero.drones:
        if len(d.instrucciones) > max_len:
            max_len = len(d.instrucciones)
    
    for d in invernadero.drones:
        while len(d.instrucciones) < max_len:
            d.agregar_instruccion("FIN")
    
    # Mostrar resumen final
    print(f"\nRESUMEN PLAN {nombre_plan}:")
    for d in invernadero.drones:
        print(f"  {d.nombre}: {d.litros_agua_utilizados}L, {d.gramos_fertilizante_utilizados}g")
    
    return max_len