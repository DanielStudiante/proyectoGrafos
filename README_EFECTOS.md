# Sistema de Efectos de Investigación

## ¿Qué se implementó?

Cada estrella puede tener **efectos** que afectan al burro cuando investiga:
- **`healthImpact`**: Energía ganada (+) o perdida (-)
- **`lifeTimeImpact`**: Años luz ganados (+) o perdidos (-)

## Uso

### 1. Configurar en JSON (data/config.json)
```json
{
  "id": 1,
  "label": "Alpha1",
  "healthImpact": -2.5,      // Pierde energía
  "lifeTimeImpact": -10,     // Envejece
  ...
}
```

### 2. Ejecutar simulador
```bash
python main.py
```

El sistema te preguntará si quieres modificar los efectos antes de empezar.

### 3. Durante el viaje

Los efectos se aplican automáticamente cuando el burro investiga:
```
🔬 El burro investiga la estrella...
💔 La investigación causó daño: -2.5 de energía
⚠️ La investigación consumió 10.0 años luz de vida
```

## Archivos modificados

- `models/star.py` - Atributos health_impact, life_time_impact
- `models/donkey.py` - Método stay_of_star() aplica efectos
- `models/simulator.py` - Integración con viajes
- `models/vertex.py` - Soporte en agregar_estrella()
- `data/config.json` - Valores por defecto
- `main.py` - **Simulador completo con configuración**

## Ejemplo

```python
from models.vertex import GrafoConstelaciones

grafo = cargar_grafo_desde_json()

# Modificar una estrella
estrella = grafo.obtener_estrella(1)
estrella.set_health_impact(-5.0)     # Peligrosa
estrella.set_life_time_impact(-20.0)

# O hacerlo antes del viaje con la función incluida
configurar_efectos_estrella(grafo)
```

¡Listo! Simple y funcional. 🚀
