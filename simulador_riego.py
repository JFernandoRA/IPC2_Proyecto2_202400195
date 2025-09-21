def generar_instrucciones_para_plan(invernadero, nombre_plan):
    plan_obj = None
    for plan in invernadero.planes_riego:
        if plan.nombre == nombre_plan:
            plan_obj = plan
            break

    if plan_obj is None:
        print(f"Error: No se encontró el plan '{nombre_plan}' en el invernadero '{invernadero.nombre}'.")
        return 0

    # Reiniciar las instrucciones de todos los drones
    for dron in invernadero.drones:
        dron.instrucciones = type(dron.instrucciones)()  # Crea una nueva instancia vacía del mismo tipo
        dron.reiniciar_posicion()

    # Convertir la secuencia del plan en una lista de ubicaciones (hilera, posicion)
    pasos_plan = []
    for paso_str in plan_obj.secuencia:
        if not paso_str:
            continue
        # Formato esperado: "H1-P2"
        try:
            partes = paso_str.replace('H', '').replace('P', '').split('-')
            hilera = int(partes[0])
            posicion = int(partes[1])
            pasos_plan.append((hilera, posicion))
        except (ValueError, IndexError):
            print(f"Advertencia: Paso '{paso_str}' no tiene formato válido. Se omitirá.")
            continue

    # Para cada paso en el plan, calcular las instrucciones para todos los drones
    tiempo_actual = 0

    for idx_paso, (hilera_objetivo, posicion_objetivo) in enumerate(pasos_plan):
        # Encontrar el dron asignado a esta hilera
        dron_activo = None
        for dron in invernadero.drones:
            if dron.hilera_asignada == hilera_objetivo:
                dron_activo = dron
                break

        if dron_activo is None:
            print(f"Advertencia: No hay dron asignado a la hilera {hilera_objetivo}. Paso omitido.")
            continue

        # Calcular cuántos segundos necesita el dron activo para llegar a la posición
        distancia = abs(dron_activo.posicion_actual - posicion_objetivo)
        direccion = "Adelante" if posicion_objetivo > dron_activo.posicion_actual else "Retroceder"

        # Generar instrucciones de movimiento para el dron activo
        for i in range(distancia):
            if direccion == "Adelante":
                dron_activo.avanzar()
                accion = f"Adelante(H{hilera_objetivo}P{dron_activo.posicion_actual})"
            else:
                dron_activo.retroceder()
                accion = f"Retroceder(H{hilera_objetivo}P{dron_activo.posicion_actual})"
            dron_activo.agregar_instruccion(accion)
            tiempo_actual += 1

            # Mientras el dron activo se mueve, los demás deben "Esperar"
            for otro_dron in invernadero.drones:
                if otro_dron != dron_activo:
                    otro_dron.agregar_instruccion("Esperar")

        # El dron activo riega
        planta = invernadero.buscar_planta_por_ubicacion(hilera_objetivo, posicion_objetivo)
        if planta:
            dron_activo.regar(planta.litros_agua, planta.gramos_fertilizante)
            accion_riego = "Regar"
        else:
            accion_riego = "Regar"  # Asumimos que riega aunque no encontremos la planta (por consistencia)

        dron_activo.agregar_instruccion(accion_riego)
        tiempo_actual += 1

        # Los demás drones "Esperan" durante el riego
        for otro_dron in invernadero.drones:
            if otro_dron != dron_activo:
                otro_dron.agregar_instruccion("Esperar")

    # Después del último riego, todos los drones deben regresar a la posición 0
    for dron in invernadero.drones:
        distancia_vuelta = abs(dron.posicion_actual - 0)
        direccion_vuelta = "Retroceder" if dron.posicion_actual > 0 else "Adelante"

        for i in range(distancia_vuelta):
            if direccion_vuelta == "Retroceder":
                dron.retroceder()
                accion = f"Retroceder(H{dron.hilera_asignada}P{dron.posicion_actual})"
            else:
                dron.avanzar()
                accion = f"Adelante(H{dron.hilera_asignada}P{dron.posicion_actual})"
            dron.agregar_instruccion(accion)
            tiempo_actual += 1

            # Los demás drones esperan
            for otro_dron in invernadero.drones:
                if otro_dron != dron:
                    otro_dron.agregar_instruccion("Esperar")

        # Finalmente, agregar "FIN"
        dron.agregar_instruccion("FIN")

    return tiempo_actual