from typing import Dict, List, Optional
from models.vertex import Graph
from models.star import Estrella

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