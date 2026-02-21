from mesa import Mesa

NUM_FILOSOFOS = 5
DURACION_SIMULACION = 300
TIEMPO_COMER_BASE = 0.3
TIEMPO_PENSAR_BASE = 0.3


def main():
    print("\n=== Filósofos Comensales - Peterson Lock + Filósofo Zurdo ===")
    print(f"Filósofos: {NUM_FILOSOFOS} | Duración: {DURACION_SIMULACION}s\n")
    
    mesa = Mesa(NUM_FILOSOFOS, DURACION_SIMULACION, TIEMPO_COMER_BASE, TIEMPO_PENSAR_BASE)
    mesa.iniciar()
    mesa.esperar()
    
    print("\n--- Finalizando ---")
    mesa.detener()
    
    stats = mesa.obtener_estadisticas()
    
    print("\n=== RESULTADOS ===")
    for i in range(NUM_FILOSOFOS):
        comidas = stats['conteo_comidas'][i]
        tipo = "ZURDO" if i == 0 else "DIESTRO"
        print(f"Filósofo {i} ({tipo}): {comidas} comidas")
    
    print(f"\nTotal: {stats['total_comidas']} | Promedio: {stats['promedio']:.1f} | Min: {stats['min_comidas']} | Max: {stats['max_comidas']}")
    print("Sin deadlock\n")

main()
