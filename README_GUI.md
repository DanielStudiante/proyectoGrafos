# 🎮 Interfaz Gráfica - Burro Científico

## 🚀 Inicio Rápido

### Instalación de Pygame
```bash
pip install pygame
```

### Ejecutar el juego
```bash
python play.py
```

## 🎯 Características

### ✨ Interfaz Profesional
- **Arquitectura MVC**: Código organizado y mantenible
- **Sistema de componentes reutilizables**: Botones, paneles, barras de progreso
- **Diseño responsivo**: Todo adaptado a una paleta de colores espacial
- **Animaciones suaves**: Pulsos en estrellas, efectos de brillo
- **Tooltips informativos**: Información al pasar el mouse

### 🎨 Elementos Visuales

#### Panel Izquierdo - Estado del Burro
- ⚡ Barra de energía (con colores dinámicos)
- 💚 Estado de salud actual
- 🌾 Cantidad de pasto disponible
- 🎂 Edad actual / máxima
- 📏 Distancia total recorrida
- 🌟 Posición actual (estrella)

#### Panel Central - Grafo de Constelaciones
- **Estrellas normales**: Círculos blancos
- **Estrellas hipergigantes**: Círculos dorados con borde ⭐
- **Estrella actual**: Azul brillante con pulso animado
- **Estrellas visitadas**: Grises
- **Conexiones**: Líneas grises entre estrellas
- **Camino activo**: Línea azul resaltada con distancias
- **Efectos de brillo**: En hover y estrella actual

#### Panel Derecho Superior - Acciones
- 🚀 **Viajar a Estrella**: Viaja a la estrella seleccionada
- 🍽️ **Comer Pasto**: Consume 5 kg de pasto
- 🔬 **Investigar**: Investiga la estrella actual
- ⚙️ **Configurar**: Configuración (próximamente)

#### Panel Derecho Inferior - Información de Estrella
Cuando seleccionas una estrella muestra:
- Nombre y tipo (Normal/Hipergigante)
- Constelación a la que pertenece
- 📏 Distancia desde posición actual
- ⚡ Energía necesaria para llegar
- 🔬 Efectos de investigación:
  - 💚 Impacto en salud (positivo/negativo)
  - 🎂 Impacto en tiempo de vida (años luz)

#### Panel Izquierdo Inferior - Estrellas Alcanzables
Lista de estrellas que puedes alcanzar con tu energía actual.

## 🎮 Controles

### Mouse
- **Click en estrella**: Selecciona la estrella
- **Hover en estrella**: Muestra tooltip con información
- **Click en botones**: Ejecuta acciones

### Teclado
- **ESPACIO**: Comer pasto rápido
- **I**: Investigar estrella actual
- **ESC**: Salir del juego

## 🎯 Cómo Jugar

1. **Inicio**: El burro comienza en la estrella ID 1
2. **Seleccionar destino**: Click en una estrella para seleccionarla
3. **Ver información**: El panel derecho muestra:
   - Distancia y energía necesaria
   - Efectos de investigación
   - Camino resaltado en el grafo
4. **Viajar**: Click en "🚀 Viajar a Estrella"
5. **Gestionar recursos**:
   - Come pasto si la energía es baja
   - Investiga para aplicar efectos (buenos o malos)
6. **Objetivo**: Explorar el máximo de estrellas sin morir

## 🎨 Sistema de Colores

### Efectos de Salud
- 💚 **Verde**: Efectos positivos en salud
- 💔 **Rojo**: Efectos negativos en salud

### Efectos de Tiempo de Vida
- 💙 **Azul claro**: Ganas años luz (rejuveneces)
- 🧡 **Naranja**: Pierdes años luz (envejeces)

### Barras de Energía
- 🟢 **Verde**: >60% energía
- 🟡 **Amarillo**: 30-60% energía
- 🔴 **Rojo**: <30% energía

## 📊 Sistema de Notificaciones

Las notificaciones aparecen en la parte superior del grafo:
- ✅ **Verde**: Acciones exitosas
- ⚠️ **Rojo**: Errores o advertencias
- ℹ️ **Gris**: Información general

## 🎭 Estados del Juego

### Playing (Jugando)
- Estado normal de juego
- Todas las interacciones activas

### Game Over
- Overlay oscuro con estadísticas finales
- Muestra:
  - Estrellas visitadas
  - Distancia recorrida
  - Edad final

## 🏗️ Arquitectura del Código

```
gui/
├── config.py           # Constantes y configuración
├── components.py       # Componentes UI reutilizables
├── graph_renderer.py   # Renderizado del grafo
├── panels.py          # Paneles de información
└── game.py            # Gestor principal del juego
```

### Componentes Principales

#### `config.py`
- Constantes de ventana, colores, tamaños
- Configuración de animaciones
- Paleta de colores consistente

#### `components.py`
- `Button`: Botones interactivos
- `Panel`: Contenedores
- `ProgressBar`: Barras de progreso
- `InfoLabel`: Etiquetas con iconos
- `Tooltip`: Información al hover
- `Notification`: Sistema de notificaciones

#### `graph_renderer.py`
- `StarRenderer`: Renderiza estrellas individuales
- `ConnectionRenderer`: Renderiza conexiones
- `GraphRenderer`: Gestiona el grafo completo

#### `panels.py`
- `DonkeyInfoPanel`: Info del burro
- `StarInfoPanel`: Info de estrella seleccionada
- `ActionsPanel`: Botones de acción
- `ReachableStarsPanel`: Estrellas alcanzables

#### `game.py`
- `GameManager`: Gestor principal (MVC)
- Maneja eventos, actualiza estado, dibuja

## 🎯 Buenas Prácticas Implementadas

### Código
- ✅ **Separación de responsabilidades**: Cada componente tiene una función clara
- ✅ **Componentes reutilizables**: Button, Panel, ProgressBar, etc.
- ✅ **Configuración centralizada**: Todos los valores en `config.py`
- ✅ **Docstrings completos**: Documentación en todas las clases y métodos
- ✅ **Type hints**: Donde es apropiado
- ✅ **Nombres descriptivos**: Variables y funciones auto-explicativas

### UI/UX
- ✅ **Feedback visual**: Estados hover, active, disabled
- ✅ **Paleta de colores consistente**: Tema espacial coherente
- ✅ **Iconos intuitivos**: Emojis para fácil reconocimiento
- ✅ **Tooltips informativos**: Ayuda contextual
- ✅ **Notificaciones temporales**: Feedback de acciones
- ✅ **Animaciones sutiles**: Mejoran la experiencia sin distraer

### Rendimiento
- ✅ **60 FPS**: Actualización suave
- ✅ **Renderizado eficiente**: Solo dibuja lo necesario
- ✅ **Sistema de eventos**: Manejo óptimo de interacciones

## 🚀 Mejoras Futuras Posibles

### Funcionalidades
- [ ] Sistema de guardado/carga
- [ ] Múltiples niveles/mapas
- [ ] Sistema de logros
- [ ] Modo historia con objetivos
- [ ] Minijuegos en las estrellas
- [ ] Tienda de mejoras para el burro

### Visuales
- [ ] Partículas al viajar
- [ ] Efectos de estrellas (twinkle)
- [ ] Fondo animado (estrellas de fondo)
- [ ] Animación del viaje del burro
- [ ] Zoom y pan en el grafo
- [ ] Temas de color alternativos

### Audio
- [ ] Música de fondo espacial
- [ ] Efectos de sonido para acciones
- [ ] Sonido ambiente

### Técnicas
- [ ] Serialización de estados
- [ ] Sistema de plugins
- [ ] Editor de niveles
- [ ] Multijugador (turn-based)

## 📝 Notas de Desarrollo

### Dependencias
- **Pygame**: ~2.5.0 o superior
- **Python**: 3.10+ (usa match/case)

### Performance
- Optimizado para grafos de hasta ~50 estrellas
- 60 FPS estable en hardware moderno
- Uso de memoria: ~50-100 MB

### Compatibilidad
- Windows ✅
- Linux ✅
- macOS ✅

## 🐛 Troubleshooting

### "Pygame no está instalado"
```bash
pip install pygame
```

### "No se puede importar gui"
Asegúrate de ejecutar desde el directorio raíz:
```bash
python play.py
```

### Las coordenadas están mal
Verifica que `config.json` tenga las coordenadas correctas y ajusta
`GraphScale.SCALE_FACTOR` en `gui/config.py`

### Rendimiento bajo
- Desactiva efectos en `gui/config.py`:
  - `VisualEffects.GLOW_ENABLED = False`
  - `VisualEffects.PARTICLES_ENABLED = False`
  - `VisualEffects.ANIMATIONS_ENABLED = False`

---

**¡Disfruta explorando el universo con tu burro científico! 🐴✨🚀**
