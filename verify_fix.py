"""Verificar el cambio en config.json"""
import json

with open('data/config.json') as f:
    config = json.load(f)

alpha1 = config['constellations'][0]['starts'][0]
beta23 = config['constellations'][0]['starts'][1]

print("=" * 60)
print("  ✅ VERIFICACIÓN DE CORRECCIÓN")
print("=" * 60)
print(f"\n🌟 Alpha1 (ID: {alpha1['id']}):")
for link in alpha1['linkedTo']:
    destino = "Beta23" if link['starId'] == 2 else f"Star {link['starId']}"
    estado = "✅ Alcanzable" if link['distance'] <= 100 else "❌ Imposible"
    print(f"   → {destino}: {link['distance']} años luz - {estado}")

print(f"\n🌟 Beta23 (ID: {beta23['id']}):")
for link in beta23['linkedTo']:
    destino = "Alpha1" if link['starId'] == 1 else f"Star {link['starId']}"
    estado = "✅ Alcanzable" if link['distance'] <= 100 else "❌ Imposible"
    print(f"   → {destino}: {link['distance']} años luz - {estado}")

print(f"\n📊 RESULTADO:")
dist_a1_to_b23 = alpha1['linkedTo'][0]['distance']
if dist_a1_to_b23 <= 100:
    print(f"   ✅ CORREGIDO: Ahora puedes viajar a Beta23")
    print(f"   Distancia: {dist_a1_to_b23} (energía máxima: 100)")
else:
    print(f"   ❌ AÚN HAY PROBLEMA: Distancia {dist_a1_to_b23} > 100")

print("=" * 60)
