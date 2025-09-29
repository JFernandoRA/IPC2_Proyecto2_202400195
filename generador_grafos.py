import graphviz
from estructuras.lista_enlazada_simple import ListaEnlazadaSimple

def generar_grafo_lista_plan(plan_riego, tiempo):
    """
    Genera un grafo de la lista enlazada del plan de riego
    SOLO muestra los pasos hasta el tiempo especificado
    """
    dot = graphviz.Digraph(comment=f'Plan {plan_riego.nombre} - Tiempo {tiempo}')
    
    # Configuración básica
    dot.attr(rankdir='LR')  # Left to Right - HORIZONTAL como una cola
    dot.attr('node', shape='box', style='filled', fillcolor='lightblue')
    dot.attr('edge', arrowhead='vee')  # Flechas simples
    
    dot.attr(label=f'Plan: {plan_riego.nombre} - Ejecutado hasta tiempo: {tiempo} segundos')
    dot.attr(labelloc='t')
    
    if plan_riego.secuencia.esta_vacia():
        dot.node('empty', 'Plan Vacío', shape='ellipse', fillcolor='lightcoral')
        return dot
    
    # Recorrer la lista de pasos del plan SOLO HASTA EL TIEMPO ESPECIFICADO
    actual = plan_riego.secuencia.cabeza
    indice = 0
    nodos_creados = []
    
    while actual is not None and indice < tiempo:  # SOLO hasta el tiempo 't'
        paso = actual.data
        node_id = f'paso_{indice}'
        nodos_creados.append(node_id)
        
        # Color según el progreso
        if indice < tiempo - 1:
            fillcolor = 'lightgreen'  # Pasos ya completados
        elif indice == tiempo - 1:
            fillcolor = 'yellow'      # Paso actual (ejecutándose)
        else:
            fillcolor = 'lightgray'   # Pasos futuros
        
        dot.node(node_id, f'Paso {indice+1}\n{paso}', fillcolor=fillcolor)
        
        # Conectar con flecha al siguiente paso (solo si hay siguiente y estamos en tiempo)
        if actual.siguiente is not None and (indice + 1) < tiempo:
            next_id = f'paso_{indice + 1}'
            dot.edge(node_id, next_id)
        
        actual = actual.siguiente
        indice += 1
    
   
    if tiempo > len(plan_riego.secuencia):
        fin_id = 'fin'
        dot.node(fin_id, f'FIN\n(Completado)', 
                 shape='ellipse', fillcolor='orange')
        
        # Conectar el último paso con FIN
        if nodos_creados:
            ultimo_nodo = nodos_creados[-1]
            dot.edge(ultimo_nodo, fin_id)
    
  
    if nodos_creados:
        dot.attr(rank='same')
        # Crear una cadena de ranking para mantener el orden
        with dot.subgraph() as s:
            s.attr(rank='same')
            for nodo in nodos_creados:
                s.node(nodo)
            if tiempo > len(plan_riego.secuencia):
                s.node('fin')
    
    return dot

def generar_grafo_lista_drones(lista_drones, tiempo):
    """
    Genera un grafo de la lista enlazada de drones con su estado en el tiempo especificado
    """
    dot = graphviz.Digraph(comment=f'Lista Drones - Tiempo {tiempo}')
    
    dot.attr(rankdir='TB')  # Top to Bottom - VERTICAL
    dot.attr('node', shape='record', style='filled', fillcolor='lightyellow')
    dot.attr('edge', arrowhead='vee')
    
    dot.attr(label=f'Estado de Drones - Tiempo: {tiempo} segundos')
    dot.attr(labelloc='t')
    
    if lista_drones.esta_vacia():
        dot.node('empty', 'No hay drones', shape='ellipse', fillcolor='lightcoral')
        return dot
    
    # Recorrer la lista de drones
    actual = lista_drones.cabeza
    indice = 0
    
    while actual is not None:
        dron = actual.data
        node_id = f'dron_{indice}'
        
        # Obtener instrucción actual en este tiempo
        instruccion_actual = "Esperar"
        if tiempo > 0 and tiempo <= len(dron.instrucciones):
            instruccion_actual = dron.instrucciones.obtener_en_indice(tiempo-1)
        
        # Color según la instrucción actual
        if 'Regar' in instruccion_actual:
            fillcolor = '#C8E6C9'  # Verde
        elif 'Adelante' in instruccion_actual:
            fillcolor = '#BBDEFB'  # Azul
        elif 'Atras' in instruccion_actual:
            fillcolor = '#FFCDD2'  # Rojo
        elif 'FIN' in instruccion_actual:
            fillcolor = '#FFE0B2'  # Naranja
        else:
            fillcolor = '#F5F5F5'  # Gris (Esperar)
        
        # Crear label con información del estado actual
        label = (
            f'{{Dron: {dron.nombre} | '
            f'Hilera: H{dron.hilera_asignada} | '
            f'Instrucción T{tiempo}: {instruccion_actual}}}'
        )
        
        dot.node(node_id, label, fillcolor=fillcolor)
        
        # Conectar con flecha al siguiente dron
        if actual.siguiente is not None:
            next_id = f'dron_{indice + 1}'
            dot.edge(node_id, next_id)
        
        actual = actual.siguiente
        indice += 1
    
    return dot

def generar_grafo_instrucciones_dron(dron, tiempo_maximo):
    """
    Genera un grafo de las instrucciones de un dron específico hasta el tiempo máximo
    """
    dot = graphviz.Digraph(comment=f'Instrucciones Dron {dron.nombre}')
    
    dot.attr(rankdir='TB')  # Vertical
    dot.attr('node', shape='box', style='filled')
    dot.attr('edge', arrowhead='vee')
    
    dot.attr(label=f'Instrucciones Dron {dron.nombre} - Hasta tiempo: {tiempo_maximo}')
    dot.attr(labelloc='t')
    
    # Nodo de información del dron
    dot.node('info', f'Dron: {dron.nombre}\nHilera: H{dron.hilera_asignada}', 
             shape='ellipse', fillcolor='lightblue')
    
    # Agregar instrucciones SOLO HASTA el tiempo máximo
    prev_node = 'info'
    for i in range(min(tiempo_maximo, len(dron.instrucciones))):
        instruccion = dron.instrucciones.obtener_en_indice(i)
        node_id = f'inst_{i}'
        
        # Color según el tipo de instrucción
        if 'Adelante' in instruccion:
            fillcolor = '#C8E6C9'  # Verde
        elif 'Atras' in instruccion:
            fillcolor = '#FFCDD2'  # Rojo
        elif 'Regar' in instruccion:
            fillcolor = '#BBDEFB'  # Azul
        elif 'Esperar' in instruccion:
            fillcolor = '#F5F5F5'  # Gris
        elif 'FIN' in instruccion:
            fillcolor = '#FFE0B2'  # Naranja
        else:
            fillcolor = '#E1BEE7'  # Morado
        
        dot.node(node_id, f'T{i+1}: {instruccion}', fillcolor=fillcolor)
        dot.edge(prev_node, node_id)
        prev_node = node_id
    
    # Si el tiempo máximo es mayor que las instrucciones, mostrar FIN
    if tiempo_maximo > len(dron.instrucciones):
        dot.node('fin', 'FIN\n(No más instrucciones)', shape='ellipse', fillcolor='orange')
        dot.edge(prev_node, 'fin')
    
    return dot