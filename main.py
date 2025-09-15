from parser_xml import cargar_configuracion

invernaderos = cargar_configuracion("entrada.xml")
print("=== INVERNADEROS CARGADOS ===")
for inv in invernaderos:
    print(f"\n{inv}")
    print(f"  Drones: {len(inv.drones)}")
    print(f"  Plantas: {len(inv.plantas)}")
    print(f"  Planes: {len(inv.planes_riego)}")