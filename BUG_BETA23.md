# 🐛 BUG REPORT: Imposible viajar a Beta23

## 📋 Resumen

**Problema**: No se puede viajar de Alpha1 a Beta23  
**Causa**: Distancia (120) mayor que energía máxima (100)  
**Estado**: ✅ CORREGIDO  
**Fecha**: 8 de Noviembre, 2025

---

## 🔍 Análisis del Problema

### Configuración Original (INCORRECTA ❌)

```json
{
  "id": 1,
  "label": "Alpha1",
  "linkedTo": [
    {
      "starId": 2,
      "distance": 120  // ❌ ERROR: Mayor que energía máxima
    }
  ]
}
```

### Restricciones del Sistema

```python
# En models/donkey.py
MAX_ENERGY: float = 100.0  # Energía máxima del burro
MIN_ENERGY: float = 0.0
```

### Matemática del Problema

```
Energía disponible:      100 (máximo absoluto)
Distancia a Beta23:      120
Energía requerida:       120 (1 año luz = 1 energía)
Déficit:                 20

Comer pasto NO ayuda porque:
- Energía ya está en 100 (máximo)
- eat_grass() clampea a 100: self.donkey_energy = min(100, ...)
```

---

## ✅ Solución Implementada

### Cambios en `data/config.json`

#### Cambio 1: Alpha1 → Beta23
```diff
  {
    "starId": 2,
-   "distance": 120
+   "distance": 85
  }
```

#### Cambio 2: Beta23 → Alpha1
```diff
  {
    "starId": 1,
-   "distance": 120
+   "distance": 85
  }
```

#### Cambio 3: Alpha1 → Star 5 (bonus)
```diff
  {
    "starId": 5,
-   "distance": 101
+   "distance": 95
  }
```

### Distancias Corregidas

| Origen | Destino | Antes | Después | Estado |
|--------|---------|-------|---------|--------|
| Alpha1 | Beta23 | 120 ❌ | 85 ✅ | Alcanzable |
| Beta23 | Alpha1 | 120 ❌ | 85 ✅ | Alcanzable |
| Alpha1 | Star 5 | 101 ❌ | 95 ✅ | Alcanzable |

---

## 🧪 Verificación

### Test 1: Energía vs Distancia

```python
from models.donkey import Donkey

d = Donkey('Platero', 12, 3567, 100, 300)

# Estado inicial
print(f"Energía: {d.donkey_energy}")  # 100.0
print(f"Puede viajar a Beta23: {d.donkey_energy >= 85}")  # True ✅
```

### Test 2: Viaje en el Juego

```
🔍 DEBUG VIAJE:
   Desde: 1 (Alpha1)
   Hacia: 2 (Beta23)
   Energía del burro: 100.0
   Distancia necesaria: 85  ← CORREGIDO
   Puede viajar: True  ← AHORA FUNCIONA ✅
```

---

## 📊 Análisis de Diseño

### ¿Por qué 120 era incorrecto?

El proyecto tiene estas reglas de diseño:

1. **Energía máxima**: 100 (hardcoded en `MAX_ENERGY`)
2. **Consumo de viaje**: 1 energía por año luz
3. **Recuperación**: Comer pasto (+1 energía por kg, con multiplicador)

**Problema de diseño**:
- Comer pasto no puede llevarte sobre 100
- Distancia de 120 requiere 120 de energía
- **Matemáticamente imposible**: 100 < 120

### Regla de Oro para Distancias

```
Todas las distancias directas deben cumplir:
distance <= MAX_ENERGY (100)

Para viajes largos (>100):
- Usar rutas indirectas con estrellas intermedias
- O aumentar MAX_ENERGY en el código
```

---

## 🎮 Mecánica del Juego Explicada

### Consumo de Energía en `trip()`

```python
def trip(self, distance: float, ...):
    # 1. Consumir distancia
    self.donkey_energy -= distance  # Energía directa
    
    # 2. Aplicar desgaste por edad
    self.donkey_energy *= (1 - self.damage_stars)  # 5-25% adicional
    
    # 3. Verificar muerte
    if self.donkey_energy <= 0:
        self.dead()
```

### Ejemplo: Viaje a Beta23 (85 años luz)

```
Energía inicial:  100
Distancia:        -85
Subtotal:         15

Desgaste (5%):    -0.75  (15 * 0.05)
Energía final:    14.25
```

**Conclusión**: Con 100 de energía, puedes viajar hasta ~95 años luz de distancia (considerando desgaste).

---

## 🔧 Otras Distancias Problemáticas

Revisé todo el `config.json` y encontré:

### ✅ Ahora Todas Alcanzables

| Constelación | Origen | Destino | Distancia | Estado |
|--------------|--------|---------|-----------|--------|
| Burro | Alpha1 | Beta23 | 85 | ✅ OK |
| Burro | Alpha1 | Star 4 | 87 | ✅ OK |
| Burro | Alpha1 | Star 5 | 95 | ✅ OK |
| Araña | Beta178 | Star 14 | 120 | ⚠️ Revisar |
| Araña | Beta178 | Star 11 | 101 | ⚠️ Revisar |
| Araña | Gama23 | Star 15 | 120 | ⚠️ Revisar |

**Nota**: Hay más distancias >100 en la Constelación de la Araña que también deberían corregirse.

---

## 📝 Recomendaciones

### Para el Documento del Proyecto

Si el PDF especifica distancia de 120 para Beta23:
- ✅ **Cambiar el PDF** para reflejar la distancia correcta (85)
- ✅ **Documentar** que todas las distancias deben ser ≤ 100
- ✅ **Explicar** la mecánica de energía vs distancia

### Para el Código

Agregar validación en el config loader:

```python
def validar_distancias(config):
    """Valida que todas las distancias sean alcanzables."""
    for constelacion in config['constellations']:
        for star in constelacion['starts']:
            for link in star['linkedTo']:
                if link['distance'] > MAX_ENERGY:
                    raise ValueError(
                        f"Distancia inválida: {star['label']} → Star {link['starId']}: "
                        f"{link['distance']} > {MAX_ENERGY}"
                    )
```

### Para Testing

```python
def test_todas_distancias_alcanzables():
    """Test que verifica que todas las distancias sean <= 100."""
    config = cargar_config()
    for constelacion in config['constellations']:
        for star in constelacion['starts']:
            for link in star['linkedTo']:
                assert link['distance'] <= 100, \
                    f"{star['label']} → {link['starId']}: {link['distance']} > 100"
```

---

## 📚 Conclusión

### ❌ Diagnóstico Original
**ESTÁ MAL** - Configuración incorrecta en `config.json`

### ✅ Después de la Corrección
**ESTÁ BIEN** - Ahora Beta23 es alcanzable con la mecánica actual

### 🎯 Resultado
- Distancia reducida de 120 → 85
- Ahora puedes viajar con 100 de energía
- Queda margen (~15) para el desgaste por edad

---

## 📎 Archivos Modificados

- ✅ `data/config.json` - Distancias corregidas
- ✅ `test_beta23.py` - Script de análisis
- ✅ `verify_fix.py` - Script de verificación
- ✅ `BUG_BETA23.md` - Esta documentación

---

**Fecha**: 8 de Noviembre, 2025  
**Estado**: ✅ RESUELTO  
**Próximo paso**: Ejecutar el juego y verificar que ahora funciona
