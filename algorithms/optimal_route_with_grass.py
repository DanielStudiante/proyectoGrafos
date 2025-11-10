"""
Algoritmo para encontrar la ruta óptima con recarga automática de pasto.

REQUERIMIENTO 2.0: Dado un origen, sugerir la ruta que permite conocer
la mayor cantidad de estrellas con el menor gasto posible, considerando:
- Recarga automática de pasto cuando energía < 50%
- Ganancia de pasto según salud: Excelente=5%, Buena/Mala=3%, Moribundo=2%
- Solo 50% del tiempo de estadía para comer
- El otro 50% para investigación (consume energía)
- Cada estrella solo se visita una vez

Usa backtracking recursivo con poda inteligente (SOLID: SRP).
"""

from typing import List, Dict, Tuple, Optional
from backend.donkey import Donkey
from backend.constellation import GrafoConstelaciones
import math


class EstadoBurroConPasto:
    """
    Estado del burro con capacidad de recargar pasto.
    Responsabilidad: Mantener estado y simular acciones del burro.
    """
    
    def __init__(self, energia: float, edad: float, salud: str, pasto: float):
        self.energia = energia
        self.edad = edad
        self.salud = salud
        self.pasto = pasto
    
    def esta_vivo(self, max_age: float = 3567) -> bool:
        """Verifica si el burro está vivo."""
        return self.salud != "Muerto" and self.edad < max_age
    
    def necesita_comer(self) -> bool:
        """Verifica si el burro necesita comer (energía < 50%)."""
        return self.energia < 50.0
    
    def puede_comer(self) -> bool:
        """Verifica si tiene pasto disponible."""
        return self.pasto > 0
    
    def calcular_salud(self) -> str:
        """Calcula el estado de salud basado en la energía."""
        if self.energia <= 0:
            return "Muerto"
        elif self.energia <= 25:
            return "Moribundo"
        elif self.energia <= 50:
            return "Mala"
        elif self.energia <= 75:
            return "Buena"
        else:
            return "Excelente"
    
    def ganancia_por_kg(self) -> float:
        """
        Calcula la ganancia de energía por kg de pasto según salud.
        REQUERIMIENTO 2.0: Excelente=5%, Buena/Mala=3%, Moribundo=2%
        """
        if self.salud == "Excelente":
            return 5.0
        elif self.salud in ["Buena", "Mala"]:
            return 3.0
        else:  # Moribundo
            return 2.0
    
    def copy(self):
        """Crea una copia del estado."""
        return EstadoBurroConPasto(self.energia, self.edad, self.salud, self.pasto)


def simular_viaje_con_pasto(
    estado: EstadoBurroConPasto,
    distancia: float,
    estrella_destino,
    max_age: float = 3567
) -> Optional[EstadoBurroConPasto]:
    """
    Simula un viaje con posibilidad de comer pasto al llegar.
    
    REQUERIMIENTO 2.0: 
    - Viaja y consume energía
    - Al llegar, si energía < 50%, come pasto automáticamente
    - Solo puede usar 50% del tiempo de estadía para comer
    - El otro 50% se usa para investigación
    
    Args:
        estado: Estado actual del burro
        distancia: Distancia a viajar
        estrella_destino: Estrella de destino con sus propiedades
        max_age: Edad máxima del burro
    
    Returns:
        Nuevo estado o None si muere
    """
    nuevo_estado = estado.copy()
    
    # REQUERIMIENTO 2.0.b: Factor de consumo de energía (debe coincidir con backend/donkey.py)
    # 0.5 = 50% de la distancia en años luz se consume como energía
    ENERGY_CONSUMPTION_FACTOR = 0.5
    energia_consumida = distancia * ENERGY_CONSUMPTION_FACTOR
    
    # 1. VIAJAR: Consumir energía
    if nuevo_estado.energia < energia_consumida:
        return None  # No puede viajar
    
    nuevo_estado.energia -= energia_consumida
    nuevo_estado.edad += distancia
    
    # Verificar si sobrevive al viaje
    if nuevo_estado.edad >= max_age or nuevo_estado.energia <= 0:
        return None
    
    nuevo_estado.salud = nuevo_estado.calcular_salud()
    
    # 2. AL LLEGAR: Comer pasto si energía < 50%
    if nuevo_estado.necesita_comer() and nuevo_estado.puede_comer():
        # Calcular cuánto tiempo tiene para comer (50% del tiempo de estadía)
        tiempo_disponible_para_comer = estrella_destino.stay_duration * 0.5
        
        # Calcular cuántos kg puede comer
        kg_que_puede_comer = int(tiempo_disponible_para_comer / estrella_destino.time_to_eat)
        kg_que_tiene = int(nuevo_estado.pasto)
        kg_a_comer = min(kg_que_puede_comer, kg_que_tiene)
        
        # Comer pasto
        ganancia_por_kg = nuevo_estado.ganancia_por_kg()
        for _ in range(kg_a_comer):
            if nuevo_estado.energia >= 100:
                break  # Ya está lleno
            
            nuevo_estado.energia += ganancia_por_kg
            nuevo_estado.pasto -= 1
        
        # Clampear energía a 100 máximo
        nuevo_estado.energia = min(100.0, nuevo_estado.energia)
        nuevo_estado.salud = nuevo_estado.calcular_salud()
    
    # 3. INVESTIGAR: Usar el otro 50% del tiempo para investigación
    tiempo_investigacion = estrella_destino.stay_duration * 0.5
    
    # REQUERIMIENTO 2.0: Consumir energía durante la investigación
    # "Y" cantidad de energía por cada "X" tiempo de investigación
    energia_consumida_investigando = tiempo_investigacion * estrella_destino.research_energy_cost
    nuevo_estado.energia -= energia_consumida_investigando
    
    # Aplicar efectos de investigación (health_impact, life_time_impact)
    # REQUERIMIENTO 2.0.a: Estos valores pueden ser modificados por el usuario
    nuevo_estado.energia += estrella_destino.health_impact
    nuevo_estado.edad += estrella_destino.life_time_impact
    
    # Verificar si sobrevive después de investigar
    if nuevo_estado.edad >= max_age or nuevo_estado.energia <= 0:
        return None
    
    nuevo_estado.energia = max(0, min(100, nuevo_estado.energia))
    nuevo_estado.salud = nuevo_estado.calcular_salud()
    
    return nuevo_estado


def encontrar_ruta_optima_con_pasto(
    grafo: GrafoConstelaciones,
    burro: Donkey,
    posicion_inicial: int,
    verbose: bool = False
) -> Dict:
    """
    Encuentra la ruta óptima que maximiza estrellas visitadas con recarga de pasto.
    
    REQUERIMIENTO 2.0: Ruta que permite conocer la mayor cantidad de estrellas
    con el menor gasto posible, considerando recarga automática de pasto.
    
    Args:
        grafo: Grafo de constelaciones
        burro: Burro con estado inicial
        posicion_inicial: ID de la estrella inicial
        verbose: Si True, imprime información de depuración
    
    Returns:
        Dict con la ruta óptima y estadísticas
    """
    # Estado inicial
    estado_inicial = EstadoBurroConPasto(
        energia=burro.donkey_energy,
        edad=burro.age,
        salud=burro.health,
        pasto=burro.grass_in_basement
    )
    
    # Variables para la mejor ruta
    mejor_ruta = [posicion_inicial]
    mejor_distancia = 0.0
    mejor_estado_final = estado_inicial.copy()
    mejor_pasto_usado = 0
    
    # Contador de exploraciones
    exploraciones = [0]
    
    def backtracking(
        posicion_actual: int,
        estado_actual: EstadoBurroConPasto,
        ruta_actual: List[int],
        distancia_actual: float,
        pasto_usado: int,
        visitados: set
    ):
        """Backtracking recursivo con poda."""
        nonlocal mejor_ruta, mejor_distancia, mejor_estado_final, mejor_pasto_usado
        
        exploraciones[0] += 1
        
        # Actualizar mejor ruta si es mejor
        if len(ruta_actual) > len(mejor_ruta):
            mejor_ruta = ruta_actual.copy()
            mejor_distancia = distancia_actual
            mejor_estado_final = estado_actual.copy()
            mejor_pasto_usado = pasto_usado
            
            if verbose:
                print(f"  💫 Nueva mejor: {len(mejor_ruta)} estrellas, pasto usado: {mejor_pasto_usado} kg")
        
        # Empate en estrellas: elegir menor gasto de pasto
        elif len(ruta_actual) == len(mejor_ruta) and pasto_usado < mejor_pasto_usado:
            mejor_ruta = ruta_actual.copy()
            mejor_distancia = distancia_actual
            mejor_estado_final = estado_actual.copy()
            mejor_pasto_usado = pasto_usado
        
        # Explorar vecinos
        vertice_actual = grafo.get_vertex(posicion_actual)
        if not vertice_actual:
            return
        
        vecinos = vertice_actual.get_connections()
        
        for vecino_vertex, distancia in vecinos.items():
            vecino_id = vecino_vertex.id
            
            # Poda 1: No visitar estrellas ya visitadas
            if vecino_id in visitados:
                continue
            
            estrella_destino = grafo.obtener_estrella(vecino_id)
            if not estrella_destino:
                continue
            
            # Guardar estado del pasto antes del viaje
            pasto_antes = estado_actual.pasto
            
            # Simular viaje con posible recarga de pasto
            nuevo_estado = simular_viaje_con_pasto(
                estado_actual,
                distancia,
                estrella_destino,
                burro.max_age
            )
            
            # Poda 2: Si no sobrevive, no explorar
            if nuevo_estado is None or not nuevo_estado.esta_vivo(burro.max_age):
                continue
            
            # Calcular pasto consumido en este viaje
            pasto_consumido = int(pasto_antes - nuevo_estado.pasto)
            
            # Recursión
            nueva_ruta = ruta_actual + [vecino_id]
            nuevo_visitados = visitados | {vecino_id}
            
            backtracking(
                vecino_id,
                nuevo_estado,
                nueva_ruta,
                distancia_actual + distancia,
                pasto_usado + pasto_consumido,
                nuevo_visitados
            )
    
    # Iniciar búsqueda
    if verbose:
        print(f"\n{'='*70}")
        print(f"🔍 BUSCANDO RUTA ÓPTIMA CON RECARGA DE PASTO (Req. 2.0)")
        print(f"{'='*70}")
        print(f"📍 Posición inicial: {posicion_inicial}")
        print(f"⚡ Energía inicial: {estado_inicial.energia:.1f}")
        print(f"🌾 Pasto disponible: {estado_inicial.pasto:.0f} kg")
        print(f"💚 Salud inicial: {estado_inicial.salud}")
        print(f"{'='*70}\n")
    
    backtracking(
        posicion_inicial,
        estado_inicial,
        [posicion_inicial],
        0.0,
        0,
        {posicion_inicial}
    )
    
    if verbose:
        print(f"\n{'='*70}")
        print(f"✅ BÚSQUEDA COMPLETADA")
        print(f"{'='*70}")
        print(f"🔢 Exploraciones: {exploraciones[0]}")
        print(f"⭐ Estrellas visitadas: {len(mejor_ruta)}")
        print(f"🌾 Pasto usado: {mejor_pasto_usado} kg")
        print(f"📏 Distancia total: {mejor_distancia:.1f} ly")
        print(f"⚡ Energía final: {mejor_estado_final.energia:.1f}")
        print(f"🌾 Pasto restante: {mejor_estado_final.pasto:.0f} kg")
        print(f"{'='*70}\n")
    
    return {
        'ruta': mejor_ruta,
        'distancia_total': mejor_distancia,
        'estrellas_visitadas': len(mejor_ruta),
        'pasto_usado': mejor_pasto_usado,
        'estado_final': {
            'energia': mejor_estado_final.energia,
            'edad': mejor_estado_final.edad,
            'salud': mejor_estado_final.salud,
            'pasto': mejor_estado_final.pasto
        },
        'exploraciones': exploraciones[0]
    }
