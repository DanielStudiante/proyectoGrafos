from typing import Dict, List, Optional
from backend.star import Estrella


class Vertex:
    """Representa un vértice en el grafo."""
    
    def __init__(self, id, x=0, y=0, constelaciones=None):
        self.id = id
        self.x = x
        self.y = y
        self.constelaciones = constelaciones or []
        self.neighbors = {}  # {Vertex: peso}
    
    def add_neighbor(self, vertex, weight=0):
        """Añade un vecino con un peso."""
        self.neighbors[vertex] = weight
    
    def get_connections(self):
        """Retorna el diccionario de vecinos."""
        return self.neighbors
    
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


class GrafoConstelaciones(Graph):
    """
    Extiende Graph para manejar constelaciones y estrellas.
    Mantiene la estructura de Vertex para algoritmos, 
    pero agrega datos de Estrella.
    """
    
    def __init__(self):
        super().__init__()
        self.estrellas: Dict[int, Estrella] = {}
        self.constelaciones: Dict[str, List[int]] = {}
    
    def agregar_estrella(
        self,
        id: int,
        label: str = "",
        x: float = 0.0,
        y: float = 0.0,
        radius: float = 1.0,
        constelaciones: Optional[List[str]] = None,
        hipergigante: bool = False,
        time_to_eat: float = 1.0,
        amount_of_energy: float = 10.0,
        health_impact: float = 0.0,
        life_time_impact: float = 0.0,
    ) -> Estrella:
        """Agrega una estrella al grafo."""
        # Crear vértice en el grafo (para algoritmos)
        self.add_vertex(id, x, y, constelaciones)
        
        # Crear estrella con datos
        estrella = Estrella(
            id=id,
            label=label,
            x=x,
            y=y,
            radius=radius,
            constelaciones=constelaciones,
            hipergigante=hipergigante,
            time_to_eat=time_to_eat,
            amount_of_energy=amount_of_energy,
            health_impact=health_impact,
            life_time_impact=life_time_impact,
        )
        
        self.estrellas[id] = estrella
        
        # Agrupar por constelación
        for const in (constelaciones or []):
            if const not in self.constelaciones:
                self.constelaciones[const] = []
            self.constelaciones[const].append(id)
        
        return estrella
    
    def obtener_estrella(self, id: int) -> Optional[Estrella]:
        """Obtiene los datos de una estrella."""
        return self.estrellas.get(id)
    
    def obtener_constelacion(self, nombre: str) -> List[int]:
        """Obtiene IDs de estrellas de una constelación."""
        return self.constelaciones.get(nombre, [])
    
    def listar_constelaciones(self) -> List[str]:
        """Lista todas las constelaciones."""
        return list(self.constelaciones.keys())
    
    def obtener_estrellas_activas(self) -> List[int]:
        """Retorna solo las estrellas activas."""
        return [
            id for id, estrella in self.estrellas.items()
            if estrella.activa
        ]
    
    def obtener_hipergigantes(self) -> List[int]:
        """Retorna IDs de estrellas hipergigantes."""
        return [
            id for id, estrella in self.estrellas.items()
            if estrella.hipergigante
        ]
    
    def bloquear_camino(self, from_id: int, to_id: int) -> bool:
        """
        Bloquea el camino entre dos estrellas (REQUERIMIENTO 0.5).
        
        Args:
            from_id: ID de la estrella origen
            to_id: ID de la estrella destino
            
        Returns:
            True si se bloqueó exitosamente, False si no existe el camino
        """
        vertex_from = self.get_vertex(from_id)
        vertex_to = self.get_vertex(to_id)
        
        if vertex_from and vertex_to and vertex_to in vertex_from.neighbors:
            vertex_from.block_edge(to_id)
            return True
        return False
    
    def habilitar_camino(self, from_id: int, to_id: int) -> bool:
        """
        Habilita el camino entre dos estrellas (REQUERIMIENTO 0.5).
        
        Args:
            from_id: ID de la estrella origen
            to_id: ID de la estrella destino
            
        Returns:
            True si se habilitó exitosamente, False si no existe el camino
        """
        vertex_from = self.get_vertex(from_id)
        vertex_to = self.get_vertex(to_id)
        
        if vertex_from and vertex_to and vertex_to in vertex_from.neighbors:
            vertex_from.unblock_edge(to_id)
            return True
        return False
    
    def esta_camino_bloqueado(self, from_id: int, to_id: int) -> bool:
        """
        Verifica si el camino está bloqueado (REQUERIMIENTO 0.5).
        
        Args:
            from_id: ID de la estrella origen
            to_id: ID de la estrella destino
            
        Returns:
            True si está bloqueado, False si está habilitado
        """
        vertex_from = self.get_vertex(from_id)
        if vertex_from:
            return vertex_from.is_edge_blocked(to_id)
        return False
    
    def obtener_caminos_bloqueados(self) -> List[tuple]:
        """
        Obtiene lista de todos los caminos bloqueados.
        
        Returns:
            Lista de tuplas (from_id, to_id) de caminos bloqueados
        """
        bloqueados = []
        for vertex_id, vertex in self.graph.items():
            for blocked_id in vertex.blocked_edges:
                bloqueados.append((vertex_id, blocked_id))
        return bloqueados