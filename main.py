from parser_xml import cargar_configuracion
from simulador_riego import generar_instrucciones_para_plan
from generador_html import generar_reporte_html
from generador_xml import generar_salida_xml, generar_salida_xml_alternativo
import os

def main():
    try:
        archivo_entrada = "entrada3.xml"
        
        if not os.path.exists(archivo_entrada):
            print(f"ERROR: No se encuentra el archivo {archivo_entrada}")
            return
        
        print(f"Archivo encontrado: {archivo_entrada}")
        invernaderos = cargar_configuracion(archivo_entrada)
    
        print("Archivos generados:")
        print("  - ReporteInvernaderos.html")
        print("  - salida.xml") 
        print("  - salida_alternativa.xml")
        
    except Exception as e:
        print(f"Error durante la ejecución: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()