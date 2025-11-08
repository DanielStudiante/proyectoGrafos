from typing import Optional, List

class Estrella:
    """
    Representa una estrella con sus propiedades físicas.
    Se integra con Donkey pero NO maneja el grafo.
    """
    
    def __init__(
        self,
        id: int,
        label: str = "",
        x: float = 0.0,
        y: float = 0.0,
        radius: float = 1.0,
        constelaciones: Optional[List[str]] = None,
        hipergigante: bool = False,
        time_to_eat: float = 1.0,  # Tiempo para comer 1kg de pasto
        amount_of_energy: float = 10.0,  # Energía que otorga
    ):
        # Identificadores
        self.id = id
        self.label = label if label else str(id)
        
        # Posición espacial
        self.x = x
        self.y = y
        self.radius = radius
        
        # Clasificación
        self.constelaciones = constelaciones if constelaciones else []
        self.hipergigante = hipergigante
        
        # Parámetros de simulación (del JSON)
        self.time_to_eat = time_to_eat  # timeToEat del JSON
        self.amount_of_energy = amount_of_energy  # amountOfEnergy del JSON
        
        # Estado
        self.visitada = False
        self.activa = True
    
    def is_hypergiant(self) -> bool:
        """Verifica si es una estrella hipergigante."""
        return self.hipergigante
    
    def marcar_visitada(self):
        """Marca la estrella como visitada."""
        self.visitada = True
    
    def resetear_visita(self):
        """Resetea el estado de visita."""
        self.visitada = False
    
    def bloquear(self):
        """Bloquea la estrella (no se puede visitar)."""
        self.activa = False
    
    def desbloquear(self):
        """Desbloquea la estrella."""
        self.activa = True
    
    def to_dict(self) -> dict:
        """Serializa a diccionario."""
        return {
            'id': self.id,
            'label': self.label,
            'x': self.x,
            'y': self.y,
            'radius': self.radius,
            'constelaciones': self.constelaciones,
            'hypergiant': self.hipergigante,
            'timeToEat': self.time_to_eat,
            'amountOfEnergy': self.amount_of_energy,
            'visitada': self.visitada,
        }
    
    def __str__(self):
        tipo = "Hipergigante" if self.hipergigante else "Normal"
        return f"Estrella({self.id}, '{self.label}', {tipo})"
    
    def __repr__(self):
        return self.__str__()