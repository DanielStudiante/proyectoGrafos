# 🐴 Simulador del Burro Científico Espacial

Proyecto de Estructuras de Datos - Navegación por Constelaciones usando Algoritmos de Grafos

---

## 📁 Estructura del Proyecto

```
Proyecto-Arboles/
│
├── main.py                  # 🎯 Punto de entrada principal
│
├── backend/                 # 🔧 BACKEND - Lógica de negocio
│   ├── constellation.py     # Grafo de constelaciones
│   ├── donkey.py            # Modelo del burro
│   ├── star.py              # Modelo de estrella
│   ├── graph.py             # Estructura de grafo base
│   ├── vertex.py            # Vértices del grafo
│   ├── simulator.py         # Simulador de viaje
│   ├── travel_manager.py    # Gestor de viajes
│   ├── health_calculator.py # Cálculo de salud
│   └── damage_calculator.py # Cálculo de daño
│
├── views/                   # 🎨 FRONTEND - Interfaz gráfica
│   ├── game.py              # Vista principal del juego
│   ├── game_manager.py      # Gestor del juego
│   ├── game_renderer.py     # Renderizado principal
│   ├── game_events.py       # Manejo de eventos
│   ├── event_handler.py     # Handler de eventos
│   ├── graph_renderer.py    # Renderizado del grafo
│   ├── star_visual.py       # Visual de estrellas
│   ├── star_editor.py       # Editor de estrellas
│   ├── connection_visual.py # Visual de conexiones
│   ├── panels.py            # Paneles UI
│   ├── info_panels.py       # Paneles de información
│   ├── action_panels.py     # Paneles de acciones
│   ├── components.py        # Componentes reutilizables
│   └── config.py            # Configuración visual
│
├── algorithms/              # 🧮 Algoritmos de grafos
│   ├── dijkstra.py          # Camino más corto (Dijkstra)
│   ├── bellman_ford.py      # Camino más corto (Bellman-Ford)
│   └── algorithms.py        # Otros algoritmos
│
├── controllers/             # 🎮 Controladores (MVC)
│
├── utils/                   # 🛠️ Utilidades
│   ├── config_loader.py     # Carga de configuración
│   └── config_saver.py      # Guardado de configuración
│
├── data/                    # 📊 Datos
│   └── config.json          # Configuración del grafo
│
└── images/                  # 🖼️ Recursos visuales
```

---

## 🎯 Separación Frontend/Backend

### Backend (`backend/`)
- **Responsabilidad**: Lógica de negocio, modelos de datos, cálculos
- **Sin dependencias de**: Pygame, GUI, visualización
- **Testeable**: Independiente de la interfaz

### Frontend (`views/`)
- **Responsabilidad**: Interfaz gráfica, renderizado, interacción usuario
- **Depende de**: Pygame, backend
- **Presenta**: Los datos del backend de forma visual

---

## 🚀 Ejecutar el Proyecto

```bash
# Modo gráfico (GUI)
python -m views.game

# O desde main.py
python main.py
```

---

## 🔧 Tecnologías

- **Python 3.8+**
- **Pygame** - Interfaz gráfica
- **Algoritmos**: Dijkstra, Bellman-Ford

---

## 📝 Flujo de Datos

```
Usuario (views/) 
    ↓
Controladores (controllers/)
    ↓
Backend (backend/)
    ↓
Algoritmos (algorithms/)
    ↓
Datos (data/)
```

---

## 👥 Equipo

Proyecto Estructura de Datos 2025-2

---

## 📄 Licencia

Proyecto académico - Universidad
