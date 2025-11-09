# 🔗 Diagrama de Integración Frontend-Backend

## 📊 ARQUITECTURA COMPLETA

```
┌─────────────────────────────────────────────────────────────────┐
│                         CAPA DE DATOS                           │
│                         (data/)                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  config.json                                                    │
│  ├─ stars[]           → Estrellas con coordenadas              │
│  ├─ edges[]           → Conexiones entre estrellas             │
│  ├─ healthImpact      → Efectos en salud ✅                     │
│  └─ lifeTimeImpact    → Efectos en tiempo de vida ✅            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                       CAPA DE MODELOS                           │
│                       (models/)                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐   ┌─────────────┐   ┌──────────────────┐     │
│  │   Vertex    │   │   Estrella  │   │     Donkey       │     │
│  ├─────────────┤   ├─────────────┤   ├──────────────────┤     │
│  │ • id        │   │ • label     │   │ • energy ✅      │     │
│  │ • neighbors │   │ • x, y      │   │ • health ✅      │     │
│  │ • weight    │   │ • hipergig. │   │ • age ✅         │     │
│  └─────────────┘   │ • health_   │   │ • grass ✅       │     │
│                    │   impact ✅  │   │ • alive ✅       │     │
│  ┌─────────────┐   │ • life_time │   └──────────────────┘     │
│  │    Graph    │   │   impact ✅  │                            │
│  ├─────────────┤   └─────────────┘                            │
│  │ • vertices  │                                               │
│  │ • add_edge  │   ┌──────────────────────────────┐           │
│  └─────────────┘   │   GrafoConstelaciones        │           │
│        ↑           ├──────────────────────────────┤           │
│        │           │ • estrellas{} ✅             │           │
│        └───────────┤ • graph{} ✅                 │           │
│                    │ • obtener_estrella() ✅      │           │
│                    │ • get_vertex() ✅            │           │
│                    └──────────────────────────────┘           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    CAPA DE ALGORITMOS                           │
│                    (algorithms/)                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  dijkstra.py                                                    │
│  ├─ encontrar_camino_mas_corto() ✅                             │
│  │   ├─ Entrada: grafo, origen, destino                        │
│  │   └─ Salida: {existe, distancia, camino, pasos}             │
│  │                                                              │
│  └─ obtener_estrellas_alcanzables() ✅                          │
│      ├─ Entrada: grafo, origen, energía_disponible             │
│      └─ Salida: [{id, distancia, camino, energía_restante}]    │
│                                                                 │
│  bellman_ford.py (disponible pero no usado en GUI)              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                  CAPA DE COORDINACIÓN                           │
│                  (models/simulator.py)                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  SimuladorViaje                                                 │
│  ├─────────────────────────────────────────────────────────┐   │
│  │ ATRIBUTOS USADOS POR GUI:                               │   │
│  │ • posicion_actual ✅                                     │   │
│  │ • distancia_total ✅                                     │   │
│  │ • historial_viaje[] ✅                                   │   │
│  │ • grafo (referencia) ✅                                  │   │
│  │ • donkey (referencia) ✅                                 │   │
│  ├─────────────────────────────────────────────────────────┤   │
│  │ MÉTODOS USADOS POR GUI:                                 │   │
│  │ • viajar_a(destino_id) → bool ✅                         │   │
│  │   ├─ Llama: encontrar_camino_mas_corto()                │   │
│  │   ├─ Llama: donkey.trip()                               │   │
│  │   └─ Actualiza: posicion, historial, distancia          │   │
│  │                                                          │   │
│  │ • comer_pasto(kg) → bool ✅                              │   │
│  │   └─ Llama: donkey.eat_grass()                          │   │
│  │                                                          │   │
│  │ • investigar_estrella(tiempo) → bool ✅                  │   │
│  │   └─ Llama: donkey.stay_of_star()                       │   │
│  │        └─ Aplica: health_impact, life_time_impact       │   │
│  │                                                          │   │
│  │ • obtener_resumen_viaje() → dict ✅                      │   │
│  │   └─ Retorna: estrellas_visitadas, distancia, edad, etc │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                      CAPA DE INTERFAZ                           │
│                      (gui/)                                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ game.py - GameManager (CONTROLADOR PRINCIPAL)            │  │
│  ├──────────────────────────────────────────────────────────┤  │
│  │ __init__():                                              │  │
│  │   self.grafo = cargar_grafo_desde_json() ✅              │  │
│  │   self.burro = crear_burro_desde_json() ✅               │  │
│  │   self.simulador = SimuladorViaje(...) ✅                │  │
│  │   self.graph_renderer = GraphRenderer(grafo) ✅          │  │
│  │   self.panels = [...] ✅                                 │  │
│  │                                                          │  │
│  │ handle_events(): (INTERACCIÓN)                          │  │
│  │   ├─ Click en estrella:                                 │  │
│  │   │   └─ graph_renderer.get_star_at_position()          │  │
│  │   │   └─ encontrar_camino_mas_corto() ✅                │  │
│  │   │                                                      │  │
│  │   ├─ Click "Viajar":                                    │  │
│  │   │   └─ simulador.viajar_a() ✅                         │  │
│  │   │                                                      │  │
│  │   ├─ Click "Comer":                                     │  │
│  │   │   └─ simulador.comer_pasto() ✅                      │  │
│  │   │                                                      │  │
│  │   └─ Click "Investigar":                                │  │
│  │       └─ simulador.investigar_estrella() ✅             │  │
│  │                                                          │  │
│  │ update(): (LÓGICA)                                      │  │
│  │   └─ graph_renderer.update(posicion_actual) ✅          │  │
│  │                                                          │  │
│  │ draw(): (RENDERIZADO)                                   │  │
│  │   ├─ graph_renderer.draw() ✅                            │  │
│  │   └─ panels.draw() ✅                                    │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ graph_renderer.py (VISTA DEL GRAFO)                      │  │
│  ├──────────────────────────────────────────────────────────┤  │
│  │ __init__(grafo):                                         │  │
│  │   self.grafo = grafo ✅                                  │  │
│  │                                                          │  │
│  │ draw():                                                  │  │
│  │   for star_id, estrella in grafo.estrellas.items(): ✅  │  │
│  │       render_star(estrella.x, estrella.y, ...)          │  │
│  │                                                          │  │
│  │   for vertex in grafo.graph.values(): ✅                │  │
│  │       render_edges(vertex.neighbors)                    │  │
│  │                                                          │  │
│  │ get_reachable_stars():                                  │  │
│  │   return obtener_estrellas_alcanzables(...) ✅          │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ panels.py (VISTAS DE INFORMACIÓN)                        │  │
│  ├──────────────────────────────────────────────────────────┤  │
│  │                                                          │  │
│  │ DonkeyInfoPanel:                                         │  │
│  │   update(donkey, star_name, distance):                  │  │
│  │     energy_bar.update(donkey.donkey_energy) ✅          │  │
│  │     grass_bar.update(donkey.grass_in_basement) ✅       │  │
│  │     health_label.update(donkey.health) ✅               │  │
│  │     age_label.update(donkey.age, donkey.max_age) ✅     │  │
│  │                                                          │  │
│  │ StarInfoPanel:                                           │  │
│  │   set_star(estrella):                                   │  │
│  │     show(estrella.label) ✅                              │  │
│  │     show(estrella.hipergigante) ✅                       │  │
│  │     show(estrella.health_impact) ✅                      │  │
│  │     show(estrella.life_time_impact) ✅                   │  │
│  │                                                          │  │
│  │ ActionsPanel:                                            │  │
│  │   [Botones que llaman callbacks del GameManager]        │  │
│  │                                                          │  │
│  │ ReachableStarsPanel:                                     │  │
│  │   set_reachable(reachable_list):                        │  │
│  │     [Muestra estrellas alcanzables]                     │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ components.py (COMPONENTES REUTILIZABLES)                │  │
│  ├──────────────────────────────────────────────────────────┤  │
│  │ • Button, Panel, ProgressBar                             │  │
│  │ • Tooltip, Notification, InfoLabel                       │  │
│  │ [No dependen del backend, solo de Pygame]                │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ config.py (CONFIGURACIÓN)                                │  │
│  ├──────────────────────────────────────────────────────────┤  │
│  │ • Colors, Fonts, Sizes                                   │  │
│  │ • Animation settings                                     │  │
│  │ [No depende del backend]                                 │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                     PUNTO DE ENTRADA                            │
│                     (play.py)                                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  main():                                                        │
│    ├─ Verificar Pygame instalado                               │
│    ├─ Mostrar controles                                        │
│    └─ game = GameManager()                                     │
│        └─ game.run()                                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔄 FLUJO DE DATOS DETALLADO

### **1. INICIALIZACIÓN**

```
play.py
  ↓
GameManager.__init__()
  ├─→ main.cargar_grafo_desde_json()
  │     ├─ Lee data/config.json
  │     ├─ Crea GrafoConstelaciones
  │     │   ├─ Para cada estrella:
  │     │   │   agregar_estrella(
  │     │   │     id, label, x, y,
  │     │   │     health_impact ✅,
  │     │   │     life_time_impact ✅
  │     │   │   )
  │     │   └─ Para cada edge:
  │     │       add_edge(from, to, weight)
  │     └─ return grafo
  │
  ├─→ main.crear_burro_desde_json()
  │     ├─ Lee data/config.json
  │     ├─ Crea Donkey(
  │     │     energy, grass, age, max_age
  │     │   )
  │     └─ return burro
  │
  ├─→ SimuladorViaje(grafo, burro, posicion_inicial)
  │     └─ Conecta grafo + burro
  │
  ├─→ GraphRenderer(grafo)
  │     └─ Prepara renderizado del grafo
  │
  └─→ Panels(...)
        └─ Crea UI components
```

---

### **2. ACCIÓN: VIAJAR A ESTRELLA**

```
Usuario hace click en estrella
  ↓
GameManager.handle_events()
  ├─ mouse_pos = pygame.mouse.get_pos()
  │
  ├─ star_id = graph_renderer.get_star_at_position(mouse_pos)
  │   └─ return star_id si está cerca del mouse
  │
  ├─ selected_star_id = star_id
  │
  ├─ resultado = encontrar_camino_mas_corto(
  │     grafo, ✅
  │     simulador.posicion_actual, ✅
  │     selected_star_id
  │   )
  │   └─ return {existe, distancia, camino, pasos}
  │
  ├─ star_info_panel.set_star(
  │     estrella, ✅
  │     distance=resultado['distancia'],
  │     path=resultado['camino']
  │   )
  │
  └─ graph_renderer.set_active_path(resultado['camino'])

Usuario hace click en botón "Viajar"
  ↓
GameManager._on_travel_click()
  ├─ if energia_suficiente:
  │   │
  │   ├─ exito = simulador.viajar_a(selected_star_id) ✅
  │   │   │
  │   │   └─ SimuladorViaje.viajar_a():
  │   │       ├─ encontrar_camino_mas_corto() ✅
  │   │       ├─ Para cada paso:
  │   │       │   ├─ donkey.trip(
  │   │       │   │     distance,
  │   │       │   │     health_impact, ✅
  │   │       │   │     life_time_impact ✅
  │   │       │   │   )
  │   │       │   └─ posicion_actual = nuevo_id ✅
  │   │       └─ return True/False
  │   │
  │   └─ if exito:
  │       ├─ notification.add("Viaje exitoso")
  │       └─ _update_ui()
  │           ├─ donkey_panel.update(burro) ✅
  │           └─ reachable_panel.update(...) ✅
  │
  └─ else:
      └─ notification.add("Energía insuficiente")
```

---

### **3. ACCIÓN: COMER PASTO**

```
Usuario hace click en "Comer Pasto"
  ↓
GameManager._on_eat_click()
  ├─ if burro.grass_in_basement > 0: ✅
  │   │
  │   ├─ exito = simulador.comer_pasto(5) ✅
  │   │   │
  │   │   └─ SimuladorViaje.comer_pasto():
  │   │       ├─ profit = donkey.calculate_grass_profit() ✅
  │   │       ├─ for _ in range(5):
  │   │       │   └─ donkey.eat_grass(profit) ✅
  │   │       │       ├─ energy += 1 * profit ✅
  │   │       │       ├─ grass_in_basement -= 1 ✅
  │   │       │       └─ health = calculate_health() ✅
  │   │       └─ return True/False
  │   │
  │   └─ if exito:
  │       ├─ notification.add("Burro comió pasto")
  │       └─ _update_ui()
  │           └─ donkey_panel.update(burro) ✅
  │               ├─ energy_bar.update(energy) ✅
  │               ├─ grass_bar.update(grass) ✅
  │               └─ health_label.update(health) ✅
  │
  └─ else:
      └─ notification.add("No hay pasto")
```

---

### **4. ACCIÓN: INVESTIGAR ESTRELLA**

```
Usuario hace click en "Investigar"
  ↓
GameManager._on_investigate_click()
  ├─ exito = simulador.investigar_estrella(tiempo=5.0) ✅
  │   │
  │   └─ SimuladorViaje.investigar_estrella():
  │       ├─ estrella = obtener_estrella_actual() ✅
  │       │
  │       ├─ donkey.stay_of_star(
  │       │     time_to_eat=estrella.time_to_eat, ✅
  │       │     time_of_stance=5.0,
  │       │     health_impact=estrella.health_impact, ✅
  │       │     life_time_impact=estrella.life_time_impact ✅
  │       │   )
  │       │   │
  │       │   └─ Donkey.stay_of_star():
  │       │       ├─ if energy < 50:
  │       │       │   └─ eat_grass() ✅
  │       │       │
  │       │       ├─ energy += health_impact ✅
  │       │       │   └─ Si >0: gana energía
  │       │       │   └─ Si <0: pierde energía
  │       │       │
  │       │       ├─ age -= life_time_impact ✅
  │       │       │   └─ Si >0: gana años de vida
  │       │       │   └─ Si <0: pierde años de vida
  │       │       │
  │       │       ├─ if age >= max_age or energy <= 0:
  │       │       │   └─ dead() ✅
  │       │       │
  │       │       └─ health = calculate_health() ✅
  │       │
  │       └─ return True/False
  │
  ├─ if exito:
  │   ├─ notification.add("Investigación completada")
  │   └─ _update_ui()
  │
  └─ if not burro.alive: ✅
      └─ state = GAME_OVER
```

---

### **5. RENDERIZADO (60 FPS)**

```
GameManager.run()
  └─ while running:
      ├─ handle_events()
      ├─ update()
      └─ draw()
          │
          ├─ graph_renderer.draw(screen)
          │   │
          │   ├─ Para cada estrella en grafo.estrellas: ✅
          │   │   ├─ star = grafo.estrellas[id] ✅
          │   │   ├─ draw_circle(star.x, star.y) ✅
          │   │   ├─ if star.hipergigante: ✅
          │   │   │   └─ draw_glow()
          │   │   └─ if star.id == current_star:
          │   │       └─ draw_pulse_animation()
          │   │
          │   └─ Para cada vertex en grafo.graph: ✅
          │       └─ Para cada neighbor:
          │           └─ draw_line(star1, star2)
          │
          ├─ donkey_panel.draw(screen)
          │   ├─ energy_bar: burro.donkey_energy ✅
          │   ├─ grass_bar: burro.grass_in_basement ✅
          │   ├─ health_label: burro.health ✅
          │   ├─ age_label: burro.age / burro.max_age ✅
          │   ├─ position: current_star.label ✅
          │   └─ distance: simulador.distancia_total ✅
          │
          ├─ star_info_panel.draw(screen)
          │   ├─ estrella.label ✅
          │   ├─ estrella.hipergigante ✅
          │   ├─ estrella.constelaciones ✅
          │   ├─ estrella.health_impact ✅
          │   └─ estrella.life_time_impact ✅
          │
          ├─ actions_panel.draw(screen)
          │   └─ [Botones]
          │
          ├─ reachable_panel.draw(screen)
          │   └─ Para cada alcanzable:
          │       └─ show(label, distance)
          │
          └─ if state == GAME_OVER:
              └─ draw_game_over()
                  └─ resumen = simulador.obtener_resumen_viaje() ✅
                      ├─ estrellas_visitadas ✅
                      ├─ distancia_total ✅
                      ├─ edad ✅
                      └─ vivo ✅
```

---

## ✅ VERIFICACIÓN DE DEPENDENCIAS

### **Frontend usa del Backend:**

| Componente GUI | Usa Backend | Método/Atributo | Estado |
|----------------|-------------|-----------------|--------|
| GameManager | GrafoConstelaciones | `estrellas`, `graph` | ✅ |
| GameManager | SimuladorViaje | `viajar_a()`, `comer_pasto()` | ✅ |
| GameManager | Algoritmos | `encontrar_camino_mas_corto()` | ✅ |
| GraphRenderer | GrafoConstelaciones | `estrellas.items()`, `graph` | ✅ |
| GraphRenderer | Estrella | `x`, `y`, `hipergigante` | ✅ |
| DonkeyInfoPanel | Donkey | `energy`, `health`, `age`, `grass` | ✅ |
| StarInfoPanel | Estrella | `label`, `impacts`, `constelaciones` | ✅ |
| ActionsPanel | SimuladorViaje | Callbacks a métodos | ✅ |
| ReachablePanel | Algoritmos | `obtener_estrellas_alcanzables()` | ✅ |

### **Backend NO depende del Frontend:**
- ✅ Modelos son independientes
- ✅ Algoritmos son independientes
- ✅ SimuladorViaje funciona en terminal y GUI
- ✅ Configuración JSON es neutral

---

## 🎯 CONCLUSIÓN

**Integración: 100% COMPLETA ✅**

- Todos los métodos requeridos existen
- Todos los atributos están disponibles
- Backend es completamente reutilizable
- Frontend aprovecha todo lo necesario del backend
- No hay dependencias circulares
- Separación de responsabilidades clara

**El proyecto está listo para usar sin modificaciones.**
