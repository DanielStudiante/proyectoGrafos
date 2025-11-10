"""
Diagnóstico: ¿Por qué no puedo viajar a Beta178?
"""
from utils.config_loader import cargar_grafo_desde_json, crear_burro_desde_json
from algorithms.dijkstra import dijkstra, obtener_estrellas_alcanzables

print("=" * 70)
print("DIAGNÓSTICO: VIAJE A BETA178")
print("=" * 70)

# Cargar configuración
grafo = cargar_grafo_desde_json()
burro = crear_burro_desde_json()

# Buscar Beta178
beta178 = None
for star_id, estrella in grafo.estrellas.items():
    if estrella.label == "Beta178":
        beta178 = estrella
        break

if not beta178:
    print("\n❌ ERROR: Beta178 no encontrada en el grafo")
    exit(1)

print(f"\n✅ Beta178 encontrada:")
print(f"   ID: {beta178.id}")
print(f"   Label: {beta178.label}")
print(f"   Posición: ({beta178.x}, {beta178.y})")
print(f"   Activa: {beta178.activa}")

# Verificar conexiones de Beta178
vertex_beta178 = grafo.get_vertex(beta178.id)
if vertex_beta178:
    print(f"\n🔗 Conexiones de Beta178:")
    if vertex_beta178.neighbors:
        for vecino, distancia in vertex_beta178.neighbors.items():
            estrella_vecina = grafo.obtener_estrella(vecino.id)
            if estrella_vecina:
                print(f"   → {estrella_vecina.label} (id={vecino.id}): {distancia} unidades")
            else:
                print(f"   → ??? (id={vecino.id}): {distancia} unidades [NO CARGADA]")
    else:
        print("   ❌ Sin conexiones")
else:
    print("\n❌ ERROR: Vértice de Beta178 no encontrado")

# Verificar desde Alpha1
print("\n" + "=" * 70)
print("DESDE ALPHA1 (posición inicial)")
print("=" * 70)

alpha1 = grafo.obtener_estrella(1)
if alpha1:
    print(f"\n📍 Alpha1:")
    print(f"   ID: {alpha1.id}")
    print(f"   Energía del burro: {burro.donkey_energy}")
    
    # Usar Dijkstra
    resultado = dijkstra(grafo, 1, beta178.id)
    
    if resultado and resultado['camino']:
        distancia = resultado['distancias'][beta178.id]
        camino = resultado['camino']
        
        print(f"\n✅ CAMINO ENCONTRADO:")
        print(f"   Distancia total: {distancia} unidades")
        print(f"   Energía necesaria: {distancia}")
        print(f"   Energía disponible: {burro.donkey_energy}")
        print(f"   ¿Alcanzable?: {'✅ SÍ' if distancia <= burro.donkey_energy else '❌ NO'}")
        
        if distancia > burro.donkey_energy:
            print(f"\n💡 PROBLEMA: Necesitas {distancia - burro.donkey_energy:.2f} más de energía")
        
        print(f"\n🗺️ Ruta:")
        for i, star_id in enumerate(camino):
            estrella = grafo.obtener_estrella(star_id)
            print(f"   {i+1}. {estrella.label} (id={star_id})")
    else:
        print(f"\n❌ NO HAY CAMINO desde Alpha1 a Beta178")

# Verificar estrellas alcanzables
print("\n" + "=" * 70)
print("ESTRELLAS ALCANZABLES DESDE ALPHA1")
print("=" * 70)

alcanzables = obtener_estrellas_alcanzables(grafo, 1, burro.donkey_energy)

print(f"\n✅ {len(alcanzables)} estrellas alcanzables:\n")
beta178_alcanzable = False

for opcion in alcanzables:
    estrella = grafo.obtener_estrella(opcion['id'])
    if not estrella:
        continue
    
    es_beta178 = (estrella.id == beta178.id)
    if es_beta178:
        beta178_alcanzable = True
        print(f"🎯 {estrella.label} (id={estrella.id})")
    else:
        print(f"   {estrella.label} (id={estrella.id})")
    
    print(f"      Distancia: {opcion['distancia']:.2f}")
    print(f"      Camino: {' → '.join([grafo.obtener_estrella(id).label for id in opcion['camino'] if grafo.obtener_estrella(id)])}")
    print()

if not beta178_alcanzable:
    print("❌ Beta178 NO ESTÁ ALCANZABLE con la energía actual")

# Verificar todas las estrellas del grafo
print("\n" + "=" * 70)
print("TODAS LAS ESTRELLAS EN EL GRAFO")
print("=" * 70)

print(f"\nTotal de estrellas: {len(grafo.estrellas)}\n")
for star_id, estrella in sorted(grafo.estrellas.items()):
    vertex = grafo.get_vertex(star_id)
    num_vecinos = len(vertex.neighbors) if vertex else 0
    print(f"  {estrella.label:15} (id={star_id:2}) - {num_vecinos} vecinos")
