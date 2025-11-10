"""
Calculador de salud del burro.
Responsabilidad: Single Responsibility - solo calcular salud basado en energía.
"""
from dataclasses import dataclass
from enum import Enum
from typing import Final


class HealthStatus(Enum):
    """Estados de salud posibles del burro."""
    EXCELLENT = "Excelente"
    GOOD = "Buena"
    BAD = "Mala"
    DYING = "Moribundo"
    DEAD = "Muerto"


@dataclass(frozen=True)
class HealthThresholds:
    """Umbrales de energía para cada estado de salud (inmutable)."""
    EXCELLENT: Final[float] = 75.0
    GOOD: Final[float] = 50.0
    BAD: Final[float] = 25.0
    DYING: Final[float] = 1.0


class HealthCalculator:
    """
    Calcula el estado de salud basado en la energía.
    Sigue Single Responsibility Principle.
    """
    
    def __init__(self, thresholds: HealthThresholds = None):
        """
        Args:
            thresholds: Umbrales personalizados (Dependency Injection)
        """
        self._thresholds = thresholds or HealthThresholds()
    
    def calculate_health(self, energy: float) -> HealthStatus:
        """
        Calcula el estado de salud basado en la energía actual.
        
        Args:
            energy: Nivel de energía actual
            
        Returns:
            HealthStatus correspondiente
        """
        if energy > self._thresholds.EXCELLENT:
            return HealthStatus.EXCELLENT
        elif energy >= self._thresholds.GOOD:
            return HealthStatus.GOOD
        elif energy >= self._thresholds.BAD:
            return HealthStatus.BAD
        elif energy >= self._thresholds.DYING:
            return HealthStatus.DYING
        else:
            return HealthStatus.DEAD
    
    def is_alive(self, energy: float) -> bool:
        """Verifica si el burro está vivo basado en energía."""
        return energy > 0
