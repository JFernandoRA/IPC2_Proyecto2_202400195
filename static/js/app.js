function cargarArchivo() {
    const archivoInput = document.getElementById('archivoXml');
    const archivo = archivoInput.files[0];
    
    if (!archivo) {
        alert('Por favor selecciona un archivo XML');
        return;
    }
    
    const formData = new FormData();
    formData.append('archivo', archivo);
    
    fetch('/cargar_archivo', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            llenarSelectores(data.invernaderos);
            mostrarMensaje('Archivo cargado exitosamente', 'success');
        } else {
            mostrarMensaje('Error: ' + data.error, 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        mostrarMensaje('Error al cargar el archivo', 'error');
    });
}

function llenarSelectores(invernaderos) {
    const selectInvernadero = document.getElementById('selectInvernadero');
    const selectPlan = document.getElementById('selectPlan');
    
    // Limpiar selectores
    selectInvernadero.innerHTML = '<option>Seleccionar invernadero</option>';
    selectPlan.innerHTML = '<option>Seleccionar plan</option>';
    
    // Llenar invernaderos
    invernaderos.forEach(inv => {
        const option = document.createElement('option');
        option.value = inv.nombre;
        option.textContent = inv.nombre;
        selectInvernadero.appendChild(option);
    });
    
    // Habilitar selectores
    selectInvernadero.disabled = false;
    
    // Event listener para cuando seleccionen invernadero
    selectInvernadero.addEventListener('change', function() {
        const invernaderoSeleccionado = invernaderos.find(inv => inv.nombre === this.value);
        llenarPlanes(invernaderoSeleccionado.planes);
    });
}

function llenarPlanes(planes) {
    const selectPlan = document.getElementById('selectPlan');
    const btnSimular = document.querySelector('button[onclick="simularPlan()"]');
    
    // Limpiar planes
    selectPlan.innerHTML = '<option>Seleccionar plan</option>';
    
    // Llenar planes
    planes.forEach(plan => {
        const option = document.createElement('option');
        option.value = plan.nombre;
        option.textContent = plan.nombre;
        selectPlan.appendChild(option);
    });
    
    // Habilitar selector de planes
    selectPlan.disabled = false;

    selectPlan.addEventListener('change', function() {
        btnSimular.disabled = (this.value === 'Seleccionar plan');
    });
}

function simularPlan() {
    const selectInvernadero = document.getElementById('selectInvernadero');
    const selectPlan = document.getElementById('selectPlan');

    if (selectInvernadero.value === 'Seleccionar invernadero' || 
        selectPlan.value === 'Seleccionar plan') {
        alert('Por favor selecciona un invernadero y un plan');
        return;
    }

    const datos = {
        invernadero: selectInvernadero.value,
        plan: selectPlan.value
    };
    
    fetch('/simular_plan', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(datos)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            mostrarResultados(data.estadisticas);
        } else {
            mostrarMensaje('Error: ' + data.error, 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        mostrarMensaje('Error al simular el plan', 'error');
    });
}

function mostrarResultados(estadisticas) {
    const resultadosDiv = document.getElementById('resultados');
    
    let html = `
        <div class="card">
            <div class="card-header">
                <h5>Resultados de la Simulación</h5>
            </div>
            <div class="card-body">
                <p><strong>Tiempo óptimo:</strong> ${estadisticas.tiempo_optimo} segundos</p>
                <p><strong>Agua total:</strong> ${estadisticas.total_agua} litros</p>
                <p><strong>Fertilizante total:</strong> ${estadisticas.total_fertilizante} gramos</p>
                
                <h6>Consumo por Dron:</h6>
                <table class="table table-sm">
                    <thead>
                        <tr>
                            <th>Dron</th>
                            <th>Agua (L)</th>
                            <th>Fertilizante (g)</th>
                        </tr>
                    </thead>
                    <tbody>
    `;
    
    estadisticas.drones.forEach(dron => {
        html += `
            <tr>
                <td>${dron.nombre}</td>
                <td>${dron.agua}</td>
                <td>${dron.fertilizante}</td>
            </tr>
        `;
    });
    
    html += `
                    </tbody>
                </table>
                
                <button onclick="generarReporteHTML()" class="btn btn-success">Generar Reporte HTML</button>
                <button onclick="generarSalidaXML()" class="btn btn-info">Generar Salida XML</button>
            </div>
        </div>
    `;
    
    resultadosDiv.innerHTML = html;
    resultadosDiv.style.display = 'block';
}

function generarReporteHTML() {
    const selectInvernadero = document.getElementById('selectInvernadero');
    const selectPlan = document.getElementById('selectPlan');
    
    const datos = {
        invernadero: selectInvernadero.value,
        plan: selectPlan.value
    };
    
    fetch('/generar_reporte_html', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(datos)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            mostrarMensaje('Reporte HTML generado exitosamente', 'success');
            // Descargar automáticamente
            window.open('/descargar_reporte', '_blank');
        } else {
            mostrarMensaje('Error: ' + data.error, 'error');
        }
    });
}

function generarSalidaXML() {
    fetch('/generar_salida_xml', {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            mostrarMensaje('Archivo XML generado exitosamente', 'success');
            // Descargar automáticamente
            window.open('/descargar_xml', '_blank');
        } else {
            mostrarMensaje('Error: ' + data.error, 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        mostrarMensaje('Error al generar XML', 'error');
    });
}

function mostrarMensaje(mensaje, tipo) {
    // Crear un toast o alerta básica
    alert(mensaje); // Por ahora usamos alert, luego podemos hacerlo más fancy
}

function generarGrafo() {
    const inputTiempo = document.getElementById('inputTiempo');
    const selectTipo = document.getElementById('selectTipoGrafo');
    const selectInvernadero = document.getElementById('selectInvernadero');
    const selectPlan = document.getElementById('selectPlan');

    const tiempo = parseInt(inputTiempo.value);
    const tipo = selectTipo.value;
    const invernadero = selectInvernadero.value;
    const plan = selectPlan.value;

    if (!tiempo || tiempo < 1) {
        mostrarMensaje('Por favor ingresa un tiempo válido', 'error');
        return;
    }

    if (invernadero === 'Seleccionar invernadero' || plan === 'Seleccionar plan') {
        mostrarMensaje('Por favor selecciona un invernadero y un plan primero', 'error');
        return;
    }

    const datos = {
        tiempo: tiempo,
        tipo: tipo,
        invernadero: invernadero,
        plan: plan
    };

    fetch('/generar_grafo', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(datos)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const tipoTexto = data.tipo === 'plan' ? 'Plan de Riego' : 'Lista de Drones';
            mostrarGrafico(data.imagen, data.tiempo, tipoTexto);
        } else {
            mostrarMensaje('Error: ' + data.error, 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        mostrarMensaje('Error al generar el gráfico', 'error');
    });
}

function mostrarGrafico(urlImagen, tiempo, tipo) {
    const container = document.getElementById('graficoContainer');
    const imagen = document.getElementById('graficoImagen');
    const info = document.getElementById('graficoInfo');
    
    imagen.src = urlImagen + '?t=' + new Date().getTime();
    info.textContent = `${tipo} - Estado en el segundo ${tiempo}`;
    container.style.display = 'block';
    container.scrollIntoView({ behavior: 'smooth' });
}

function mostrarAyuda() {
    const modal = new bootstrap.Modal(document.getElementById('modalAyuda'));
    modal.show();
}