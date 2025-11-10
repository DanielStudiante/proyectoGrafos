"""
Estructura base de grafo.
Responsabilidad: Solo la lógica de grafos (vértices y aristas).
"""

class Vertex:
    """Representa un vértice en el grafo."""
    
    def __init__(self, id, x=0, y=0, constelaciones=None):
        self.id = id
        self.x = x
        self.y = y
        self.constelaciones = constelaciones or []
        self.neighbors = {}  # {Vertex: peso}
        self.blocked_edges = set()  # IDs de vértices bloqueados (Req 0.5)
    
    def add_neighbor(self, vertex, weight=0):
        """Añade un vecino con un peso."""
        self.neighbors[vertex] = weight
    
    def get_connections(self):
        """Retorna el diccionario de vecinos (solo los no bloqueados)."""
        # REQUERIMIENTO 0.5: Filtrar conexiones bloqueadas
        return {
            vertex: weight 
            for vertex, weight in self.neighbors.items() 
            if vertex.id not in self.blocked_edges
        }
    
    def get_all_connections(self):
        """Retorna TODAS las conexiones (incluyendo bloqueadas)."""
        return self.neighbors
    
    def block_edge(self, vertex_id):
        """Bloquea el camino hacia un vértice (REQUERIMIENTO 0.5)."""
        self.blocked_edges.add(vertex_id)
    
    def unblock_edge(self, vertex_id):
        """Habilita el camino hacia un vértice (REQUERIMIENTO 0.5)."""
        self.blocked_edges.discard(vertex_id)
    
    def is_edge_blocked(self, vertex_id):
        """Verifica si el camino está bloqueado (REQUERIMIENTO 0.5)."""
        return vertex_id in self.blocked_edges
    
    def get_weight(self, vertex):
        """Obtiene el peso de la conexión a un vecino."""
        return self.neighbors.get(vertex, None)
    
    def __str__(self):
        return f"Vertex({self.id})"


class Graph:
    """Grafo base que mantiene vértices y conexiones."""
    
    def __init__(self):
        self.graph = {}  # {id: Vertex}
    
    def add_vertex(self, id, x=0, y=0, constelaciones=None):
        """Añade un vértice al grafo."""
        if id not in self.graph:
            self.graph[id] = Vertex(id, x, y, constelaciones)
        return self.graph[id]
    
    def get_vertex(self, id):
        """Obtiene un vértice por ID."""
        return self.graph.get(id)
    
    def get_vertices(self):
        """Retorna lista de IDs de vértices."""
        return list(self.graph.keys())
    
    def add_edge(self, from_id, to_id, weight=0):
        """Añade una arista entre dos vértices."""
        if from_id not in self.graph:
            self.add_vertex(from_id)
        if to_id not in self.graph:
            self.add_vertex(to_id)
        
        self.graph[from_id].add_neighbor(self.graph[to_id], weight)
