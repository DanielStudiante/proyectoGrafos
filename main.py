"""
Sistema principal de simulacion del burro cientifico.
Responsabilidad: Interfaz de terminal para el usuario.
"""

from utils.config_loader import cargar_grafo_desde_json, crear_burro_desde_json
from backend.constellation import GrafoConstelaciones
from backend.simulator import SimuladorViaje


def configurar_efectos_estrella(grafo):
    """Permite al cientifico configurar los efectos de investigacion."""
    print("\n" + "="*70)
    print("CONFIGURACION DE EFECTOS DE INVESTIGACION")
    print("="*70)
    
    # Mostrar estrellas disponibles
    print("\nEstrellas disponibles:")
    for star_id, estrella in grafo.estrellas.items():
        health_sign = "+" if estrella.health_impact >= 0 else ""
        life_sign = "+" if estrella.life_time_impact >= 0 else ""
        print(f"  {star_id}. {estrella.label} - Salud: {health_sign}{estrella.health_impact:.1f}, Vida: {life_sign}{estrella.life_time_impact:.1f} años")
    
    print("\nDeseas modificar los efectos? (s/n): ", end="")
    if input().strip().lower() != 's':
        return
    
    while True:
        try:
            print("\nIngresa el ID de la estrella (0 para terminar): ", end="")
            star_id = int(input().strip())
            
            if star_id == 0:
                break
            
            estrella = grafo.obtener_estrella(star_id)
            if not estrella:
                print(f"Estrella {star_id} no encontrada")
                continue
            
            print(f"\nConfigurando: {estrella.label}")
            print(f"   Valores actuales - Salud: {estrella.health_impact:+.1f}, Vida: {estrella.life_time_impact:+.1f}")
            
            health = input("   Nuevo impacto en salud (Enter para mantener): ").strip()
            if health:
                estrella.set_health_impact(float(health))
            
            life = input("   Nuevo impacto en vida (Enter para mantener): ").strip()
            if life:
                estrella.set_life_time_impact(float(life))
            
            print(f"   Actualizado: Salud: {estrella.health_impact:+.1f}, Vida: {estrella.life_time_impact:+.1f}")
        
        except ValueError:
            print("Valor invalido")
        except KeyboardInterrupt:
            break
    
    print("\nConfiguracion completada")


def main():
    """Funcion principal del simulador."""
    print("="*70)
    print("SIMULADOR DEL BURRO CIENTIFICO")
    print("="*70)
    
    # 1. Cargar datos
    print("\nCargando configuracion...")
    grafo = cargar_grafo_desde_json()
    burro = crear_burro_desde_json()
    print(f"Cargado: {len(grafo.estrellas)} estrellas, Burro: {burro.name}")
    
    # 2. Configurar efectos (OPCIONAL)
    configurar_efectos_estrella(grafo)
    
    # 3. Iniciar simulacion
    print("\n" + "="*70)
    print("INICIO DE LA SIMULACION")
    print("="*70)
    
    posicion_inicial = 1
    simulador = SimuladorViaje(grafo, burro, posicion_inicial)
    
    # Loop de simulacion
    while burro.alive:
        opciones = simulador.mostrar_opciones()
        
        if not opciones:
            print("\nIntenta comer pasto o has llegado al limite.")
            print("Comer pasto? (s/n): ", end="")
            if input().strip().lower() == 's':
                simulador.comer_pasto(5)
                continue
            else:
                break
        
        print("\nOpciones:")
        print("   Numero = Viajar a esa estrella")
        print("   'c' = Comer pasto")
        print("   'r' = Ver resumen")
        print("   'q' = Salir")
        
        accion = input("\nAccion: ").strip().lower()
        
        if accion == 'q':
            break
        elif accion == 'c':
            simulador.comer_pasto(5)
        elif accion == 'r':
            resumen = simulador.obtener_resumen_viaje()
            print(f"\nRESUMEN:")
            print(f"   Estrellas visitadas: {resumen['estrellas_visitadas']}")
            print(f"   Distancia total: {resumen['distancia_total']:.2f} ly")
            print(f"   Salud: {resumen['salud']}")
        elif accion.isdigit():
            idx = int(accion) - 1
            if 0 <= idx < len(opciones):
                destino = opciones[idx]['id']
                simulador.viajar_a(destino)
            else:
                print("Opcion invalida")
        else:
            print("Comando no reconocido")
    
    # Resumen final
    print("\n" + "="*70)
    print("FIN DE LA SIMULACION")
    print("="*70)
    resumen = simulador.obtener_resumen_viaje()
    print(f"Estrellas visitadas: {resumen['estrellas_visitadas']}")
    print(f"Distancia total: {resumen['distancia_total']:.2f} ly")
    print(f"Estado: {'VIVO' if resumen['vivo'] else 'MUERTO'}")
    print(f"Salud final: {resumen['salud']}")


if __name__ == "__main__":
    main()
