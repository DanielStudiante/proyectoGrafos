"""
Modelo del burro científico - Refactorizado con SOLID y mejores prácticas Python.

Principios aplicados:
- Single Responsibility: Cada clase tiene una sola responsabilidad
- Dependency Inversion: Inyección de dependencias (calculadoras)
- Type hints completos (PEP 484)
- Dataclasses para datos inmutables
- Nombres según PEP 8
"""
from dataclasses import dataclass
from typing import Optional

from models.health_calculator import HealthCalculator, HealthStatus
from models.damage_calculator import DamageCalculator


# Constantes del módulo (PEP 8: UPPER_CASE)
MAX_ENERGY: float = 100.0
MIN_ENERGY: float = 0.0


class Donkey:
    """
    Burro científico explorador de constelaciones.
    
    Responsabilidad: Gestionar estado y acciones del burro.
    Usa Dependency Injection para testing y flexibilidad.
    """
    
    def __init__(
        self,
        name: str,
        age: float,
        max_age: float,
        donkey_energy: float,
        grass_in_basement: int,
        health_calculator: Optional[HealthCalculator] = None,
        damage_calculator: Optional[DamageCalculator] = None
    ):
        """
        Inicializa el burro con sus stats.
        
        Args:
            name: Nombre del burro
            age: Edad actual en años luz  
            max_age: Edad máxima (al llegar aquí, muere)
            donkey_energy: Energía inicial (0-100)
            grass_in_basement: Cantidad de pasto en kg
            health_calculator: Calculadora de salud (inyectable)
            damage_calculator: Calculadora de daño (inyectable)
        """
        # State (mutable)
        self.name: str = name
        self.age: float = age
        self.max_age: float = max_age
        self.donkey_energy: float = self._clamp_energy(donkey_energy)
        self.grass_in_basement: int = grass_in_basement
        self.alive: bool = True
        
        # Dependency Inversion: inyección de dependencias
        self._health_calculator = health_calculator or HealthCalculator()
        self._damage_calculator = damage_calculator or DamageCalculator()
        
        # Propiedades derivadas
        self._update_health()
    
    @property
    def health(self) -> str:
        """Estado de salud actual (propiedad calculada)."""
        return self._health_calculator.calculate_health(self.donkey_energy).value
    
    @property
    def damage_stars(self) -> float:
        """Daño por viaje entre estrellas (propiedad calculada)."""
        return self._damage_calculator.calculate_damage(self.age, is_constellation=False)
    
    @property
    def damage_constellations(self) -> float:
        """Daño por viaje entre constelaciones (propiedad calculada)."""
        return self._damage_calculator.calculate_damage(self.age, is_constellation=True)
    
    def _clamp_energy(self, energy: float) -> float:
        """Asegura que la energía esté en rango válido [0, 100]."""
        return max(MIN_ENERGY, min(MAX_ENERGY, energy))
    
    def _update_health(self) -> None:
        """Actualiza el estado de salud basado en energía."""
        self.alive = self._health_calculator.is_alive(self.donkey_energy)
    
    def calculate_grass_profit(self) -> float:
        """
        Calcula el multiplicador de ganancia de energía al comer pasto.
        
        Returns:
            Multiplicador según salud actual (1.01 - 1.05)
        """
        if self.grass_in_basement <= 0:
            return 0.0
        
        # Mapeo salud -> multiplicador
        health_multipliers = {
            HealthStatus.EXCELLENT.value: 1.05,
            HealthStatus.GOOD.value: 1.03,
            HealthStatus.BAD.value: 1.02,
            HealthStatus.DYING.value: 1.01,
        }
        
        return health_multipliers.get(self.health, 1.0)
    
    def eat_grass(self, grass_profit: float = 1.0) -> bool:
        """
        Consume 1kg de pasto para recuperar energía.
        
        Args:
            grass_profit: Multiplicador de ganancia de energía
            
        Returns:
            True si comió exitosamente, False si no pudo
        """
        if self.grass_in_basement <= 0:
            print("No hay hierba en el sótano para que el burro coma.")
            return False
        
        if self.donkey_energy >= MAX_ENERGY:
            print("El burro ya tiene energía completa y no necesita comer.")
            return False
        
        # Incrementar energía
        self.donkey_energy += 1.0 * grass_profit
        self.donkey_energy = self._clamp_energy(self.donkey_energy)
        
        # Consumir pasto
        self.grass_in_basement -= 1
        
        # Actualizar estado
        self._update_health()
        
        return True
    
    def consume_energy(self, amount: float) -> None:
        """
        Consume energía y actualiza estado.
        
        Args:
            amount: Cantidad de energía a consumir
        """
        self.donkey_energy -= amount
        self.donkey_energy = self._clamp_energy(self.donkey_energy)
        self._update_health()
    
    def apply_health_impact(self, impact: float) -> None:
        """
        Aplica un impacto de salud (positivo o negativo).
        
        Args:
            impact: Cambio en energía (+recupera, -daña)
        """
        self.donkey_energy += impact
        self.donkey_energy = self._clamp_energy(self.donkey_energy)
        self._update_health()
    
    def apply_age_impact(self, impact: float) -> None:
        """
        Aplica un impacto de edad (investigación que gana/pierde tiempo).
        
        Args:
            impact: Años luz ganados (+) o perdidos (-)
        """
        self.age -= impact  # Restar porque ganar tiempo = reducir edad efectiva
        self._check_death()
    
    def apply_travel_wear(self, distance: float, is_constellation: bool = False) -> None:
        """
        Aplica desgaste por viaje.
        
        Args:
            distance: Distancia recorrida
            is_constellation: Si es viaje entre constelaciones
        """
        # Consumir energía por distancia
        self.consume_energy(distance)
        
        # Incrementar edad
        self.age += distance
        
        # Aplicar desgaste adicional
        damage = self.damage_constellations if is_constellation else self.damage_stars
        self.donkey_energy *= (1 - damage)
        self.donkey_energy = self._clamp_energy(self.donkey_energy)
        
        # Verificar muerte
        self._check_death()
    
    def apply_hypergiant_bonus(self) -> None:
        """Aplica bonus por llegar a estrella hipergigante."""
        self.donkey_energy *= 1.5
        self.donkey_energy = self._clamp_energy(self.donkey_energy)
        self.grass_in_basement *= 2
        self._update_health()
    
    def _check_death(self) -> None:
        """Verifica condiciones de muerte."""
        if self.age >= self.max_age or self.donkey_energy <= MIN_ENERGY:
            self.dead()
    
    def dead(self) -> None:
        """Marca al burro como muerto."""
        self.alive = False
    
    def __str__(self) -> str:
        """Representación legible."""
        return f"Donkey(name='{self.name}', age={self.age:.1f}, energy={self.donkey_energy:.1f}, health='{self.health}')"
    
    def __repr__(self) -> str:
        """Representación técnica."""
        return (f"Donkey(name={self.name!r}, age={self.age}, max_age={self.max_age}, "
                f"energy={self.donkey_energy}, grass={self.grass_in_basement}, alive={self.alive})")
