"""
Utilidades para viajes inter-galácticos.
Responsabilidad: Calcular galaxias alcanzables y rutas.
"""

from typing import List, Dict, Set, Optional, Tuple
from backend.constellation import GrafoConstelaciones


def get_constellation_of_star(grafo: GrafoConstelaciones, star_id: int) -> Optional[str]:
    """
    Obtiene la constelación (galaxia) a la que pertenece una estrella.
    
    Args:
        grafo: Grafo de constelaciones
        star_id: ID de la estrella
    
    Returns:
        Nombre de la constelación o None
    """
    estrella = grafo.obtener_estrella(star_id)
    if not estrella or not estrella.constelaciones:
        return None
    return estrella.constelaciones[0]  # Usar primera constelación


def get_connected_constellations(grafo: GrafoConstelaciones) -> Dict[str, Set[str]]:
    """
    Construye un grafo de conexiones entre constelaciones (galaxias).
    
    Dos constelaciones están conectadas si hay al menos una arista
    entre estrellas de ambas constelaciones.
    
    Args:
        grafo: Grafo de constelaciones
    
    Returns:
        Dict {constelación: set de constelaciones vecinas}
    """
    connections = {}
    
    # Inicializar diccionario
    for const_name in grafo.listar_constelaciones():
        connections[const_name] = set()
    
    # Para cada estrella, ver sus vecinos
    for star_id, estrella in grafo.estrellas.items():
        if not estrella.constelaciones:
            continue
        
        star_constellation = estrella.constelaciones[0]
        
        # Obtener vecinos de esta estrella
        vertex = grafo.get_vertex(star_id)
        if not vertex:
            continue
        
        neighbors = vertex.get_connections()
        
        for neighbor_vertex, _ in neighbors.items():
            neighbor_star = grafo.obtener_estrella(neighbor_vertex.id)
            if not neighbor_star or not neighbor_star.constelaciones:
                continue
            
            neighbor_constellation = neighbor_star.constelaciones[0]
            
            # Si son diferentes constelaciones, hay conexión
            if star_constellation != neighbor_constellation:
                connections[star_constellation].add(neighbor_constellation)
                connections[neighbor_constellation].add(star_constellation)
    
    return connections


def get_reachable_constellations(
    grafo: GrafoConstelaciones,
    current_star_id: int,
    max_distance: int = 2
) -> Dict[str, int]:
    """
    Obtiene constelaciones (galaxias) alcanzables desde la posición actual.
    
    REQUERIMIENTO c: Hipergigantes pueden enviar a través de 2 galaxias.
    Usa BFS para encontrar constelaciones a distancia <= max_distance.
    
    Args:
        grafo: Grafo de constelaciones
        current_star_id: ID de la estrella actual (debe ser hipergigante)
        max_distance: Distancia máxima en saltos de galaxia (default: 2)
    
    Returns:
        Dict {nombre_constelación: distancia_en_saltos}
    """
    current_constellation = get_constellation_of_star(grafo, current_star_id)
    if not current_constellation:
        return {}
    
    # Construir grafo de conexiones entre constelaciones
    constellation_graph = get_connected_constellations(grafo)
    
    # BFS para encontrar constelaciones alcanzables
    visited = {current_constellation: 0}
    queue = [(current_constellation, 0)]
    
    while queue:
        constellation, distance = queue.pop(0)
        
        if distance >= max_distance:
            continue
        
        # Explorar vecinos
        for neighbor in constellation_graph.get(constellation, []):
            if neighbor not in visited:
                visited[neighbor] = distance + 1
                queue.append((neighbor, distance + 1))
    
    # Eliminar la constelación actual
    if current_constellation in visited:
        del visited[current_constellation]
    
    return visited


def get_stars_in_constellation(
    grafo: GrafoConstelaciones,
    constellation_name: str
) -> List[Dict]:
    """
    Obtiene todas las estrellas de una constelación.
    
    Args:
        grafo: Grafo de constelaciones
        constellation_name: Nombre de la constelación
    
    Returns:
        Lista de diccionarios con info de estrellas
    """
    star_ids = grafo.obtener_constelacion(constellation_name)
    stars = []
    
    for star_id in star_ids:
        estrella = grafo.obtener_estrella(star_id)
        if estrella:
            stars.append({
                'id': star_id,
                'label': estrella.label,
                'hipergigante': estrella.hipergigante,
                'x': estrella.x,
                'y': estrella.y
            })
    
    return stars


def is_hypergiant(grafo: GrafoConstelaciones, star_id: int) -> bool:
    """
    Verifica si una estrella es hipergigante.
    
    Args:
        grafo: Grafo de constelaciones
        star_id: ID de la estrella
    
    Returns:
        True si es hipergigante
    """
    estrella = grafo.obtener_estrella(star_id)
    return estrella.hipergigante if estrella else False
