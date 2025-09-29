from estructuras.lista_enlazada_simple import ListaEnlazadaSimple

def generar_salida_xml(lista_invernaderos, ruta_salida="salida.xml"):
    contenido_xml = '<?xml version="1.0"?>\n<datosSalida>\n  <listaInvernaderos>\n'

    # Iterar sobre invernaderos
    for invernadero in lista_invernaderos:
        contenido_xml += f'    <invernadero nombre="{invernadero.nombre}">\n'
        contenido_xml += '      <listaPlanes>\n'

        # Para cada plan
        for plan in invernadero.planes_riego:
            # Simular este plan para obtener los datos actualizados
            from simulador_riego import generar_instrucciones_para_plan
            tiempo_optimo = generar_instrucciones_para_plan(invernadero, plan.nombre)
            
            # Calcular totales para este plan
            total_agua = 0
            total_fert = 0
            for dron in invernadero.drones:
                total_agua += dron.litros_agua_utilizados
                total_fert += dron.gramos_fertilizante_utilizados

            contenido_xml += f'        <plan nombre="{plan.nombre}">\n'
            contenido_xml += f'          <tiempoOptimoSegundos>{tiempo_optimo}</tiempoOptimoSegundos>\n'
            contenido_xml += f'          <aguaRequeridaLitros>{total_agua}</aguaRequeridaLitros>\n'
            contenido_xml += f'          <fertilizanteRequeridoGramos>{total_fert}</fertilizanteRequeridoGramos>\n'
            
            # Eficiencia de drones
            contenido_xml += '          <eficienciaDronesRegadores>\n'
            for dron in invernadero.drones:
                contenido_xml += f'            <dron nombre="{dron.nombre}" litrosAgua="{dron.litros_agua_utilizados}" gramosFertilizante="{dron.gramos_fertilizante_utilizados}"/>\n'
            contenido_xml += '          </eficienciaDronesRegadores>\n'
            
            # Instrucciones por tiempo
            contenido_xml += '          <instrucciones>\n'
            
            if not invernadero.drones.esta_vacia():
                primer_dron = invernadero.drones.obtener_en_indice(0)
                max_segundos = len(primer_dron.instrucciones)
                
                for segundo in range(max_segundos):
                    contenido_xml += f'            <tiempo segundos="{segundo + 1}">\n'
                    
                    for dron in invernadero.drones:
                        accion = dron.obtener_instruccion_en_segundo(segundo)
                        contenido_xml += f'              <dron nombre="{dron.nombre}" accion="{accion}"/>\n'
                    
                    contenido_xml += '            </tiempo>\n'
            
            contenido_xml += '          </instrucciones>\n'
            contenido_xml += '        </plan>\n'
        
        contenido_xml += '      </listaPlanes>\n'
        contenido_xml += '    </invernadero>\n'
    
    contenido_xml += '  </listaInvernaderos>\n</datosSalida>'

    # Guardar el archivo
    with open(ruta_salida, 'w', encoding='utf-8') as f:
        f.write(contenido_xml)
    
    print(f"Archivo XML generado: {ruta_salida}")

def generar_salida_xml_alternativo(lista_invernaderos, ruta_salida="salida_alternativa.xml"):
    """
    Versión alternativa que genera el XML exactamente como en el ejemplo del enunciado.
    """
    
    contenido_xml = '<?xml version="1.0"?>\n<datosSalida>\n  <ListaInvernaderos>\n'

    for invernadero in lista_invernaderos:
        contenido_xml += f'    <invernadero nombre="{invernadero.nombre}">\n'
        contenido_xml += '      <listaPlanes>\n'

        for plan in invernadero.planes_riego:
            from simulador_riego import generar_instrucciones_para_plan
            tiempo_optimo = generar_instrucciones_para_plan(invernadero, plan.nombre)
            
            total_agua = 0
            total_fert = 0
            for dron in invernadero.drones:
                total_agua += dron.litros_agua_utilizados
                total_fert += dron.gramos_fertilizante_utilizados

            contenido_xml += f'        <plan nombre="{plan.nombre}">\n'
            contenido_xml += f'          <tiempoOptimoSegundos>{tiempo_optimo}</tiempoOptimoSegundos>\n'
            contenido_xml += f'          <aguaRequeridaLitros>{total_agua}</aguaRequeridaLitros>\n'
            contenido_xml += f'          <fertilizanteRequeridoGramos>{total_fert}</fertilizanteRequeridoGramos>\n'
            
            contenido_xml += '          <eficienciaDronesRegadores>\n'
            for dron in invernadero.drones:
                contenido_xml += f'            <dron nombre="{dron.nombre}" litrosAgua="{dron.litros_agua_utilizados}" gramosFertilizante="{dron.gramos_fertilizante_utilizados}"/>\n'
            contenido_xml += '          </eficienciaDronesRegadores>\n'
            
            contenido_xml += '          <instrucciones>\n'
            
            if not invernadero.drones.esta_vacia():
                primer_dron = invernadero.drones.obtener_en_indice(0)
                max_segundos = len(primer_dron.instrucciones)
                
                for segundo in range(max_segundos):
                    contenido_xml += f'            <tiempo segundos="{segundo + 1}">\n'
                    
                    for dron in invernadero.drones:
                        accion = dron.obtener_instruccion_en_segundo(segundo)
                        # Limpiar la acción para el XML (sin caracteres especiales)
                        accion_limpia = accion.replace('"', "'")
                        contenido_xml += f'              <dron nombre="{dron.nombre}" accion="{accion_limpia}"/>\n'
                    
                    contenido_xml += '            </tiempo>\n'
            
            contenido_xml += '          </instrucciones>\n'
            contenido_xml += '        </plan>\n'
        
        contenido_xml += '      </listaPlanes>\n'
        contenido_xml += '    </invernadero>\n'
    
    contenido_xml += '  </ListaInvernaderos>\n</datosSalida>'

    with open(ruta_salida, 'w', encoding='utf-8') as f:
        f.write(contenido_xml)
    
    print(f"Archivo XML alternativo generado: {ruta_salida}")