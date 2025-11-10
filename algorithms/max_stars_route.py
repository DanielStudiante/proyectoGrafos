"""
Algoritmo para encontrar la ruta que permita visitar la mayor cantidad de estrellas.

REQUERIMIENTO 1.2: Dada una estrella origen y las condiciones iniciales del burro,
proponer la ruta que le permitirá conocer la mayor cantidad de estrellas antes de morir.

Este algoritmo utiliza backtracking con poda para explorar todas las rutas posibles
y encontrar la que maximiza el número de estrellas visitadas.
"""

from typing import List, Dict, Tuple, Optional
from backend.donkey import Donkey
from backend.constellation import GrafoConstelaciones
import copy


class EstadoBurro:
    """Representa el estado del burro en un momento dado."""
    
    def __init__(self, energia: float, edad: float, salud: str, pasto: float):
        self.energia = energia
        self.edad = edad
        self.salud = salud
        self.pasto = pasto
    
    def esta_vivo(self) -> bool:
        """Verifica si el burro está vivo."""
        return self.salud != "Muerto" and self.edad < 3567
    
    def puede_viajar(self, distancia: float) -> bool:
        """Verifica si el burro tiene energía suficiente para viajar."""
        return self.energia >= distancia and self.esta_vivo()
    
    def copy(self):
        """Crea una copia del estado."""
        return EstadoBurro(self.energia, self.edad, self.salud, self.pasto)


def calcular_salud(energia: float) -> str:
    """
    Calcula el estado de salud basado en la energía.
    Cada 25% de energía representa un nivel de salud.
    """
    if energia <= 0:
        return "Muerto"
    elif energia <= 25:
        return "Moribundo"
    elif energia <= 50:
        return "Mala"
    elif energia <= 75:
        return "Buena"
    else:
        return "Excelente"


def simular_viaje(estado: EstadoBurro, distancia: float, estrella_destino) -> Optional[EstadoBurro]:
    """
    Simula el viaje a una estrella y retorna el nuevo estado.
    
    Args:
        estado: Estado actual del burro
        distancia: Distancia a viajar
        estrella_destino: Estrella destino con sus efectos
    
    Returns:
        Nuevo estado del burro o None si muere en el viaje
    """
    nuevo_estado = estado.copy()
    
    # Factor de reducción de consumo de energía (debe coincidir con backend/donkey.py)
    ENERGY_CONSUMPTION_FACTOR = 0.2
    energia_consumida = distancia * ENERGY_CONSUMPTION_FACTOR
    
    # Verificar si puede viajar
    if not nuevo_estado.puede_viajar(energia_consumida):
        return None
    
    # Consumir energía por el viaje
    nuevo_estado.energia -= energia_consumida
    
    # Incrementar edad por el viaje (distancia en años luz = edad)
    nuevo_estado.edad += distancia
    
    # Verificar si sigue vivo después del viaje
    if nuevo_estado.edad >= 3567 or nuevo_estado.energia <= 0:
        nuevo_estado.salud = "Muerto"
        return None
    
    # Actualizar salud basada en energía
    nuevo_estado.salud = calcular_salud(nuevo_estado.energia)
    
    return nuevo_estado


def encontrar_ruta_maxima_estrellas(
    grafo: GrafoConstelaciones,
    burro: Donkey,
    posicion_inicial: int,
    verbose: bool = False
) -> Dict:
    """
    Encuentra la ruta que permite visitar la mayor cantidad de estrellas
    con los valores iniciales del burro (sin recargar energía ni comer).
    
    REQUERIMIENTO 1.2: Calcula la ruta óptima usando solo valores iniciales.
    
    Args:
        grafo: Grafo de constelaciones
        burro: Burro con estado inicial
        posicion_inicial: ID de la estrella inicial
        verbose: Si True, imprime información de depuración
    
    Returns:
        Dict con:
            - 'ruta': Lista de IDs de estrellas en orden de visita
            - 'distancia_total': Distancia total recorrida
            - 'estrellas_visitadas': Número de estrellas visitadas
            - 'estado_final': Estado del burro al final
    """
    # Estado inicial
    estado_inicial = EstadoBurro(
        energia=burro.donkey_energy,
        edad=burro.age,
        salud=burro.health,
        pasto=burro.grass_in_basement
    )
    
    # Variables para guardar la mejor ruta
    mejor_ruta = [posicion_inicial]
    mejor_distancia = 0.0
    mejor_estado_final = estado_inicial.copy()
    
    # Contador de exploraciones (para debugging)
    exploraciones = [0]
    
    def backtracking(
        posicion_actual: int,
        estado_actual: EstadoBurro,
        ruta_actual: List[int],
        distancia_actual: float,
        visitados: set
    ):
        """
        Función recursiva para explorar todas las rutas posibles.
        
        Usa backtracking con poda para optimizar la búsqueda.
        """
        nonlocal mejor_ruta, mejor_distancia, mejor_estado_final
        
        exploraciones[0] += 1
        
        # Si esta ruta es mejor (más estrellas), actualizar mejor ruta
        if len(ruta_actual) > len(mejor_ruta):
            mejor_ruta = ruta_actual.copy()
            mejor_distancia = distancia_actual
            mejor_estado_final = estado_actual.copy()
            
            if verbose:
                print(f"  💫 Nueva mejor ruta: {len(mejor_ruta)} estrellas, distancia: {mejor_distancia:.1f} ly")
        
        # Si empatan en estrellas, elegir la de menor distancia
        elif len(ruta_actual) == len(mejor_ruta) and distancia_actual < mejor_distancia:
            mejor_ruta = ruta_actual.copy()
            mejor_distancia = distancia_actual
            mejor_estado_final = estado_actual.copy()
        
        # Obtener vecinos de la estrella actual
        vertice_actual = grafo.get_vertex(posicion_actual)
        if not vertice_actual:
            return
        
        vecinos = vertice_actual.get_connections()
        
        # Explorar cada vecino
        for vecino_vertex, distancia in vecinos.items():
            vecino_id = vecino_vertex.id
            
            # Poda 1: No visitar estrellas ya visitadas
            if vecino_id in visitados:
                continue
            
            # Obtener estrella destino
            estrella_destino = grafo.obtener_estrella(vecino_id)
            if not estrella_destino:
                continue
            
            # Simular el viaje
            nuevo_estado = simular_viaje(estado_actual, distancia, estrella_destino)
            
            # Poda 2: Si el burro no sobrevive al viaje, no explorar
            if nuevo_estado is None or not nuevo_estado.esta_vivo():
                continue
            
            # Poda 3: Si no puede viajar, no explorar
            if not estado_actual.puede_viajar(distancia):
                continue
            
            # Recursión: explorar desde el vecino
            nueva_ruta = ruta_actual + [vecino_id]
            nuevo_visitados = visitados | {vecino_id}
            
            backtracking(
                vecino_id,
                nuevo_estado,
                nueva_ruta,
                distancia_actual + distancia,
                nuevo_visitados
            )
    
    # Iniciar búsqueda desde posición inicial
    if verbose:
        print(f"\n{'='*60}")
        print(f"🔍 BUSCANDO RUTA ÓPTIMA")
        print(f"{'='*60}")
        print(f"📍 Posición inicial: {posicion_inicial}")
        print(f"⚡ Energía inicial: {estado_inicial.energia:.1f}")
        print(f"💚 Salud inicial: {estado_inicial.salud}")
        print(f"🎂 Edad inicial: {estado_inicial.edad:.1f} años luz")
        print(f"{'='*60}\n")
    
    backtracking(
        posicion_inicial,
        estado_inicial,
        [posicion_inicial],
        0.0,
        {posicion_inicial}
    )
    
    if verbose:
        print(f"\n{'='*60}")
        print(f"✅ BÚSQUEDA COMPLETADA")
        print(f"{'='*60}")
        print(f"🔢 Exploraciones realizadas: {exploraciones[0]}")
        print(f"⭐ Mejor ruta: {' → '.join(map(str, mejor_ruta))}")
        print(f"📊 Estrellas visitadas: {len(mejor_ruta)}")
        print(f"📏 Distancia total: {mejor_distancia:.1f} ly")
        print(f"⚡ Energía final: {mejor_estado_final.energia:.1f}")
        print(f"💚 Salud final: {mejor_estado_final.salud}")
        print(f"🎂 Edad final: {mejor_estado_final.edad:.1f} años luz")
        print(f"{'='*60}\n")
    
    return {
        'ruta': mejor_ruta,
        'distancia_total': mejor_distancia,
        'estrellas_visitadas': len(mejor_ruta),
        'estado_final': {
            'energia': mejor_estado_final.energia,
            'edad': mejor_estado_final.edad,
            'salud': mejor_estado_final.salud,
            'pasto': mejor_estado_final.pasto
        },
        'exploraciones': exploraciones[0]
    }


def obtener_nombres_ruta(grafo: GrafoConstelaciones, ruta_ids: List[int]) -> List[str]:
    """
    Convierte una lista de IDs de estrellas a sus nombres.
    
    Args:
        grafo: Grafo de constelaciones
        ruta_ids: Lista de IDs de estrellas
    
    Returns:
        Lista de nombres de estrellas
    """
    nombres = []
    for star_id in ruta_ids:
        estrella = grafo.obtener_estrella(star_id)
        if estrella:
            nombres.append(estrella.label)
        else:
            nombres.append(f"ID:{star_id}")
    return nombres
