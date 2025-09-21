from parser_xml import cargar_configuracion
from parser_xml import cargar_configuracion
from simulador_riego import generar_instrucciones_para_plan

def main():
    invernaderos = cargar_configuracion("entrada.xml")

    print("=== INVERNADEROS CARGADOS ===")
    for inv in invernaderos:
        print(f"\n{inv}")
        print(f"  Drones: {len(inv.drones)}")
        print(f"  Plantas: {len(inv.plantas)}")
        print(f"  Planes: {len(inv.planes_riego)}")

        for plan in inv.planes_riego:
            print(f"\n--- Generando instrucciones para el plan: {plan.nombre} ---")
            tiempo_optimo = generar_instrucciones_para_plan(inv, plan.nombre)
            print(f"  Tiempo óptimo calculado: {tiempo_optimo} segundos")
            print("  Instrucciones generadas (primeras 10 por dron):")
            for dron in inv.drones:
                print(f"    {dron.nombre}: ", end="")
                instrucciones_mostrar = []
                contador = 0
                for instruccion in dron.instrucciones:
                    if contador >= 10:
                        instrucciones_mostrar.append("...")
                        break
                    instrucciones_mostrar.append(instruccion)
                    contador += 1
                print(", ".join(instrucciones_mostrar))

if __name__ == "__main__":
    main()