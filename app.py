from flask import Flask, render_template, request, jsonify, send_file
import os
from parser_xml import cargar_configuracion
from simulador_riego import generar_instrucciones_para_plan
from generador_grafos import generar_grafo_lista_plan, generar_grafo_lista_drones

app = Flask(__name__)

invernaderos_actuales = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cargar_archivo', methods=['POST'])
def cargar_archivo():
    global invernaderos_actuales

    if 'archivo' not in request.files:
        return jsonify({'error': 'No se seleccionó archivo'}), 400

    archivo = request.files['archivo']
    if archivo.filename == '':
        return jsonify({'error': 'No se seleccionó archivo'}), 400

    if archivo and archivo.filename.endswith('.xml'):
        try:
            if not os.path.exists('uploads'):
                os.makedirs('uploads')
            archivo_path = os.path.join('uploads', archivo.filename)
            archivo.save(archivo_path)

            invernaderos_actuales = cargar_configuracion(archivo_path)

            datos_invernaderos = []
            for inv in invernaderos_actuales:
                planes = [{'nombre': plan.nombre} for plan in inv.planes_riego]
                datos_invernaderos.append({
                    'nombre': inv.nombre,
                    'planes': planes
                })
            return jsonify({
                'success': True,
                'invernaderos': datos_invernaderos
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return jsonify({'error': 'Archivo no válido'}), 400

@app.route('/simular_plan', methods=['POST'])
def simular_plan():
    global invernaderos_actuales

    if invernaderos_actuales is None:
        return jsonify({'error': 'No hay invernaderos cargados'}), 400

    data = request.json
    nombre_invernadero = data.get('invernadero')
    nombre_plan = data.get('plan')

    invernadero_obj = None
    for inv in invernaderos_actuales:
        if inv.nombre == nombre_invernadero:
            invernadero_obj = inv
            break

    if invernadero_obj is None:
        return jsonify({'error': 'Invernadero no encontrado'}), 404

    try:
        tiempo_optimo = generar_instrucciones_para_plan(invernadero_obj, nombre_plan)

        estadisticas = {
            'tiempo_optimo': tiempo_optimo,
            'drones': []
        }

        total_agua = 0
        total_fert = 0

        for dron in invernadero_obj.drones:
            estadisticas['drones'].append({
                'nombre': dron.nombre,
                'agua': dron.litros_agua_utilizados,
                'fertilizante': dron.gramos_fertilizante_utilizados
            })
            total_agua += dron.litros_agua_utilizados
            total_fert += dron.gramos_fertilizante_utilizados

        estadisticas['total_agua'] = total_agua
        estadisticas['total_fertilizante'] = total_fert

        return jsonify({
            'success': True,
            'estadisticas': estadisticas
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/generar_reporte_html', methods=['POST'])
def generar_reporte_html():
    global invernaderos_actuales

    if invernaderos_actuales is None:
        return jsonify({'error': 'No hay invernaderos cargados'}), 400

    data = request.json
    nombre_invernadero = data.get('invernadero')
    nombre_plan = data.get('plan')

    try:
        invernadero_obj = None
        for inv in invernaderos_actuales:
            if inv.nombre == nombre_invernadero:
                invernadero_obj = inv
                break

        if invernadero_obj is None:
            return jsonify({'error': 'Invernadero no encontrado'}), 404

        from estructuras.lista_enlazada_simple import ListaEnlazadaSimple
        invernaderos_temporal = ListaEnlazadaSimple()

        from modelos.invernadero import Invernadero
        invernadero_filtrado = Invernadero(
            invernadero_obj.nombre,
            invernadero_obj.numero_hileras,
            invernadero_obj.plantas_x_hilera
        )

        for planta in invernadero_obj.plantas:
            invernadero_filtrado.agregar_planta(planta)

        for dron in invernadero_obj.drones:
            invernadero_filtrado.agregar_dron(dron)

        for plan in invernadero_obj.planes_riego:
            if plan.nombre == nombre_plan:
                invernadero_filtrado.agregar_plan_riego(plan)
                break

        invernaderos_temporal.agregar_al_final(invernadero_filtrado)

        from generador_html import generar_reporte_html as gen_html
        gen_html(invernaderos_temporal, "ReporteInvernaderos.html")

        return jsonify({'success': True, 'archivo': 'ReporteInvernaderos.html'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/descargar_reporte')
def descargar_reporte():
    return send_file('ReporteInvernaderos.html', as_attachment=True)

@app.route('/generar_salida_xml', methods=['POST'])
def generar_salida_xml():
    global invernaderos_actuales

    if invernaderos_actuales is None:
        return jsonify({'error': 'No hay invernaderos cargados'}), 400

    try:
        from generador_xml import generar_salida_xml as gen_xml
        gen_xml(invernaderos_actuales)
        return jsonify({'success': True, 'archivo': 'salida.xml'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/descargar_xml')
def descargar_xml():
    return send_file('salida.xml', as_attachment=True)

@app.route('/generar_grafo', methods=['POST'])
def generar_grafo():
    global invernaderos_actuales

    if invernaderos_actuales is None:
        return jsonify({'error': 'No hay invernaderos cargados'}), 400

    data = request.json
    tiempo = data.get('tiempo', 1)
    tipo_grafo = data.get('tipo', 'plan')
    invernadero_nombre = data.get('invernadero')
    plan_nombre = data.get('plan')

    try:
        invernadero = None
        for inv in invernaderos_actuales:
            if inv.nombre == invernadero_nombre:
                invernadero = inv
                break

        if invernadero is None:
            return jsonify({'error': 'Invernadero no encontrado'}), 404

        if tipo_grafo == 'plan':
            plan = None
            for p in invernadero.planes_riego:
                if p.nombre == plan_nombre:
                    plan = p
                    break
            
            if plan is None:
                return jsonify({'error': 'Plan no encontrado'}), 404
                
            dot = generar_grafo_lista_plan(plan, tiempo)
            nombre_archivo = f'grafo_plan_{plan_nombre}_t{tiempo}'
        else:
            dot = generar_grafo_lista_drones(invernadero.drones, tiempo)
            nombre_archivo = f'grafo_drones_{invernadero_nombre}_t{tiempo}'

        if not os.path.exists('static/graficos'):
            os.makedirs('static/graficos')
        dot.render(f'static/graficos/{nombre_archivo}', format='png', cleanup=True)

        return jsonify({
            'success': True,
            'imagen': f'/static/graficos/{nombre_archivo}.png',
            'tiempo': tiempo,
            'tipo': tipo_grafo
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)