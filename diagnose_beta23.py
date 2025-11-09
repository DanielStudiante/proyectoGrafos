"""
Verificación de por qué no puedes viajar a Beta23
"""
from utils.config_loader import cargar_grafo_desde_json, crear_burro_desde_json
from algorithms.dijkstra import obtener_estrellas_alcanzables

print("=" * 60)
print("¿POR QUÉ NO PUEDO VIAJAR A BETA23?")
print("=" * 60)

# Cargar configuración
grafo = cargar_grafo_desde_json()
burro = crear_burro_desde_json()

print(f"\n🐴 Estado del Burro:")
print(f"   Energía: {burro.donkey_energy}")
print(f"   Salud: {burro.health}")

# Buscar estrellas alcanzables desde Alpha1
print(f"\n📍 Posición actual: Alpha1 (id=1)")
print(f"\n🔍 Buscando estrellas alcanzables con {burro.donkey_energy} de energía...")

alcanzables = obtener_estrellas_alcanzables(
    grafo,
    1,  # Alpha1
    burro.donkey_energy
)

print(f"\n✅ Encontradas {len(alcanzables)} estrellas alcanzables:")
print("=" * 60)

beta23_encontrada = False

for opcion in alcanzables:
    estrella = grafo.obtener_estrella(opcion['id'])
    
    if not estrella:
        continue  # Saltar estrellas no cargadas
    
    es_beta23 = estrella.id == 2
    
    if es_beta23:
        beta23_encontrada = True
        print(f"\n🎯 ✅ BETA23 ENCONTRADA!")
    else:
        print(f"\n• {estrella.label} (id={estrella.id})")
    
    print(f"  Distancia: {opcion['distancia']:.2f} unidades")
    print(f"  Energía necesaria: {opcion['distancia']:.2f}")
    print(f"  Energía restante: {opcion['energia_restante']:.2f}")
    print(f"  Camino: {' → '.join([grafo.obtener_estrella(id).label for id in opcion['camino']])}")

print("\n" + "=" * 60)

if not beta23_encontrada:
    print("❌ BETA23 NO ESTÁ EN LA LISTA DE ALCANZABLES")
    print("\n🔍 Diagnóstico:")
    
    # Verificar distancia
    from algorithms.dijkstra import dijkstra
    resultado = dijkstra(grafo, 1, 2)
    
    distancia_beta23 = resultado['distancias'][2]
    print(f"   • Distancia a Beta23: {distancia_beta23}")
    print(f"   • Energía del burro: {burro.donkey_energy}")
    print(f"   • ¿Alcanzable?: {'✅ SÍ' if distancia_beta23 <= burro.donkey_energy else '❌ NO'}")
    
    if distancia_beta23 > burro.donkey_energy:
        print(f"\n💡 SOLUCIÓN: Necesitas {distancia_beta23 - burro.donkey_energy:.2f} más de energía")
        print(f"   Come pasto para recuperar energía.")
else:
    print("✅ BETA23 SÍ ESTÁ ALCANZABLE")
    print("\n💡 Si no puedes viajar en el juego, puede ser un problema de:")
    print("   1. La interfaz no actualiza la lista correctamente")
    print("   2. El burro está en otra posición (no en Alpha1)")
    print("   3. Beta23 está bloqueada por alguna razón")
