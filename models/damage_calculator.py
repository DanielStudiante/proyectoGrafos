"""
Calculador de daño por viaje.
Responsabilidad: Single Responsibility - calcular daño basado en edad.
"""
from dataclasses import dataclass
from typing import Final


@dataclass(frozen=True)
class DamageRates:
    """Tasas de daño para diferentes rangos de edad (inmutable)."""
    # Edad: [min, max, daño_estrella, daño_constelación]
    YOUNG_MAX: Final[float] = 891.0
    YOUNG_STAR: Final[float] = 0.05
    YOUNG_CONSTELLATION: Final[float] = 0.08
    
    ADULT_MAX: Final[float] = 1783.0
    ADULT_STAR: Final[float] = 0.10
    ADULT_CONSTELLATION: Final[float] = 0.15
    
    MATURE_MAX: Final[float] = 2675.0
    MATURE_STAR: Final[float] = 0.15
    MATURE_CONSTELLATION: Final[float] = 0.20
    
    OLD_STAR: Final[float] = 0.20
    OLD_CONSTELLATION: Final[float] = 0.25


class DamageCalculator:
    """
    Calcula el daño por desgaste en viajes.
    Sigue Single Responsibility Principle.
    """
    
    def __init__(self, rates: DamageRates = None):
        """
        Args:
            rates: Tasas de daño personalizadas (Dependency Injection)
        """
        self._rates = rates or DamageRates()
    
    def calculate_damage(self, age: float, is_constellation: bool = False) -> float:
        """
        Calcula el daño por desgaste basado en la edad.
        
        Args:
            age: Edad actual en años luz
            is_constellation: Si es viaje entre constelaciones
            
        Returns:
            Porcentaje de daño (0.05 = 5%)
        """
        if age < self._rates.YOUNG_MAX:
            return self._rates.YOUNG_CONSTELLATION if is_constellation else self._rates.YOUNG_STAR
        elif age < self._rates.ADULT_MAX:
            return self._rates.ADULT_CONSTELLATION if is_constellation else self._rates.ADULT_STAR
        elif age < self._rates.MATURE_MAX:
            return self._rates.MATURE_CONSTELLATION if is_constellation else self._rates.MATURE_STAR
        else:
            return self._rates.OLD_CONSTELLATION if is_constellation else self._rates.OLD_STAR
