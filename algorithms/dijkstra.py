import math
import heapq

def dijkstra(graph, start_id, end_id=None, verbose=False):
    """
    Algoritmo de Dijkstra para encontrar el camino más corto.
    
    REQUERIMIENTO: Una estrella solo puede ser visitada una única vez.
    No considera estrellas ya visitadas como destinos válidos.
    
    Args:
        graph: Instancia de Graph con get_vertices() y get_vertex()
        start_id: ID del vértice inicial
        end_id: ID del vértice destino (opcional)
        verbose: Si True, imprime el proceso
    
    Returns:
        dict con 'distancias', 'predecesores', 'camino'
    """
    if start_id not in graph.get_vertices():
        if verbose:
            print(f"Error: El vértice {start_id} no existe.")
        return None

    dist = {v: math.inf for v in graph.get_vertices()}
    pred = {v: None for v in graph.get_vertices()}
    visitados = set()
    
    dist[start_id] = 0
    pred[start_id] = start_id
    pq = [(0, start_id)]
    
    while pq:
        dist_actual, u_id = heapq.heappop(pq)
        
        if u_id in visitados:
            continue
        
        visitados.add(u_id)
        
        if end_id and u_id == end_id:
            break
        
        vertex_u = graph.get_vertex(u_id)
        
        for vertex_v, weight in vertex_u.get_connections().items():
            v_id = vertex_v.id
            
            if v_id in visitados:
                continue
            
            # REQUERIMIENTO: No considerar estrellas ya visitadas
            # (excepto si es el punto de partida)
            estrella_v = graph.obtener_estrella(v_id)
            if estrella_v and estrella_v.visitada and v_id != start_id:
                continue
            
            nueva_distancia = dist[u_id] + weight
            
            if nueva_distancia < dist[v_id]:
                dist[v_id] = nueva_distancia
                pred[v_id] = u_id
                heapq.heappush(pq, (nueva_distancia, v_id))

    camino = None
    if end_id:
        camino = obtener_camino(pred, start_id, end_id)

    return {
        'distancias': dist,
        'predecesores': pred,
        'camino': camino
    }


def obtener_camino(pred, start_id, end_id):
    """Reconstruye el camino desde start_id hasta end_id."""
    if pred.get(end_id) is None:
        return None
    
    camino = []
    actual = end_id
    visitados = set()
    
    while actual != start_id:
        if actual in visitados:
            return None
        camino.append(actual)
        visitados.add(actual)
        actual = pred[actual]
        if actual is None:
            return None
    
    camino.append(start_id)
    camino.reverse()
    return camino


def encontrar_camino_mas_corto(graph, start_id, end_id, verbose=False):
    """
    Encuentra el camino más corto entre dos puntos.
    Retorna dict con 'existe', 'camino', 'distancia', 'pasos'.
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
    
    pasos = []
    for i in range(len(camino) - 1):
        u = camino[i]
        v = camino[i + 1]
        vertex_u = graph.get_vertex(u)
        vertex_v = graph.get_vertex(v)
        peso = vertex_u.get_connections()[vertex_v]
        
        pasos.append({
            'desde': u,
            'hasta': v,
            'peso': peso,
        })
    
    return {
        'existe': True,
        'camino': camino,
        'distancia': distancia,
        'pasos': pasos
    }


def obtener_estrellas_alcanzables(graph, start_id, energia_maxima, verbose=False):
    """Encuentra estrellas alcanzables dentro de un límite de energía."""
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
    
    alcanzables.sort(key=lambda x: x['distancia'])
    return alcanzables