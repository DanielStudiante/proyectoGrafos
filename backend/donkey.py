"""
Modelo del burro científico.
Refactorizado aplicando SOLID y mejores prácticas Python.

Principios SOLID aplicados:
- Single Responsibility: Cada calculadora tiene una única responsabilidad
- Open/Closed: Extendible mediante composición de calculadoras
- Dependency Inversion: Inyección de dependencias para testability

Mejores prácticas Python:
- Type hints completos (PEP 484)
- Properties para cálculos derivados
- Nombres según PEP 8
- Docstrings según PEP 257
"""
from time import sleep
from typing import Optional

from backend.health_calculator import HealthCalculator
from backend.damage_calculator import DamageCalculator


# Constantes del módulo (PEP 8: UPPER_CASE con underscores)
MAX_ENERGY: float = 100.0
MIN_ENERGY: float = 0.0


class Donkey:
    """
    Burro científico explorador de constelaciones estelares.
    
    Esta clase gestiona el estado completo del burro durante su viaje,
    incluyendo energía, edad, salud y recursos (pasto).
    
    Utiliza Dependency Injection para las calculadoras de salud y daño,
    lo que facilita el testing y permite extender funcionalidad sin modificar código.
    
    Attributes:
        name: Nombre del burro
        age: Edad actual en años luz
        max_age: Edad máxima antes de morir
        donkey_energy: Energía actual (0-100)
        grass_in_basement: Cantidad de pasto disponible en kg
        alive: Si el burro está vivo
        
    Properties (calculadas):
        health: Estado de salud basado en energía
        damage_stars: Porcentaje de desgaste por viaje entre estrellas
        damage_constellations: Porcentaje de desgaste entre constelaciones
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
    ) -> None:
        """
        Inicializa el burro con sus estadísticas base.
        
        Args:
            name: Nombre identificador del burro
            age: Edad inicial en años luz
            max_age: Edad límite antes de morir naturalmente
            donkey_energy: Energía inicial (se clampea a [0, 100])
            grass_in_basement: Cantidad inicial de pasto en kg
            health_calculator: Calculadora de salud (inyectable para testing)
            damage_calculator: Calculadora de daño (inyectable para testing)
        """
        # Estado mutable del burro
        self.name: str = name
        self.age: float = age
        self.max_age: float = max_age
        self.donkey_energy: float = self._clamp_energy(donkey_energy)
        self.grass_in_basement: int = grass_in_basement
        self.alive: bool = True
        
        # Dependency Inversion: inyección de dependencias
        # Permite mockear para testing y cambiar implementación
        self._health_calculator = health_calculator or HealthCalculator()
        self._damage_calculator = damage_calculator or DamageCalculator()
        
        # Calcular propiedades iniciales para compatibilidad
        self.damage_stars: float = self.calculate_damage_per_trip()
        self.damage_constellations: float = self.calculate_damage_per_trip(True)
        self.health: str = self.calculate_donkey_health()
    
    def calculate_damage_per_trip(self, is_constellation: bool = False) -> float:
        """Calcula el daño por viaje (método legacy mantenido para compatibilidad)."""
        return self._damage_calculator.calculate_damage(self.age, is_constellation)
    
    def calculate_donkey_health(self) -> str:
        """Calcula la salud del burro (método legacy mantenido para compatibilidad)."""
        return self._health_calculator.calculate_health(self.donkey_energy).value
    
    def _clamp_energy(self, energy: float) -> float:
        """
        Asegura que la energía esté dentro del rango válido [0, 100].
        
        Args:
            energy: Valor de energía a validar
            
        Returns:
            Energía clampeada al rango válido
        """
        return max(MIN_ENERGY, min(MAX_ENERGY, energy))
    
    def _update_derived_properties(self) -> None:
        """Actualiza las propiedades calculadas (para compatibilidad con código existente)."""
        self.damage_stars = self.calculate_damage_per_trip(False)
        self.damage_constellations = self.calculate_damage_per_trip(True)
        self.health = self.calculate_donkey_health()
        self.alive = self._health_calculator.is_alive(self.donkey_energy) and self.age < self.max_age
    
    def calculate_grass_profit(self) -> float:
        """
        Calcula cuánta energía aporta cada kg de pasto consumido.
        
        REQUERIMIENTO: El burro come pasto cuando tiene menos del 50% de energía.
        Cada kg de pasto aporta diferente energía según su salud:
        - Excelente: 5% de energía por kg
        - Buena: 3% de energía por kg  
        - Mala: 2% de energía por kg
        - Moribundo: 1% de energía por kg
        
        Returns:
            Porcentaje de energía ganada por kg de pasto (1-5%)
        """
        if self.grass_in_basement <= 0:
            return 0.0
        
        # Mapeo de estado de salud a porcentaje de energía ganada por kg
        health_energy_gain = {
            'Excelente': 5.0,  # 5% de energía por kg
            'Buena': 3.0,      # 3% de energía por kg
            'Mala': 2.0,       # 2% de energía por kg
            'Moribundo': 1.0,  # 1% de energía por kg
        }
        
        return health_energy_gain.get(self.health, 2.0)
    
    def eat_grass(self, grass_profit: float = 5.0) -> bool:
        """
        Consume 1kg de pasto para recuperar energía.
        
        REQUERIMIENTO: Solo puede comer si tiene menos del 50% de energía.
        
        Args:
            grass_profit: Porcentaje de energía ganada por kg (1-5%)
            
        Returns:
            True si comió exitosamente, False si no pudo comer
        """
        if self.grass_in_basement <= 0:
            print("No hay hierba en el sótano para que el burro coma.")
            return False
        
        # REQUERIMIENTO: Solo puede comer si tiene menos del 50% de energía
        if self.donkey_energy >= 50.0:
            print(f"El burro tiene {self.donkey_energy:.1f}% de energía (≥50%). No necesita comer.")
            return False
        
        # Incrementar energía según el porcentaje de ganancia
        self.donkey_energy += grass_profit
        self.donkey_energy = self._clamp_energy(self.donkey_energy)
        
        # Consumir pasto
        self.grass_in_basement -= 1
        
        # Actualizar propiedades derivadas
        self._update_derived_properties()
        
        return True
    
    def dead(self) -> None:
        """Marca al burro como muerto y detiene todas las acciones."""
        self.alive = False
        self.damage_stars = 0
    
    def stay_of_star(
        self,
        time_to_eat_kg: float = 0,
        time_of_stance: float = 0,
        health_impact: float = 0,
        life_time_impact: float = 0,
        research_energy_cost: float = 0
    ) -> Optional[str]:
        """
        El burro permanece en una estrella para investigar.
        
        REQUERIMIENTO: Al llegar a una estrella:
        - Si tiene < 50% energía, usa el 50% del tiempo para comer
        - El 50% restante (o 100% si no come) se usa para investigar
        - Cada kg de pasto tarda "time_to_eat_kg" horas en consumirse
        - La investigación consume "research_energy_cost" por hora
        
        Args:
            time_to_eat_kg: Tiempo para comer 1kg de hierba (horas)
            time_of_stance: Tiempo total de estancia en la estrella (horas)
            health_impact: Impacto en la energía/salud (positivo o negativo)
            life_time_impact: Impacto en el tiempo de vida en años luz
            research_energy_cost: Energía consumida por hora de investigación
            
        Returns:
            None si sobrevive, mensaje de error si muere
        """
        if not self.alive:
            return "El burro está muerto y no puede explorar."
        
        print(f"\n🔬 El burro investiga la estrella...")
        
        # REQUERIMIENTO: Si tiene < 50% energía, debe comer primero
        if self.donkey_energy < 50.0:
            print(f"⚠️ Energía baja ({self.donkey_energy:.1f}%). El burro come primero.")
            
            # 50% del tiempo para comer, 50% para investigar
            time_to_eat = time_of_stance * 0.5
            time_investigate = time_of_stance * 0.5
            
            # Calcular cuántos kg puede comer en ese tiempo
            kg_to_eat = int(time_to_eat / time_to_eat_kg) if time_to_eat_kg > 0 else 0
            
            print(f"🍽️  Tiempo disponible para comer: {time_to_eat:.1f} horas")
            print(f"🌾 Puede comer hasta {kg_to_eat} kg de pasto")
            
            # Comer pasto según el tiempo disponible
            kg_comidos = 0
            for _ in range(kg_to_eat):
                grass_profit = self.calculate_grass_profit()
                if self.eat_grass(grass_profit):
                    kg_comidos += 1
                    sleep(time_to_eat_kg)
                    print(f"  🌾 Comió 1 kg (+{grass_profit:.1f}% energía). Energía: {self.donkey_energy:.1f}%")
                    
                    # Si ya tiene ≥50% energía, deja de comer
                    if self.donkey_energy >= 50.0:
                        print(f"  ✅ Energía recuperada a {self.donkey_energy:.1f}%. Deja de comer.")
                        break
                else:
                    break
            
            if kg_comidos > 0:
                print(f"🌾 Total comido: {kg_comidos} kg de pasto")
        else:
            # Si tiene ≥50% energía, usa todo el tiempo para investigar
            time_investigate = time_of_stance
            print(f"✅ Energía suficiente ({self.donkey_energy:.1f}%). No necesita comer.")
        
        # Aplicar efectos de la investigación
        print(f"⏱️ Tiempo de investigación: {time_investigate:.1f} horas")
        
        # REQUERIMIENTO: Consumir energía durante la investigación
        # "Y" cantidad de energía por cada "X" tiempo de investigación
        if research_energy_cost > 0:
            energia_consumida = research_energy_cost * time_investigate
            self.donkey_energy -= energia_consumida
            print(f"🔬 Energía consumida investigando: {energia_consumida:.1f} ({research_energy_cost:.1f} × {time_investigate:.1f}h)")
        
        # Efectos en la salud/energía (healthImpact)
        if health_impact != 0:
            self.donkey_energy += health_impact
            if health_impact > 0:
                print(f"💚 La investigación fue beneficiosa: +{health_impact:.1f} de energía")
            else:
                print(f"💔 La investigación causó daño: {health_impact:.1f} de energía")
            
            # Asegurar que la energía esté en rango válido
            self.donkey_energy = self._clamp_energy(self.donkey_energy)
        
        # Efectos en el tiempo de vida
        if life_time_impact != 0:
            # Convención: NEGATIVO = malo (envejece), POSITIVO = bueno (rejuvenece)
            # Si life_time_impact < 0: pierde años de vida (se hace más viejo, age aumenta)
            # Si life_time_impact > 0: gana años de vida (se hace más joven, age disminuye)
            self.age -= life_time_impact  # Restamos porque positivo = ganar = reducir edad
            if life_time_impact > 0:  # Valores positivos rejuvenecen (disminuyen age)
                print(f"⏰ ¡Experimento exitoso! Rejuveneció {life_time_impact:.1f} años luz de vida")
                print(f"   Nueva edad efectiva: {self.age:.1f} años luz")
            else:  # Valores negativos envejecen (aumentan age)
                print(f"⚠️ La investigación envejeció {abs(life_time_impact):.1f} años luz de vida")
                print(f"   Nueva edad: {self.age:.1f} años luz")
        
        # Verificar si sigue vivo después de los efectos
        if self.age >= self.max_age or self.donkey_energy <= MIN_ENERGY:
            self.dead()
            print(f"\n💀 El burro ha muerto durante la investigación...")
            return "El burro ha muerto."
        
        # Actualizar propiedades derivadas
        self._update_derived_properties()
        print(f"💚 Estado de salud: {self.health}")
        print(f"⚡ Energía final: {self.donkey_energy:.1f}")
        
        return None

    def trip(
        self,
        distance: float,
        time_to_eat_kg: float = 0,
        time_of_stance: float = 0,
        is_star: bool = True,
        health_impact: float = 0,
        life_time_impact: float = 0,
        research_energy_cost: float = 0
    ) -> Optional[str]:
        """
        Realiza un viaje a una estrella.
        
        El viaje consume energía igual a la distancia recorrida multiplicada
        por un factor de reducción, más un desgaste adicional basado en la edad.
        
        Args:
            distance: Distancia a recorrer en años luz
            time_to_eat_kg: Tiempo para comer 1kg
            time_of_stance: Tiempo de estancia en la estrella
            is_star: Si es viaje dentro de la misma constelación
            health_impact: Impacto de investigación en salud
            life_time_impact: Impacto de investigación en tiempo de vida
            
        Returns:
            None si sobrevive, mensaje de error si muere
        """
        if not self.alive:
            return "El burro está muerto y no puede viajar."
        
        # REQUERIMIENTO 2.0.b: La distancia en años luz consume energía
        # Factor de consumo: 0.5 = 50% de la distancia (balance entre realismo y jugabilidad)
        # Ejemplo: viajar 20 años luz consume 10% de energía
        ENERGY_CONSUMPTION_FACTOR = 0.5
        
        # Consumir energía = distancia recorrida * factor de consumo
        self.donkey_energy -= distance * ENERGY_CONSUMPTION_FACTOR
        
        # REQUERIMIENTO 2.0.b: Incrementar edad por la distancia en años luz
        self.age += distance
        
        # Aplicar desgaste adicional por edad
        if is_star:
            self.donkey_energy *= (1 - self.damage_stars)
        else:
            self.donkey_energy *= (1 - self.damage_constellations)
        
        # Asegurar rango válido
        self.donkey_energy = self._clamp_energy(self.donkey_energy)
        
        # Verificar muerte
        if self.age >= self.max_age or self.donkey_energy <= MIN_ENERGY:
            self.dead()
            return "El burro ha muerto durante el viaje."
        
        # Actualizar propiedades derivadas
        self._update_derived_properties()
        
        # Investigar la estrella de destino si aplica
        if is_star:
            return self.stay_of_star(time_to_eat_kg, time_of_stance, health_impact, life_time_impact, research_energy_cost)
        
        return None

    def hyper_star(self, distance: float) -> Optional[str]:
        """
        Visita una estrella hipergigante que otorga bonificaciones.
        
        Las estrellas hipergigantes otorgan:
        - 50% más de energía
        - Duplica el pasto disponible
        
        Args:
            distance: Distancia recorrida hasta la estrella
            
        Returns:
            None si sobrevive, mensaje de error si muere
        """
        if not self.alive:
            return "El burro está muerto y no puede viajar."
        
        self.age += distance
        
        if self.age >= self.max_age or self.donkey_energy <= MIN_ENERGY:
            self.dead()
            return "El burro ha muerto durante el viaje."
        
        # Aplicar bonificaciones de hipergigante
        self.donkey_energy *= 1.5
        self.donkey_energy = self._clamp_energy(self.donkey_energy)
        self.grass_in_basement *= 2
        
        # Actualizar propiedades derivadas
        self._update_derived_properties()
        
        return None
    
    def intergalactic_travel(self) -> None:
        """
        Realiza un viaje inter-galáctico desde una estrella hipergigante.
        
        REQUERIMIENTO c: Las estrellas hipergigantes pueden enviar al burro
        a través de dos galaxias (constelaciones). Este viaje:
        - Recarga 50% de su nivel ACTUAL de burroenergía
        - Duplica la cantidad de pasto en bodega
        - NO consume energía (viaje instantáneo)
        - NO aumenta edad (viaje cuántico)
        
        Returns:
            None
        """
        # Recargar 50% de energía actual
        recharge_amount = self.donkey_energy * 0.5
        self.donkey_energy += recharge_amount
        self.donkey_energy = self._clamp_energy(self.donkey_energy)
        
        # Duplicar pasto en bodega
        self.grass_in_basement *= 2
        
        # Actualizar propiedades derivadas
        self._update_derived_properties()
        
        print(f"\n{'='*70}")
        print(f"🌌 ¡VIAJE INTER-GALÁCTICO COMPLETADO!")
        print(f"{'='*70}")
        print(f"⚡ Energía recargada: +{recharge_amount:.1f} (total: {self.donkey_energy:.1f})")
        print(f"🌾 Pasto duplicado: {self.grass_in_basement:.0f} kg")
        print(f"{'='*70}\n")