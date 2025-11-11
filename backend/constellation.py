"""
Grafo de constelaciones.
Responsabilidad: Gestión de estrellas agrupadas en constelaciones.
"""

from typing import Dict, List, Optional
from backend.graph import Graph
from backend.star import Estrella


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
        stay_duration: float = 5.0,
        amount_of_energy: float = 10.0,
        health_impact: float = 0.0,
        life_time_impact: float = 0.0,
        research_energy_cost: float = 1.0,
    ) -> Estrella:
        """
        Agrega una estrella al grafo.
        Si la estrella ya existe, acumula las constelaciones nuevas.
        """
        # Si la estrella ya existe, solo agregar constelaciones nuevas
        if id in self.estrellas:
            estrella_existente = self.estrellas[id]
            
            # Acumular constelaciones (sin duplicados)
            for const in (constelaciones or []):
                if const not in estrella_existente.constelaciones:
                    estrella_existente.constelaciones.append(const)
                
                # Actualizar también el diccionario de constelaciones
                if const not in self.constelaciones:
                    self.constelaciones[const] = []
                if id not in self.constelaciones[const]:
                    self.constelaciones[const].append(id)
            
            return estrella_existente
        
        # Si es nueva, crear la estrella
        # Crear vértice en el grafo (para algoritmos)
        self.add_vertex(id, x, y, constelaciones)
        
        # Crear estrella con datos
        estrella = Estrella(
            id=id,
            label=label,
            x=x,
            y=y,
            radius=radius,
            constelaciones=constelaciones or [],
            hipergigante=hipergigante,
            time_to_eat=time_to_eat,
            stay_duration=stay_duration,
            amount_of_energy=amount_of_energy,
            health_impact=health_impact,
            life_time_impact=life_time_impact,
            research_energy_cost=research_energy_cost,
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
    
    def obtener_color_constelacion(self, nombre_constelacion: str) -> int:
        """
        Obtiene el índice de color para una constelación.
        Retorna un número entre 0-9 para mapear a la paleta de colores.
        """
        constelaciones_ordenadas = sorted(self.constelaciones.keys())
        try:
            return constelaciones_ordenadas.index(nombre_constelacion) % 10
        except ValueError:
            return 0
    
    def estrella_tiene_multiples_constelaciones(self, star_id: int) -> bool:
        """
        Verifica si una estrella pertenece a más de una constelación.
        Según requerimiento: debe resaltarse en ROJO.
        """
        estrella = self.obtener_estrella(star_id)
        if estrella:
            return len(estrella.constelaciones) > 1
        return False
    
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
        
        IMPORTANTE: En un grafo no dirigido, bloquear A→B también bloquea B→A.
        
        Args:
            from_id: ID de la estrella origen
            to_id: ID de la estrella destino
            
        Returns:
            True si se bloqueó exitosamente, False si no existe el camino
        """
        vertex_from = self.get_vertex(from_id)
        vertex_to = self.get_vertex(to_id)
        
        if vertex_from and vertex_to and vertex_to in vertex_from.neighbors:
            # Bloquear en AMBAS direcciones para grafo no dirigido
            vertex_from.block_edge(to_id)
            vertex_to.block_edge(from_id)
            return True
        return False
    
    def habilitar_camino(self, from_id: int, to_id: int) -> bool:
        """
        Habilita el camino entre dos estrellas (REQUERIMIENTO 0.5).
        
        IMPORTANTE: En un grafo no dirigido, habilitar A→B también habilita B→A.
        
        Args:
            from_id: ID de la estrella origen
            to_id: ID de la estrella destino
            
        Returns:
            True si se habilitó exitosamente, False si no existe el camino
        """
        vertex_from = self.get_vertex(from_id)
        vertex_to = self.get_vertex(to_id)
        
        if vertex_from and vertex_to and vertex_to in vertex_from.neighbors:
            # Habilitar en AMBAS direcciones para grafo no dirigido
            vertex_from.unblock_edge(to_id)
            vertex_to.unblock_edge(from_id)
            return True
        return False
    
    def esta_camino_bloqueado(self, from_id: int, to_id: int) -> bool:
        """
        Verifica si el camino está bloqueado (REQUERIMIENTO 0.5).
        
        IMPORTANTE: Verifica en ambas direcciones ya que es un grafo no dirigido.
        
        Args:
            from_id: ID de la estrella origen
            to_id: ID de la estrella destino
            
        Returns:
            True si está bloqueado, False si está habilitado
        """
        vertex_from = self.get_vertex(from_id)
        vertex_to = self.get_vertex(to_id)
        
        # Verificar bloqueo en cualquiera de las dos direcciones
        if vertex_from and vertex_from.is_edge_blocked(to_id):
            return True
        if vertex_to and vertex_to.is_edge_blocked(from_id):
            return True
        
        return False
    
    def obtener_caminos_bloqueados(self) -> List[tuple]:
        """
        Obtiene lista de todos los caminos bloqueados.
        
        IMPORTANTE: Como el grafo es no dirigido, evita duplicados (A→B y B→A se consideran el mismo camino).
        
        Returns:
            Lista de tuplas (from_id, to_id) de caminos bloqueados (sin duplicados)
        """
        bloqueados = []
        procesados = set()
        
        for vertex_id, vertex in self.graph.items():
            for blocked_id in vertex.blocked_edges:
                # Crear clave única para evitar duplicados (A→B y B→A)
                camino_key = tuple(sorted([vertex_id, blocked_id]))
                
                if camino_key not in procesados:
                    bloqueados.append((vertex_id, blocked_id))
                    procesados.add(camino_key)
        
        return bloqueados
