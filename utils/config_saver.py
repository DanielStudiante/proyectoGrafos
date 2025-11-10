"""
Utilidad para guardar configuración editada al JSON
"""
import json
from pathlib import Path


def save_grafo_to_json(grafo, ruta="data/config.json"):
    """
    Guarda el estado actual del grafo al archivo JSON.
    
    Args:
        grafo: GrafoConstelaciones con los datos actualizados
        ruta: Ruta al archivo JSON
    """
    # Leer el JSON actual para preservar otros campos
    with open(ruta, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Actualizar solo las estrellas
    for constellation in data['constellations']:
        for star_data in constellation['starts']:
            star_id = star_data['id']
            estrella = grafo.obtener_estrella(star_id)
            
            if estrella:
                # Actualizar campos editables
                star_data['amountOfEnergy'] = estrella.amount_of_energy
                star_data['timeToEat'] = estrella.time_to_eat
                star_data['stayDuration'] = estrella.stay_duration
                star_data['healthImpact'] = estrella.health_impact
                star_data['lifeTimeImpact'] = estrella.life_time_impact
    
    # Guardar con formato bonito
    with open(ruta, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    return True
