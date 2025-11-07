import math

class Vertex:
    def __init__(self, id, x=0, y=0, constelaciones=None):
        self.id = id
        self.x = x
        self.y = y
        self.constelaciones = constelaciones if constelaciones else []
        self.adjacent = {}

    def add_neighbor(self, neighbor, weight=0):
        self.adjacent[neighbor] = weight

    def get_connections(self):
        return self.adjacent

    def get_position(self):
        return (self.x, self.y)


class Graph:
    def __init__(self):
        self.vertex_list = {}
        self.num_vertex = 0

    def add_vertex(self, id, x=0, y=0, constelaciones=None):
        self.num_vertex += 1
        new_vertex = Vertex(id, x, y, constelaciones)
        self.vertex_list[id] = new_vertex
        return new_vertex

    def get_vertex(self, id):
        return self.vertex_list.get(id)

    def add_edge(self, from_id, to_id, weight=0):
        if from_id not in self.vertex_list:
            self.add_vertex(from_id)
        if to_id not in self.vertex_list:
            self.add_vertex(to_id)
        v1 = self.vertex_list[from_id]
        v2 = self.vertex_list[to_id]
        v1.add_neighbor(v2, weight)
        v2.add_neighbor(v1, weight)

    def get_vertices(self):
        return list(self.vertex_list.keys())

    def get_edges(self):
        edges = []
        for v in self.vertex_list.values():
            for neighbor, weight in v.get_connections().items():
                edges.append((v.id, neighbor.id, weight))
        return edges
    
    

def bellman_ford(graph, start_id, verbose=False):
    """
    Algoritmo de Bellman-Ford para encontrar el camino más corto desde un vértice inicial.
    
    Args:
        graph: Instancia de Graph con vértices y aristas
        start_id: ID del vértice inicial
        verbose: Si True, imprime el proceso paso a paso
    
    Returns:
        dict: {
            'distancias': dict con las distancias mínimas desde start_id,
            'predecesores': dict con los predecesores de cada vértice,
            'tiene_ciclo_negativo': bool indicando si hay ciclo negativo
        }
        None si el vértice inicial no existe
    """
    # Validar que el vértice inicial existe
    if start_id not in graph.get_vertices():
        if verbose:
            print(f"Error: El vértice {start_id} no existe en el grafo.")
        return None

    # === Inicialización ===
    dist = {v: math.inf for v in graph.get_vertices()}
    pred = {v: None for v in graph.get_vertices()}
    dist[start_id] = 0
    pred[start_id] = start_id

    if verbose:
        print("=== Bellman-Ford: Inicialización ===")
        print(f"Vértice inicial: {start_id}")
        for v in graph.get_vertices():
            print(f"  {v}: (distancia={'∞' if dist[v]==math.inf else dist[v]}, predecesor={pred[v]})")
        print()

    # === Relajación (|V| - 1 iteraciones) ===
    num_vertices = len(graph.get_vertices())
    
    for iteration in range(num_vertices - 1):
        if verbose:
            print(f"=== Iteración {iteration + 1} ===")
        
        cambios = False

        # Recorrer todas las aristas
        for u_id in graph.get_vertices():
            vertex_u = graph.get_vertex(u_id)
            
            # Solo procesar si el vértice actual es alcanzable
            if dist[u_id] == math.inf:
                continue
            
            for vertex_v, weight in vertex_u.get_connections().items():
                v_id = vertex_v.id
                
                # Relajación: verificar si existe un camino mejor
                if dist[u_id] + weight < dist[v_id]:
                    old_dist = dist[v_id]
                    dist[v_id] = dist[u_id] + weight
                    pred[v_id] = u_id
                    cambios = True
                    
                    if verbose:
                        old_str = "∞" if old_dist == math.inf else f"{old_dist}"
                        print(f"  Actualizado {v_id}: {u_id} → {v_id} (peso={weight})")
                        print(f"    Distancia: {old_str} → {dist[v_id]}")

        if verbose:
            if cambios:
                print("\n  Estado de las etiquetas:")
                for v in graph.get_vertices():
                    dist_str = "∞" if dist[v] == math.inf else f"{dist[v]}"
                    print(f"    {v}: (distancia={dist_str}, predecesor={pred[v]})")
            else:
                print("  No hubo cambios. El algoritmo converge.")
            print()

        # Optimización: si no hubo cambios, terminar
        if not cambios:
            break

    # === Detección de ciclos negativos ===
    tiene_ciclo_negativo = False
    
    for u_id in graph.get_vertices():
        vertex_u = graph.get_vertex(u_id)
        
        if dist[u_id] == math.inf:
            continue
            
        for vertex_v, weight in vertex_u.get_connections().items():
            v_id = vertex_v.id
            
            if dist[u_id] + weight < dist[v_id]:
                tiene_ciclo_negativo = True
                if verbose:
                    print(f"⚠️  Ciclo negativo detectado: {u_id} → {v_id}")
                break
        
        if tiene_ciclo_negativo:
            break
    
    if verbose:
        if tiene_ciclo_negativo:
            print("\n❌ El grafo contiene un ciclo negativo. No hay solución óptima.")
        else:
            print("✓ No se detectaron ciclos negativos.")
        
        print("\n=== Resultado Final ===")
        print(f"Caminos más cortos desde {start_id}:")
        for v in sorted(graph.get_vertices()):
            dist_str = "∞" if dist[v] == math.inf else f"{dist[v]}"
            print(f"  {v}: distancia={dist_str}, predecesor={pred[v]}")

    return {
        'distancias': dist,
        'predecesores': pred,
        'tiene_ciclo_negativo': tiene_ciclo_negativo
    }


def obtener_camino(pred, start_id, end_id):
    """
    Reconstruye el camino desde start_id hasta end_id usando los predecesores.
    
    Args:
        pred: Diccionario de predecesores
        start_id: ID del vértice inicial
        end_id: ID del vértice destino
    
    Returns:
        list: Lista de IDs representando el camino, o None si no hay camino
    """
    if pred.get(end_id) is None:
        return None
    
    if start_id not in pred or end_id not in pred:
        return None
    
    camino = []
    actual = end_id
    
    # Prevenir ciclos infinitos
    visitados = set()
    
    while actual != start_id:
        if actual in visitados:
            return None  # Ciclo detectado
        
        camino.append(actual)
        visitados.add(actual)
        actual = pred[actual]
        
        if actual is None:
            return None
    
    camino.append(start_id)
    camino.reverse()
    
    return camino


def obtener_distancia(dist, start_id, end_id):
    """
    Obtiene la distancia más corta entre dos vértices.
    
    Args:
        dist: Diccionario de distancias
        start_id: ID del vértice inicial
        end_id: ID del vértice destino
    
    Returns:
        float: Distancia, o math.inf si no hay camino, o None si los vértices no existen
    """
    if end_id not in dist:
        return None
    
    return dist[end_id]


def imprimir_camino(graph, pred, dist, start_id, end_id):
    """
    Imprime el camino más corto desde start_id hasta end_id de forma legible.
    
    Args:
        graph: Instancia de Graph
        pred: Diccionario de predecesores
        dist: Diccionario de distancias
        start_id: ID del vértice inicial
        end_id: ID del vértice destino
    """
    camino = obtener_camino(pred, start_id, end_id)
    distancia = obtener_distancia(dist, start_id, end_id)
    
    if camino is None or distancia == math.inf:
        print(f"\nNo existe un camino desde {start_id} hasta {end_id}")
        return
    
    print(f"\n=== Camino más corto: {start_id} → {end_id} ===")
    print(f"Distancia total: {distancia}")
    print("Ruta:", " → ".join(map(str, camino)))
    
    # Mostrar detalles de cada arista
    print("\nDetalle del camino:")
    for i in range(len(camino) - 1):
        u = camino[i]
        v = camino[i + 1]
        vertex_u = graph.get_vertex(u)
        vertex_v = graph.get_vertex(v)
        weight = vertex_u.get_connections()[vertex_v]
        print(f"  {u} → {v}: peso = {weight}")


def calcular_caminos_desde_origen(graph, start_id, verbose=False):

    """
    Función de conveniencia que calcula todos los caminos desde un origen
    y retorna los resultados de forma estructurada.
    
    Args:
        graph: Instancia de Graph
        start_id: ID del vértice inicial
        verbose: Si True, imprime el proceso
    
    Returns:
        dict: {
            'origen': int,
            'alcanzables': list de IDs de vértices alcanzables,
            'no_alcanzables': list de IDs de vértices no alcanzables,
            'distancias': dict con distancias,
            'predecesores': dict con predecesores,
            'tiene_ciclo_negativo': bool
        }
        None si hay error
    """
    resultado = bellman_ford(graph, start_id, verbose)
    
    if resultado is None:
        return None
    
    alcanzables = []
    no_alcanzables = []
    
    for v_id in graph.get_vertices():
        if v_id == start_id:
            continue
        
        if resultado['distancias'][v_id] != math.inf:
            alcanzables.append(v_id)
        else:
            no_alcanzables.append(v_id)
    
    return {
        'origen': start_id,
        'alcanzables': alcanzables,
        'no_alcanzables': no_alcanzables,
        'distancias': resultado['distancias'],
        'predecesores': resultado['predecesores'],
        'tiene_ciclo_negativo': resultado['tiene_ciclo_negativo']
    }

import math
import heapq

def dijkstra(graph, start_id, end_id=None, verbose=False):
    """
    Algoritmo de Dijkstra para encontrar el camino más corto desde un vértice inicial.
    Más eficiente que Bellman-Ford para grafos sin pesos negativos.
    
    Args:
        graph: Instancia de Graph con vértices y aristas
        start_id: ID del vértice inicial
        end_id: ID del vértice destino (opcional). Si se proporciona, termina al encontrarlo
        verbose: Si True, imprime el proceso paso a paso
    
    Returns:
        dict: {
            'distancias': dict con las distancias mínimas desde start_id,
            'predecesores': dict con los predecesores de cada vértice,
            'camino': list con el camino si se especificó end_id, None si no
        }
        None si el vértice inicial no existe
    """
    # Validar que el vértice inicial existe
    if start_id not in graph.get_vertices():
        if verbose:
            print(f"Error: El vértice {start_id} no existe en el grafo.")
        return None

    # === Inicialización ===
    dist = {v: math.inf for v in graph.get_vertices()}
    pred = {v: None for v in graph.get_vertices()}
    visitados = set()
    
    dist[start_id] = 0
    pred[start_id] = start_id
    
    # Cola de prioridad: (distancia, vértice_id)
    pq = [(0, start_id)]
    
    if verbose:
        print("=== Dijkstra: Inicialización ===")
        print(f"Vértice inicial: {start_id}")
        if end_id:
            print(f"Vértice destino: {end_id}")
        print()

    iteracion = 0
    
    # === Proceso principal ===
    while pq:
        # Extraer el vértice con menor distancia
        dist_actual, u_id = heapq.heappop(pq)
        
        # Si ya fue visitado, saltar
        if u_id in visitados:
            continue
        
        visitados.add(u_id)
        iteracion += 1
        
        if verbose:
            print(f"=== Iteración {iteracion} ===")
            print(f"  Procesando vértice: {u_id} (distancia={dist_actual})")
        
        # Si llegamos al destino, podemos terminar
        if end_id and u_id == end_id:
            if verbose:
                print(f"  ✓ Destino {end_id} alcanzado!")
            break
        
        # Examinar vecinos
        vertex_u = graph.get_vertex(u_id)
        
        for vertex_v, weight in vertex_u.get_connections().items():
            v_id = vertex_v.id
            
            # Si ya fue visitado, saltar
            if v_id in visitados:
                continue
            
            # Relajación
            nueva_distancia = dist[u_id] + weight
            
            if nueva_distancia < dist[v_id]:
                old_dist = dist[v_id]
                dist[v_id] = nueva_distancia
                pred[v_id] = u_id
                heapq.heappush(pq, (nueva_distancia, v_id))
                
                if verbose:
                    old_str = "∞" if old_dist == math.inf else f"{old_dist}"
                    print(f"    Actualizado {v_id}: {u_id} → {v_id} (peso={weight})")
                    print(f"      Distancia: {old_str} → {nueva_distancia}")
        
        if verbose:
            print(f"  Visitados hasta ahora: {sorted(visitados)}")
            print()

    if verbose:
        print("\n=== Resultado Final ===")
        print(f"Caminos más cortos desde {start_id}:")
        for v in sorted(graph.get_vertices()):
            if dist[v] != math.inf:
                dist_str = f"{dist[v]}"
                print(f"  {v}: distancia={dist_str}, predecesor={pred[v]}")
            else:
                print(f"  {v}: NO ALCANZABLE")

    # Reconstruir camino si se especificó destino
    camino = None
    if end_id:
        camino = obtener_camino(pred, start_id, end_id)

    return {
        'distancias': dist,
        'predecesores': pred,
        'camino': camino
    }


def obtener_camino(pred, start_id, end_id):
    """
    Reconstruye el camino desde start_id hasta end_id usando los predecesores.
    
    Args:
        pred: Diccionario de predecesores
        start_id: ID del vértice inicial
        end_id: ID del vértice destino
    
    Returns:
        list: Lista de IDs representando el camino, o None si no hay camino
    """
    if pred.get(end_id) is None:
        return None
    
    if start_id not in pred or end_id not in pred:
        return None
    
    camino = []
    actual = end_id
    
    # Prevenir ciclos infinitos
    visitados = set()
    
    while actual != start_id:
        if actual in visitados:
            return None  # Ciclo detectado
        
        camino.append(actual)
        visitados.add(actual)
        actual = pred[actual]
        
        if actual is None:
            return None
    
    camino.append(start_id)
    camino.reverse()
    
    return camino


def obtener_distancia(dist, end_id):
    """
    Obtiene la distancia más corta hacia un vértice.
    
    Args:
        dist: Diccionario de distancias
        end_id: ID del vértice destino
    
    Returns:
        float: Distancia, o math.inf si no hay camino, o None si el vértice no existe
    """
    if end_id not in dist:
        return None
    
    return dist[end_id]


def imprimir_camino(graph, resultado, start_id, end_id):
    """
    Imprime el camino más corto desde start_id hasta end_id de forma legible.
    
    Args:
        graph: Instancia de Graph
        resultado: Resultado de dijkstra()
        start_id: ID del vértice inicial
        end_id: ID del vértice destino
    """
    pred = resultado['predecesores']
    dist = resultado['distancias']
    
    camino = obtener_camino(pred, start_id, end_id)
    distancia = obtener_distancia(dist, end_id)
    
    if camino is None or distancia == math.inf:
        print(f"\n❌ No existe un camino desde {start_id} hasta {end_id}")
        return
    
    print(f"\n=== Camino más corto: {start_id} → {end_id} ===")
    print(f"Distancia total: {distancia}")
    print("Ruta:", " → ".join(map(str, camino)))
    
    # Mostrar detalles de cada arista
    print("\nDetalle del camino:")
    total_acumulado = 0
    for i in range(len(camino) - 1):
        u = camino[i]
        v = camino[i + 1]
        vertex_u = graph.get_vertex(u)
        vertex_v = graph.get_vertex(v)
        weight = vertex_u.get_connections()[vertex_v]
        total_acumulado += weight
        print(f"  {u} → {v}: peso = {weight} (acumulado: {total_acumulado})")


def encontrar_camino_mas_corto(graph, start_id, end_id, verbose=False):
    """
    Función simplificada para encontrar el camino más corto entre dos puntos.
    Ideal para usar en el juego.
    
    Args:
        graph: Instancia de Graph
        start_id: ID del vértice inicial (estrella actual del burro)
        end_id: ID del vértice destino (estrella objetivo)
        verbose: Si True, muestra el proceso
    
    Returns:
        dict: {
            'existe': bool,
            'camino': list de IDs (el recorrido completo),
            'distancia': float (distancia total),
            'pasos': list de dict con detalles de cada paso
        }
        None si hay error
    """
    resultado = dijkstra(graph, start_id, end_id, verbose)
    
    if resultado is None:
        return None
    
    camino = resultado['camino']
    distancia = resultado['distancias'].get(end_id, math.inf)
    
    if camino is None or distancia == math.inf:
        return {
            'existe': False,
            'camino': None,
            'distancia': math.inf,
            'pasos': []
        }
    
    # Construir detalles de cada paso
    pasos = []
    distancia_acumulada = 0
    
    for i in range(len(camino) - 1):
        u = camino[i]
        v = camino[i + 1]
        vertex_u = graph.get_vertex(u)
        vertex_v = graph.get_vertex(v)
        peso = vertex_u.get_connections()[vertex_v]
        distancia_acumulada += peso
        
        pasos.append({
            'desde': u,
            'hasta': v,
            'peso': peso,
            'distancia_acumulada': distancia_acumulada
        })
    
    return {
        'existe': True,
        'camino': camino,
        'distancia': distancia,
        'pasos': pasos
    }


def obtener_estrellas_alcanzables(graph, start_id, energia_maxima, verbose=False):
    """
    Encuentra todas las estrellas alcanzables dentro de un límite de energía.
    Útil para mostrar opciones disponibles al burro.
    
    Args:
        graph: Instancia de Graph
        start_id: ID de la estrella actual
        energia_maxima: Energía disponible del burro
        verbose: Si True, muestra información
    
    Returns:
        list: Lista de dict con información de estrellas alcanzables, ordenadas por distancia
    """
    resultado = dijkstra(graph, start_id, verbose=verbose)
    
    if resultado is None:
        return []
    
    alcanzables = []
    
    for v_id in graph.get_vertices():
        if v_id == start_id:
            continue
        
        distancia = resultado['distancias'][v_id]
        
        if distancia <= energia_maxima and distancia != math.inf:
            camino = obtener_camino(resultado['predecesores'], start_id, v_id)
            
            alcanzables.append({
                'id': v_id,
                'distancia': distancia,
                'camino': camino,
                'energia_restante': energia_maxima - distancia
            })
    
    # Ordenar por distancia (más cercanas primero)
    alcanzables.sort(key=lambda x: x['distancia'])
    
    return alcanzables