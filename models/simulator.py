"""
Simulador de viaje.
Responsabilidad: Mantener estado del viaje y coordinar acciones.
"""

from models.constellation import GrafoConstelaciones
from models.donkey import Donkey
from models.star import Estrella
from models.travel_manager import TravelManager
from algorithms.dijkstra import obtener_estrellas_alcanzables


class SimuladorViaje:
    """
    Coordina el viaje del burro por las constelaciones.
    Mantiene el estado del viaje (posición, historial, distancia).
    """
    
    def __init__(self, grafo: GrafoConstelaciones, donkey: Donkey, posicion_inicial: int):
        self.grafo = grafo
        self.donkey = donkey
        self.posicion_actual = posicion_inicial
        self.historial_viaje = [posicion_inicial]
        self.distancia_total = 0.0
        self.travel_manager = TravelManager(grafo, donkey)
    
    def obtener_estrella_actual(self) -> Estrella:
        """Obtiene la estrella donde está el burro actualmente."""
        return self.grafo.obtener_estrella(self.posicion_actual)
    
    def mostrar_opciones(self):
        """Muestra las estrellas alcanzables con la energía actual del burro."""
        print(f"\n{'='*60}")
        print(f"🐴 ESTADO DEL BURRO: {self.donkey.name}")
        print(f"{'='*60}")
        
        estrella_actual = self.obtener_estrella_actual()
        print(f"📍 Posición actual: {estrella_actual.label} (ID: {self.posicion_actual})")
        print(f"⚡ Energía: {self.donkey.donkey_energy:.2f}")
        print(f"💚 Salud: {self.donkey.health}")
        print(f"🌾 Pasto en sótano: {self.donkey.grass_in_basement} kg")
        print(f"🎂 Edad: {self.donkey.age:.2f} años (máx: {self.donkey.max_age})")
        print(f"📏 Distancia total recorrida: {self.distancia_total:.2f} ly")
        
        # Obtener estrellas alcanzables
        alcanzables = obtener_estrellas_alcanzables(
            self.grafo,
            self.posicion_actual,
            self.donkey.donkey_energy
        )
        
        if not alcanzables:
            print("\n❌ No hay estrellas alcanzables con tu energía actual.")
            print("💡 Intenta comer pasto para recuperar energía.")
            return []
        
        print(f"\n✅ ESTRELLAS ALCANZABLES ({len(alcanzables)}):")
        print(f"{'-'*60}")
        
        for i, opcion in enumerate(alcanzables, 1):
            estrella = self.grafo.obtener_estrella(opcion['id'])
            tipo = "⭐ HIPERGIGANTE" if estrella.hipergigante else "🌟 Normal"
            
            print(f"\n{i}. {estrella.label} (ID: {opcion['id']}) {tipo}")
            print(f"   📏 Distancia: {opcion['distancia']:.2f} ly")
            print(f"   ⚡ Energía necesaria: {opcion['distancia']:.2f}")
            print(f"   🔋 Energía restante: {opcion['energia_restante']:.2f}")
            print(f"   🛤️  Camino: {' → '.join(map(str, opcion['camino']))}")
            
            # Mostrar efectos de investigación
            effects = estrella.get_investigation_effects()
            if effects['health_impact'] != 0 or effects['life_time_impact'] != 0:
                print(f"   🔬 Efectos: {effects['description']}")
            
            if estrella.hipergigante:
                print(f"   🎁 Bonus: +50% energía, x2 pasto")
        
        return alcanzables
    
    def viajar_a(self, destino_id: int, verbose: bool = True) -> bool:
        """
        Ejecuta un viaje completo a una estrella destino.
        """
        exito, nueva_posicion, distancia = self.travel_manager.viajar_a(
            self.posicion_actual,
            destino_id,
            verbose
        )
        
        if exito:
            self.posicion_actual = nueva_posicion
            self.historial_viaje.append(nueva_posicion)
            self.distancia_total += distancia
        
        return exito
    
    def comer_pasto(self, cantidad_kg: int = 1) -> bool:
        """Hace que el burro coma pasto del sótano."""
        grass_profit = self.donkey.calculate_grass_profit()
        
        comidos = 0
        for _ in range(cantidad_kg):
            if self.donkey.eat_grass(grass_profit):
                comidos += 1
            else:
                break
        
        if comidos > 0:
            print(f"🌾 El burro comió {comidos} kg de pasto")
            print(f"⚡ Energía actual: {self.donkey.donkey_energy:.2f}")
            print(f"💚 Salud: {self.donkey.health}")
            return True
        
        return False
    
    def investigar_estrella(self, tiempo_investigacion: float = None):
        """
        Investiga la estrella actual aplicando los efectos de salud y tiempo de vida.
        
        Args:
            tiempo_investigacion: Tiempo de investigación en horas. 
                                 Si es None, usa el stayDuration de la estrella.
        """
        estrella = self.obtener_estrella_actual()
        
        # Usar el tiempo de estadía definido en la estrella si no se especifica
        if tiempo_investigacion is None:
            tiempo_investigacion = estrella.stay_duration
        
        print(f"\n🔬 INVESTIGANDO: {estrella.label}")
        print(f"   ⏱️  Tiempo de investigación: {tiempo_investigacion} horas")
        
        # Mostrar efectos esperados
        effects = estrella.get_investigation_effects()
        print(f"   📊 Efectos: {effects['description']}")
        
        # Aplicar investigación
        resultado = self.donkey.stay_of_star(
            time_to_eat_kg=estrella.time_to_eat,
            time_of_stance=tiempo_investigacion,
            health_impact=estrella.health_impact,
            life_time_impact=estrella.life_time_impact,
        )
        
        if resultado:
            print(f"   ❌ {resultado}")
            return False
        
        print(f"   ✅ Investigación completada")
        return True
    
    def obtener_resumen_viaje(self) -> dict:
        """Genera un resumen del viaje."""
        return {
            'estrellas_visitadas': len(self.historial_viaje),
            'distancia_total': self.distancia_total,
            'energia_actual': self.donkey.donkey_energy,
            'salud': self.donkey.health,
            'edad': self.donkey.age,
            'pasto_restante': self.donkey.grass_in_basement,
            'historial': self.historial_viaje,
            'vivo': self.donkey.alive,
        }