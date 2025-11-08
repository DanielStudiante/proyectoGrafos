from models.vertex import GrafoConstelaciones
from models.donkey import Donkey
from models.star import Estrella
from algorithms.dijkstra import encontrar_camino_mas_corto, obtener_estrellas_alcanzables

class SimuladorViaje:
    """
    Coordina el viaje del burro por las constelaciones.
    Integra la lógica de Donkey con el grafo de estrellas.
    """
    
    def __init__(self, grafo: GrafoConstelaciones, donkey: Donkey, posicion_inicial: int):
        self.grafo = grafo
        self.donkey = donkey
        self.posicion_actual = posicion_inicial
        self.historial_viaje = [posicion_inicial]
        self.distancia_total = 0.0
    
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
            
            if estrella.hipergigante:
                print(f"   🎁 Bonus: +50% energía, x2 pasto")
        
        return alcanzables
    
    def viajar_a(self, destino_id: int, verbose: bool = True) -> bool:
        """
        Ejecuta un viaje completo a una estrella destino.
        Usa el método trip() de Donkey para aplicar daño.
        """
        if not self.donkey.alive:
            print("❌ El burro está muerto. No puede viajar.")
            return False
        
        # Planificar ruta
        resultado = encontrar_camino_mas_corto(
            self.grafo,
            self.posicion_actual,
            destino_id,
            verbose=False
        )
        
        if not resultado or not resultado['existe']:
            if verbose:
                print(f"❌ No hay ruta disponible a la estrella {destino_id}")
            return False
        
        if resultado['distancia'] > self.donkey.donkey_energy:
            if verbose:
                print(f"❌ Energía insuficiente.")
                print(f"   Necesitas: {resultado['distancia']:.2f}")
                print(f"   Tienes: {self.donkey.donkey_energy:.2f}")
            return False
        
        # Ejecutar viaje por pasos
        if verbose:
            print(f"\n🚀 INICIANDO VIAJE")
            print(f"{'-'*60}")
        
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
            
            # Usar método trip() de Donkey
            resultado_viaje = self.donkey.trip(
                distance=paso['peso'],
                time_to_eat_kg=estrella_destino.time_to_eat,
                time_of_stance=0,  # Se manejará después
                is_star=es_misma_constelacion
            )
            
            if resultado_viaje:
                if verbose:
                    print(f"   ❌ {resultado_viaje}")
                return False
            
            # Actualizar posición
            self.posicion_actual = paso['hasta']
            self.historial_viaje.append(paso['hasta'])
            self.distancia_total += paso['peso']
            
            if verbose:
                print(f"   ⚡ Energía restante: {self.donkey.donkey_energy:.2f}")
                print(f"   💚 Salud: {self.donkey.health}")
        
        # Llegada a la estrella destino
        estrella_destino = self.grafo.obtener_estrella(destino_id)
        estrella_destino.marcar_visitada()
        
        if verbose:
            print(f"\n✅ LLEGASTE A: {estrella_destino.label}")
            
            # Verificar si es hipergigante
            if estrella_destino.hipergigante:
                print(f"\n⭐ ¡ESTRELLA HIPERGIGANTE!")
                self.donkey.hyper_star(0)  # Aplicar bonus
                print(f"   🎁 Energía: {self.donkey.donkey_energy:.2f} (+50%)")
                print(f"   🌾 Pasto: {self.donkey.grass_in_basement} kg (x2)")
        
        return True
    
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
    
    def investigar_estrella(self, tiempo_investigacion: float = 5.0):
        """
        Investiga la estrella actual.
        Implementar lógica de investigación según el proyecto.
        """
        estrella = self.obtener_estrella_actual()
        
        print(f"\n🔬 INVESTIGANDO: {estrella.label}")
        print(f"   ⏱️  Tiempo de investigación: {tiempo_investigacion} horas")
        
        # Aquí va la lógica de investigación
        # (ganancia de conocimiento, efectos sobre el burro, etc.)
        
        print(f"   ✅ Investigación completada")
    
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