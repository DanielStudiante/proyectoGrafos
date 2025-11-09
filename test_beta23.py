"""Test para analizar el viaje a Beta23"""
from models.donkey import Donkey

print("=" * 60)
print("  ANÁLISIS: ¿Por qué no puedes viajar a Beta23?")
print("=" * 60)

# Configuración inicial del burro
d = Donkey('Platero', 12, 3567, 100, 300)

print(f"\n📊 ESTADO INICIAL:")
print(f"   Energía: {d.donkey_energy}")
print(f"   Salud: {d.health}")
print(f"   Pasto disponible: {d.grass_in_basement} kg")
print(f"   Edad: {d.age} años luz")

print(f"\n🎯 OBJETIVO:")
print(f"   Destino: Beta23 (ID: 2)")
print(f"   Distancia desde Alpha1: 120 años luz")
print(f"   Energía requerida: 120")

print(f"\n❌ PROBLEMA:")
print(f"   Tienes: {d.donkey_energy} energía")
print(f"   Necesitas: 120 energía")
print(f"   Déficit: {120 - d.donkey_energy} energía")

print(f"\n💡 SOLUCIÓN - Comer pasto:")
profit = d.calculate_grass_profit()
print(f"   Ganancia por kg (salud {d.health}): {profit}x")
print(f"   Es decir: {1 * profit:.2f} energía por kg")

# Calcular cuántos kg necesitas
energia_faltante = 120 - d.donkey_energy
kg_necesarios = int(energia_faltante / profit) + 1

print(f"   Necesitas comer aproximadamente: {kg_necesarios} kg de pasto")

print(f"\n🍽️ SIMULACIÓN - Comiendo pasto:")
comidos = 0
while d.donkey_energy < 120 and comidos < 25:
    energia_antes = d.donkey_energy
    if d.eat_grass(d.calculate_grass_profit()):
        comidos += 1
        print(f"   [{comidos}] Comió 1kg → Energía: {energia_antes:.2f} → {d.donkey_energy:.2f}")
    else:
        break

print(f"\n✅ RESULTADO:")
print(f"   Comiste: {comidos} kg de pasto")
print(f"   Energía final: {d.donkey_energy:.2f}")
print(f"   Pasto restante: {d.grass_in_basement} kg")
print(f"   ¿Puedes viajar a Beta23? {'SÍ ✅' if d.donkey_energy >= 120 else 'NO ❌'}")

print(f"\n⚠️ PERO HAY UN PROBLEMA:")
print(f"   La energía tiene un MÁXIMO de 100")
print(f"   Aunque comas pasto, no puedes pasar de 100")
print(f"   Por lo tanto, NUNCA podrás viajar directamente a Beta23")

print(f"\n🔧 SOLUCIONES POSIBLES:")
print(f"   1. Usar una ruta alternativa (si existe)")
print(f"   2. Cambiar la configuración (reducir distancia a Beta23)")
print(f"   3. Aumentar el máximo de energía del burro")
print(f"   4. Encontrar una estrella intermedia")

# Buscar rutas alternativas
print(f"\n🗺️ RUTAS ALTERNATIVAS desde Alpha1:")
print(f"   → Alpha1 a starId 4: distancia 87 (✅ alcanzable)")
print(f"   → Alpha1 a starId 5: distancia 101 (❌ requiere comer)")
print(f"   → Alpha1 a starId 2 (Beta23): distancia 120 (❌ imposible)")

print(f"\n📋 CONCLUSIÓN:")
print(f"   {'='*56}")
print(f"   ESTÁ MAL ❌")
print(f"   {'='*56}")
print(f"   El diseño del juego tiene un PROBLEMA:")
print(f"   - Energía máxima: 100")
print(f"   - Distancia a Beta23: 120")
print(f"   - Es MATEMÁTICAMENTE IMPOSIBLE llegar")
print(f"   ")
print(f"   RECOMENDACIÓN:")
print(f"   Cambiar en config.json la distancia de Alpha1 → Beta23")
print(f"   De 120 → 95 (o menos)")
print("=" * 60)
