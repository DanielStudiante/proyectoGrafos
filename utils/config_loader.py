"""
Cargador de configuración.
Responsabilidad: Cargar datos desde JSON.
"""

import json
from models.constellation import GrafoConstelaciones
from models.donkey import Donkey


def cargar_grafo_desde_json(ruta: str = "data/config.json") -> GrafoConstelaciones:
    """
    Carga un grafo de constelaciones desde un archivo JSON.
    
    Args:
        ruta: Ruta al archivo JSON
        
    Returns:
        GrafoConstelaciones con estrellas y conexiones
    """
    with open(ruta, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    grafo = GrafoConstelaciones()
    
    # Procesar constelaciones y estrellas
    for constellation in data.get('constellations', []):
        constellation_name = constellation.get('name', 'Sin nombre')
        
        # Agregar estrellas de la constelación
        for star_data in constellation.get('starts', []):  # Nota: JSON usa "starts" (typo)
            coords = star_data.get('coordenates', {})
            grafo.agregar_estrella(
                id=star_data['id'],
                label=star_data.get('label', str(star_data['id'])),
                x=coords.get('x', 0),
                y=coords.get('y', 0),
                radius=star_data.get('radius', 1.0),
                constelaciones=[constellation_name],
                hipergigante=star_data.get('hypergiant', False),
                time_to_eat=star_data.get('timeToEat', 1.0),
                stay_duration=star_data.get('stayDuration', 5.0),
                amount_of_energy=star_data.get('amountOfEnergy', 10.0),
                health_impact=star_data.get('healthImpact', 0.0),
                life_time_impact=star_data.get('lifeTimeImpact', 0.0),
            )
            
            # Agregar aristas desde linkedTo
            for link in star_data.get('linkedTo', []):
                grafo.add_edge(
                    star_data['id'],
                    link['starId'],
                    link.get('distance', 1.0)
                )
    
    return grafo


def crear_burro_desde_json(ruta: str = "data/config.json") -> Donkey:
    """
    Crea un burro desde un archivo JSON.
    
    Args:
        ruta: Ruta al archivo JSON
        
    Returns:
        Donkey con configuración inicial
    """
    with open(ruta, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    return Donkey(
        name="Burro Científico",
        age=data.get('startAge', 0),
        max_age=data.get('deathAge', 3567),
        donkey_energy=data.get('burroenergiaInicial', 100),
        grass_in_basement=data.get('pasto', 300)
    )
