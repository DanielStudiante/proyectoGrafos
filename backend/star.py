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
        stay_duration: float = 5.0,  # Tiempo total de estadía en la estrella (horas)
        amount_of_energy: float = 10.0,  # Energía que otorga
        health_impact: float = 0.0,  # Impacto en la salud (positivo o negativo)
        life_time_impact: float = 0.0,  # Impacto en el tiempo de vida en años luz (positivo=gana, negativo=pierde)
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
        self.stay_duration = stay_duration  # stayDuration del JSON - tiempo de estadía
        self.amount_of_energy = amount_of_energy  # amountOfEnergy del JSON
        
        # Efectos de investigación en la estrella
        self.health_impact = health_impact  # Impacto en energía/salud del burro
        self.life_time_impact = life_time_impact  # Años luz ganados o perdidos
        
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
    
    def set_health_impact(self, value: float):
        """Establece el impacto en la salud/energía del burro."""
        self.health_impact = value
    
    def set_life_time_impact(self, value: float):
        """Establece el impacto en el tiempo de vida (años luz)."""
        self.life_time_impact = value
    
    def get_investigation_effects(self) -> dict:
        """Retorna los efectos de investigar esta estrella."""
        return {
            'health_impact': self.health_impact,
            'life_time_impact': self.life_time_impact,
            'description': self._get_effect_description()
        }
    
    def _get_effect_description(self) -> str:
        """Genera una descripción de los efectos."""
        effects = []
        
        if self.health_impact > 0:
            effects.append(f"💚 +{self.health_impact:.1f} de energía")
        elif self.health_impact < 0:
            effects.append(f"💔 {self.health_impact:.1f} de energía")
        
        if self.life_time_impact > 0:
            effects.append(f"⏰ +{self.life_time_impact:.1f} años luz de vida")
        elif self.life_time_impact < 0:
            effects.append(f"⚠️ {self.life_time_impact:.1f} años luz de vida")
        
        return " | ".join(effects) if effects else "Sin efectos"
    
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
            'stayDuration': self.stay_duration,
            'amountOfEnergy': self.amount_of_energy,
            'healthImpact': self.health_impact,
            'lifeTimeImpact': self.life_time_impact,
            'visitada': self.visitada,
        }
    
    def __str__(self):
        tipo = "Hipergigante" if self.hipergigante else "Normal"
        return f"Estrella({self.id}, '{self.label}', {tipo})"
    
    def __repr__(self):
        return self.__str__()