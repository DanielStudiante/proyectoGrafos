"""
Resumen de energía de todas las estrellas
"""
import json

with open('data/config.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("=" * 80)
print("CONFIGURACIÓN DE ENERGÍA DE ESTRELLAS")
print("=" * 80)

for constellation in data['constellations']:
    print(f"\n🌌 {constellation['name']}")
    print("-" * 80)
    
    for star in constellation['starts']:
        print(f"\n⭐ {star['label']} (id={star['id']})")
        print(f"   🌾 Pasto disponible: {star.get('amountOfEnergy', 0)} kg")
        print(f"   ⏱️  Tiempo por kg: {star.get('timeToEat', 1)} horas")
        print(f"   ⏰ Tiempo de estadía: {star.get('stayDuration', 5.0)} horas")
        
        health = star.get('healthImpact', 0)
        if health > 0:
            print(f"   ⚡ Impacto energía: +{health} ✅")
        elif health < 0:
            print(f"   ⚡ Impacto energía: {health} ❌")
        else:
            print(f"   ⚡ Impacto energía: 0 ➖")
        
        lifetime = star.get('lifeTimeImpact', 0)
        if lifetime > 0:
            print(f"   🕐 Impacto vida: +{lifetime} años luz")
        elif lifetime < 0:
            print(f"   🕐 Impacto vida: {lifetime} años luz")
        
        # Calcular cuántos kg puede comer
        tiempo_total = star.get('stayDuration', 5.0)
        tiempo_por_kg = star.get('timeToEat', 1)
        pasto_maximo = star.get('amountOfEnergy', 0)
        
        # Si energía < 50, dedica 50% del tiempo a comer
        tiempo_para_comer_bajo = tiempo_total * 0.5
        kg_con_energia_baja = min(int(tiempo_para_comer_bajo / tiempo_por_kg), pasto_maximo)
        
        print(f"   📊 Si energía < 50: puede comer {kg_con_energia_baja} kg (máx {pasto_maximo} kg)")

print("\n" + "=" * 80)
print(f"ENERGÍA INICIAL DEL BURRO: {data.get('burroenergiaInicial', 100)}")
print(f"PASTO INICIAL EN SÓTANO: {data.get('pasto', 300)} kg")
print("=" * 80)
