"""
Gestor de viajes.
Responsabilidad: Coordinar viajes entre estrellas.
"""

from backend.constellation import GrafoConstelaciones
from backend.donkey import Donkey
from algorithms.dijkstra import encontrar_camino_mas_corto


class TravelManager:
    """Gestiona la ejecución de viajes entre estrellas."""
    
    def __init__(self, grafo: GrafoConstelaciones, donkey: Donkey):
        self.grafo = grafo
        self.donkey = donkey
    
    def viajar_a(self, origen: int, destino: int, verbose: bool = True) -> tuple:
        """
        Ejecuta un viaje completo a una estrella destino.
        
        REQUERIMIENTO: Una estrella solo puede ser visitada una única vez.
        
        Returns:
            tuple: (exito: bool, nueva_posicion: int, distancia_recorrida: float)
        """
        if not self.donkey.alive:
            if verbose:
                print("❌ El burro está muerto. No puede viajar.")
            return (False, origen, 0.0)
        
        # REQUERIMIENTO: Verificar que la estrella destino no haya sido visitada
        estrella_destino = self.grafo.obtener_estrella(destino)
        if estrella_destino and estrella_destino.visitada:
            if verbose:
                print(f"❌ La estrella {estrella_destino.label} ya fue visitada anteriormente.")
                print(f"   REQUERIMIENTO: Una estrella solo puede ser visitada una única vez.")
            return (False, origen, 0.0)
        
        # Planificar ruta
        resultado = encontrar_camino_mas_corto(
            self.grafo,
            origen,
            destino,
            verbose=False
        )
        
        if not resultado or not resultado['existe']:
            if verbose:
                print(f"❌ No hay ruta disponible a la estrella {destino}")
            return (False, origen, 0.0)
        
        # ELIMINADA VALIDACIÓN: Permitir viaje aunque no haya energía suficiente
        # El burro puede morir durante el viaje (Requerimiento 1.2)
        
        # Ejecutar viaje por pasos
        if verbose:
            print(f"\n🚀 INICIANDO VIAJE")
            print(f"{'-'*60}")
        
        distancia_total = 0.0
        posicion_actual = origen
        
        for paso in resultado['pasos']:
            estrella_origen = self.grafo.obtener_estrella(paso['desde'])
            estrella_destino = self.grafo.obtener_estrella(paso['hasta'])
            
            if verbose:
                print(f"\n📍 {estrella_origen.label} → {estrella_destino.label}")
                print(f"   Distancia: {paso['peso']:.2f} ly")
            
            # Determinar si viaja entre constelaciones
            es_misma_constelacion = bool(
                set(estrella_origen.constelaciones) & 
                set(estrella_destino.constelaciones)
            )
            
            # Usar método trip() de Donkey con efectos de investigación
            resultado_viaje = self.donkey.trip(
                distance=paso['peso'],
                time_to_eat_kg=estrella_destino.time_to_eat,
                time_of_stance=0,  # Se manejará después
                is_star=es_misma_constelacion,
                health_impact=estrella_destino.health_impact,
                life_time_impact=estrella_destino.life_time_impact,
                research_energy_cost=estrella_destino.research_energy_cost,
            )
            
            if resultado_viaje:
                if verbose:
                    print(f"   ❌ {resultado_viaje}")
                return (False, posicion_actual, distancia_total)
            
            # Actualizar posición
            posicion_actual = paso['hasta']
            distancia_total += paso['peso']
            
            if verbose:
                print(f"   ⚡ Energía restante: {self.donkey.donkey_energy:.2f}")
                print(f"   💚 Salud: {self.donkey.health}")
        
        # Llegada a la estrella destino
        estrella_destino = self.grafo.obtener_estrella(destino)
        estrella_destino.marcar_visitada()
        
        if verbose:
            print(f"\n✅ LLEGASTE A: {estrella_destino.label}")
            
            # Verificar si es hipergigante
            if estrella_destino.hipergigante:
                print(f"\n⭐ ¡ESTRELLA HIPERGIGANTE!")
                self.donkey.hyper_star(0)  # Aplicar bonus
                print(f"   🎁 Energía: {self.donkey.donkey_energy:.2f} (+50%)")
                print(f"   🌾 Pasto: {self.donkey.grass_in_basement} kg (x2)")
        
        return (True, posicion_actual, distancia_total)
