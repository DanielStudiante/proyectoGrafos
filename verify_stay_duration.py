"""Verificar que cada estrella tiene su tiempo de estadía definido"""
import json

print("=" * 70)
print("  ✅ VERIFICACIÓN: Tiempo de Estadía por Estrella")
print("=" * 70)

with open('data/config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

print(f"\n📋 CONFIGURACIÓN:\n")

for constelacion in config['constellations']:
    print(f"🌌 {constelacion['name']}")
    print("─" * 70)
    
    for star in constelacion['starts']:
        stay = star.get('stayDuration', '❌ NO DEFINIDO')
        time_eat = star.get('timeToEat', '❌ NO DEFINIDO')
        
        estado = "✅" if 'stayDuration' in star else "❌"
        
        print(f"{estado} {star['label']:15} (ID: {star['id']:2})")
        print(f"   ⏱️  Tiempo de estadía: {stay} horas")
        print(f"   🍽️  Tiempo por kg:     {time_eat} horas")
        
        # Calcular cuántos kg puede comer
        if isinstance(stay, (int, float)) and isinstance(time_eat, (int, float)) and time_eat > 0:
            max_kg = int(stay / time_eat)
            print(f"   📊 Puede comer máximo: {max_kg} kg de pasto")
        
        # Mostrar efectos
        health = star.get('healthImpact', 0)
        life = star.get('lifeTimeImpact', 0)
        
        effects = []
        if health > 0:
            effects.append(f"💚 +{health} energía")
        elif health < 0:
            effects.append(f"💔 {health} energía")
        
        if life > 0:
            effects.append(f"⏰ +{life} años luz")
        elif life < 0:
            effects.append(f"⚠️ {life} años luz")
        
        if effects:
            print(f"   🎯 Efectos: {' | '.join(effects)}")
        
        print()
    
    print()

# Resumen
print("=" * 70)
print("📊 RESUMEN:")
print("=" * 70)

total_stars = sum(len(c['starts']) for c in config['constellations'])
stars_with_stay = sum(
    1 for c in config['constellations'] 
    for s in c['starts'] 
    if 'stayDuration' in s
)

print(f"Total de estrellas:              {total_stars}")
print(f"Con stayDuration definido:       {stars_with_stay} ✅")
print(f"Sin stayDuration (falta):        {total_stars - stars_with_stay} ❌")

if stars_with_stay == total_stars:
    print(f"\n✅ PERFECTO: Todas las estrellas tienen tiempo de estadía definido")
else:
    print(f"\n⚠️  ATENCIÓN: Faltan {total_stars - stars_with_stay} estrellas por configurar")

print("=" * 70)
