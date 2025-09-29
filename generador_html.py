def generar_reporte_html(lista_invernaderos, ruta_salida="ReporteInvernaderos.html"):
    """
    Genera un reporte HTML con la información de todos los invernaderos y planes.
    """
    
    html = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Reporte GuateRiegos 2.0</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { 
            background: linear-gradient(135deg, #e3f2fd 0%, #f3e5f5 100%);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .header { 
            background: linear-gradient(120deg, #1565C0, #42A5F5);
            color: white; 
            padding: 30px 0;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }
        .header h1 {
            font-weight: 300;
            margin: 0;
            font-size: 2.5rem;
        }
        .card { 
            border: none;
            border-radius: 15px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
            margin-bottom: 30px;
            overflow: hidden;
        }
        .card-header {
            background: linear-gradient(120deg, #2E7D32, #4CAF50);
            color: white;
            padding: 20px;
            border-bottom: none;
        }
        .card-header h2 {
            margin: 0;
            font-weight: 400;
        }
        .plan-card {
            background: white;
            border-radius: 12px;
            padding: 0;
            margin-bottom: 25px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
            border-left: 5px solid #42A5F5;
        }
        .plan-header {
            background: linear-gradient(120deg, #42A5F5, #64B5F6);
            color: white;
            padding: 20px;
            margin: 0;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
        .stat-card {
            background: linear-gradient(135deg, #E8F5E8, #F1F8E9);
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            border-left: 4px solid #4CAF50;
        }
        .stat-number {
            font-size: 2rem;
            font-weight: bold;
            color: #2E7D32;
            margin-bottom: 5px;
        }
        .stat-label {
            color: #555;
            font-size: 0.9rem;
        }
        .table-custom {
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        }
        .table-custom thead th {
            background: linear-gradient(120deg, #5C6BC0, #7986CB);
            color: white;
            border: none;
            padding: 15px;
            font-weight: 500;
        }
        .table-custom tbody td {
            padding: 12px 15px;
            border-color: #e0e0e0;
        }
        .table-hover tbody tr:hover {
            background-color: #f8f9fa;
            transform: translateY(-1px);
            transition: all 0.2s;
        }
        .efficiency-table {
            background: linear-gradient(135deg, #E3F2FD, #E1F5FE);
        }
        .efficiency-table thead th {
            background: linear-gradient(120deg, #0288D1, #03A9F4);
        }
        .section-title {
            color: #1565C0;
            margin: 25px 0 15px 0;
            padding-bottom: 10px;
            border-bottom: 2px solid #E3F2FD;
            font-weight: 500;
        }
        .badge-custom {
            background: linear-gradient(120deg, #FF9800, #FFB74D);
            padding: 8px 15px;
            border-radius: 20px;
            font-weight: 500;
            color: white;
        }
        .instructions-table {
            font-size: 0.9rem;
        }
        .instructions-table td {
            word-break: break-word;
        }
        .dron-card {
            transition: transform 0.2s;
        }
        .dron-card:hover {
            transform: translateY(-2px);
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="container">
            <h1>Sistema de Riego Automatizado</h1>
            <p class="lead mb-0">GuateRiegos 2.0 - Reporte de Eficiencia</p>
        </div>
    </div>
    <div class="container">"""

    # Iterar sobre invernaderos
    for invernadero in lista_invernaderos:
        html += f"""
        <div class="card">
            <div class="card-header">
                <h2>{invernadero.nombre}</h2>
                <p class="mb-0">Configuración: {invernadero.numero_hileras} hileras × {invernadero.plantas_x_hilera} plantas</p>
            </div>
            <div class="card-body">"""
        
        # Para cada plan - SIMULAR CADA UNO POR SEPARADO
        for plan in invernadero.planes_riego:
            html += f"""
                <div class="plan-card">
                    <div class="plan-header">
                        <h3 class="mb-0">Plan: {plan.nombre}</h3>
                    </div>
                    <div class="card-body">"""
            
            # SIMULAR ESTE PLAN ESPECÍFICO para obtener sus datos
            from simulador_riego import generar_instrucciones_para_plan
            tiempo_optimo = generar_instrucciones_para_plan(invernadero, plan.nombre)
            
            # Calcular estadísticas para ESTE plan
            total_agua = 0
            total_fert = 0
            for dron in invernadero.drones:
                total_agua += dron.litros_agua_utilizados
                total_fert += dron.gramos_fertilizante_utilizados
            
            # --- ESTADÍSTICAS PRINCIPALES ---
            html += f"""
                        <div class="stats-grid">
                            <div class="stat-card">
                                <div class="stat-number">{tiempo_optimo}s</div>
                                <div class="stat-label">Tiempo Óptimo</div>
                            </div>
                            <div class="stat-card">
                                <div class="stat-number">{total_agua}L</div>
                                <div class="stat-label">Agua Total</div>
                            </div>
                            <div class="stat-card">
                                <div class="stat-number">{total_fert}g</div>
                                <div class="stat-label">Fertilizante Total</div>
                            </div>
                            <div class="stat-card">
                                <div class="stat-number">{len(plan.secuencia)}</div>
                                <div class="stat-label">Plantas Regadas</div>
                            </div>
                        </div>"""
            
            # --- EFICIENCIA POR DRON ---
            html += """
                        <h4 class="section-title">Eficiencia por Dron</h4>
                        <table class='table table-success table-custom efficiency-table'>
                            <thead>
                                <tr>
                                    <th>Dron</th>
                                    <th>Hilera</th>
                                    <th>Agua (L)</th>
                                    <th>Fertilizante (g)</th>
                                    <th>Estado</th>
                                </tr>
                            </thead>
                            <tbody>"""
            
            for dron in invernadero.drones:
                estado = "Activo" if dron.litros_agua_utilizados > 0 else "Inactivo"
                html += f"""
                                <tr>
                                    <td><strong>{dron.nombre}</strong></td>
                                    <td>H{dron.hilera_asignada}</td>
                                    <td>{dron.litros_agua_utilizados}</td>
                                    <td>{dron.gramos_fertilizante_utilizados}</td>
                                    <td><span class="badge-custom">{estado}</span></td>
                                </tr>"""
            
            html += """
                            </tbody>
                        </table>"""
            
            # --- ASIGNACIÓN DE DRONES ---
            html += """
                        <h4 class="section-title">Asignación de Drones</h4>
                        <div class="row">"""
            
            for dron in invernadero.drones:
                html += f"""
                            <div class="col-md-4 mb-3">
                                <div class="card border-primary dron-card">
                                    <div class="card-body text-center">
                                        <h5 class="card-title">{dron.nombre}</h5>
                                        <p class="card-text">
                                            <strong>Hilera:</strong> H{dron.hilera_asignada}<br>
                                            <strong>Posición Actual:</strong> P{dron.posicion_actual}<br>
                                            <strong>Instrucciones:</strong> {len(dron.instrucciones)}
                                        </p>
                                    </div>
                                </div>
                            </div>"""
            
            html += """
                        </div>"""
            
            # --- INSTRUCCIONES POR TIEMPO ---
            html += """
                        <h4 class="section-title">Instrucciones por Segundo</h4>
                        <div class="table-responsive">
                            <table class='table table-bordered table-custom instructions-table'>
                                <thead>
                                    <tr>
                                        <th>Segundo</th>"""
            
            # Encabezados de drones
            for dron in invernadero.drones:
                html += f"<th>{dron.nombre}</th>"
            
            html += """
                                    </tr>
                                </thead>
                                <tbody>"""
            
            # Filas de instrucciones
            if not invernadero.drones.esta_vacia():
                primer_dron = invernadero.drones.obtener_en_indice(0)
                max_segundos = len(primer_dron.instrucciones)
                
                for t in range(max_segundos):
                    html += f"""
                                    <tr>
                                        <td><strong>{t + 1}</strong></td>"""
                    
                    for dron in invernadero.drones:
                        accion = dron.obtener_instruccion_en_segundo(t)
                        html += f"<td>{accion}</td>"
                    
                    html += """
                                    </tr>"""
            
            html += """
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>"""  # Cierre de plan-card
        
        html += """
            </div>
        </div>"""
    
    html += """
        <footer class="text-center mt-5 mb-4">
            <p class="text-muted">Sistema GuateRiegos 2.0 • Generado automáticamente</p>
        </footer>
    </div>
</body>
</html>"""

    # Guardar el archivo
    with open(ruta_salida, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"Reporte HTML generado: {ruta_salida}")