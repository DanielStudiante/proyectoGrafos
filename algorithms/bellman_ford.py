import math

def bellman_ford(graph, start_id, verbose=False):
    """
    Algoritmo de Bellman-Ford. Detecta ciclos negativos.
    
    Args:
        graph: Instancia de Graph
        start_id: ID del vértice inicial
        verbose: Si True, imprime el proceso
    
    Returns:
        dict con 'distancias', 'predecesores', 'tiene_ciclo_negativo'
    """
    if start_id not in graph.get_vertices():
        if verbose:
            print(f"Error: El vértice {start_id} no existe.")
        return None

    dist = {v: math.inf for v in graph.get_vertices()}
    pred = {v: None for v in graph.get_vertices()}
    dist[start_id] = 0
    pred[start_id] = start_id

    num_vertices = len(graph.get_vertices())
    
    # Relajación
    for iteration in range(num_vertices - 1):
        cambios = False

        for u_id in graph.get_vertices():
            vertex_u = graph.get_vertex(u_id)
            
            if dist[u_id] == math.inf:
                continue
            
            for vertex_v, weight in vertex_u.get_connections().items():
                v_id = vertex_v.id
                
                if dist[u_id] + weight < dist[v_id]:
                    dist[v_id] = dist[u_id] + weight
                    pred[v_id] = u_id
                    cambios = True

        if not cambios:
            break

    # Detección de ciclos negativos
    tiene_ciclo_negativo = False
    
    for u_id in graph.get_vertices():
        vertex_u = graph.get_vertex(u_id)
        
        if dist[u_id] == math.inf:
            continue
            
        for vertex_v, weight in vertex_u.get_connections().items():
            v_id = vertex_v.id
            
            if dist[u_id] + weight < dist[v_id]:
                tiene_ciclo_negativo = True
                break
        
        if tiene_ciclo_negativo:
            break

    return {
        'distancias': dist,
        'predecesores': pred,
        'tiene_ciclo_negativo': tiene_ciclo_negativo
    }