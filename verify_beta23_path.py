"""
Verificación de caminos a Beta23
"""
from utils.config_loader import cargar_grafo_desde_json
from algorithms.dijkstra import dijkstra

print("=" * 60)
print("VERIFICACIÓN DE CONEXIONES A BETA23")
print("=" * 60)

# Cargar grafo
grafo = cargar_grafo_desde_json()

# Obtener estrellas
alpha1 = grafo.obtener_estrella(1)
beta23 = grafo.obtener_estrella(2)

if not alpha1:
    print("❌ ERROR: No se encontró Alpha1")
    exit(1)
if not beta23:
    print("❌ ERROR: No se encontró Beta23")
    exit(1)

print(f"\n✅ Alpha1 (id={alpha1.id}): {alpha1.label}")
print(f"✅ Beta23 (id={beta23.id}): {beta23.label}")

# Verificar vértices y conexiones
vertex_alpha1 = grafo.get_vertex(1)
vertex_beta23 = grafo.get_vertex(2)

if not vertex_alpha1:
    print("❌ ERROR: No se encontró vértice de Alpha1")
    exit(1)
if not vertex_beta23:
    print("❌ ERROR: No se encontró vértice de Beta23")
    exit(1)

print(f"\n📊 Análisis de conexiones:")
print(f"   Alpha1 tiene {len(vertex_alpha1.neighbors)} vecinos")
print(f"   Beta23 tiene {len(vertex_beta23.neighbors)} vecinos")

# Revisar conexiones de Alpha1
print(f"\n🔗 Vecinos de Alpha1:")
for vecino, peso in vertex_alpha1.neighbors.items():
    estrella_vecino = grafo.obtener_estrella(vecino.id)
    if estrella_vecino:
        print(f"   → {estrella_vecino.label} (id={vecino.id}): distancia={peso}")
    else:
        print(f"   → ??? (id={vecino.id}): distancia={peso} [ESTRELLA NO ENCONTRADA]")

# Revisar conexiones de Beta23
print(f"\n🔗 Vecinos de Beta23:")
for vecino, peso in vertex_beta23.neighbors.items():
    estrella_vecino = grafo.obtener_estrella(vecino.id)
    if estrella_vecino:
        print(f"   → {estrella_vecino.label} (id={vecino.id}): distancia={peso}")
    else:
        print(f"   → ??? (id={vecino.id}): distancia={peso} [ESTRELLA NO ENCONTRADA]")

# Verificar peso de la arista Alpha1 → Beta23
print(f"\n📏 Verificación de distancias:")
peso_alpha1_beta23 = vertex_alpha1.get_weight(vertex_beta23)
peso_beta23_alpha1 = vertex_beta23.get_weight(vertex_alpha1)

if peso_alpha1_beta23 is not None:
    print(f"   ✅ Alpha1 → Beta23: {peso_alpha1_beta23} unidades")
else:
    print(f"   ❌ NO HAY CONEXIÓN de Alpha1 a Beta23")

if peso_beta23_alpha1 is not None:
    print(f"   ✅ Beta23 → Alpha1: {peso_beta23_alpha1} unidades")
else:
    print(f"   ❌ NO HAY CONEXIÓN de Beta23 a Alpha1")

# Probar algoritmo de Dijkstra
print("\n" + "=" * 60)
print("PRUEBA DE DIJKSTRA: Alpha1 → Beta23")
print("=" * 60)

try:
    resultado = dijkstra(grafo, 1, 2)  # De Alpha1 a Beta23
    
    if resultado:
        distancias = resultado['distancias']
        predecesores = resultado['predecesores']
        camino = resultado['camino']
        
        print(f"\n✅ Distancia calculada por Dijkstra: {distancias.get(2, 'NO ALCANZABLE')}")
        
        if camino:
            print(f"✅ Camino encontrado: {camino}")
            ruta_labels = ' → '.join([grafo.obtener_estrella(id).label for id in camino])
            print(f"   Ruta: {ruta_labels}")
        else:
            print("❌ NO SE ENCONTRÓ CAMINO A BETA23")
            print(f"\nPredecesores: {predecesores}")
            print(f"Distancias: {distancias}")
    else:
        print("❌ Dijkstra retornó None")
        
except Exception as e:
    print(f"❌ ERROR: {e}")
    import traceback
    traceback.print_exc()

# Verificar todas las estrellas alcanzables desde Alpha1
print("\n" + "=" * 60)
print("TODAS LAS ESTRELLAS ALCANZABLES DESDE ALPHA1")
print("=" * 60)

resultado_todas = dijkstra(grafo, 1)  # Sin destino específico
if resultado_todas:
    distancias = resultado_todas['distancias']
    for star_id, distancia in sorted(distancias.items()):
        if distancia != float('inf'):
            estrella = grafo.obtener_estrella(star_id)
            if estrella:
                print(f"  {estrella.label} (id={star_id}): {distancia} unidades")
