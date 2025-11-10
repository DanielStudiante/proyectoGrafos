"""
Constantes y configuración para la interfaz gráfica.
Centraliza todos los valores de configuración para fácil mantenimiento.
"""

# Ventana - MÍNIMO 200um x 200um según requerimiento
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 900
FPS = 60
TITLE = "🐴 Burro Científico - Explorador de Constelaciones"

# Dimensiones del tablero (unidades de medida)
BOARD_WIDTH_UM = 200  # Unidades de medida mínimas
BOARD_HEIGHT_UM = 200  # Unidades de medida mínimas

# Colores (paleta profesional)
class Colors:
    # Fondo y UI
    BACKGROUND = (15, 15, 25)           # Azul muy oscuro
    SPACE_DARK = (10, 10, 20)           # Negro espacial
    PANEL_BG = (25, 25, 40)             # Azul oscuro panel
    PANEL_BORDER = (60, 60, 100)        # Borde panel
    
    # Estrellas
    STAR_NORMAL = (255, 255, 200)       # Blanco amarillento
    STAR_HYPERGIANT = (255, 200, 50)    # Naranja dorado
    STAR_VISITED = (150, 150, 150)      # Gris (visitada)
    STAR_CURRENT = (100, 200, 255)      # Azul brillante
    STAR_HOVER = (255, 100, 100)        # Rojo al hover
    STAR_GLOW = (255, 255, 150)         # Brillo
    STAR_MULTI_CONSTELLATION = (255, 50, 50)  # ROJO para múltiples constelaciones
    
    # Colores por constelación (paleta distintiva)
    # Cada constelación tiene su propio color según requerimiento
    CONSTELLATION_COLORS = {
        0: (100, 150, 255),   # Azul
        1: (255, 100, 150),   # Rosa
        2: (150, 255, 100),   # Verde
        3: (255, 200, 100),   # Naranja
        4: (200, 100, 255),   # Morado
        5: (100, 255, 255),   # Cyan
        6: (255, 255, 100),   # Amarillo
        7: (255, 150, 100),   # Coral
        8: (150, 100, 255),   # Violeta
        9: (100, 255, 150),   # Verde agua
    }
    
    # Conexiones
    CONNECTION = (50, 50, 80)           # Líneas entre estrellas
    CONNECTION_ACTIVE = (100, 150, 255) # Línea del camino
    PATH_OPTIMAL = (0, 255, 255)        # Cyan brillante para ruta óptima sin pasto (REQ 1.2)
    PATH_OPTIMAL_GRASS = (0, 255, 100)  # Verde brillante para ruta óptima con pasto (REQ 2.0)
    
    # Texto
    TEXT_PRIMARY = (255, 255, 255)      # Blanco
    TEXT_SECONDARY = (180, 180, 200)    # Gris claro
    TEXT_TITLE = (255, 215, 0)          # Dorado
    TEXT_DANGER = (255, 100, 100)       # Rojo
    TEXT_SUCCESS = (100, 255, 100)      # Verde
    TEXT_INFO = (100, 200, 255)         # Azul info
    TEXT_HIGHLIGHT = (255, 255, 0)      # Amarillo resaltado
    
    # UI Elements
    BUTTON_BG = (40, 40, 70)            # Fondo botón
    BUTTON_HOVER = (60, 60, 100)        # Hover botón
    BUTTON_ACTIVE = (80, 80, 120)       # Botón presionado
    BUTTON_DISABLED = (30, 30, 40)      # Botón deshabilitado
    
    # Efectos
    HEALTH_POSITIVE = (100, 255, 150)   # Verde salud positiva
    HEALTH_NEGATIVE = (255, 100, 100)   # Rojo salud negativa
    LIFE_POSITIVE = (150, 200, 255)     # Azul vida positiva
    LIFE_NEGATIVE = (255, 150, 100)     # Naranja vida negativa
    
    # Barras de progreso
    ENERGY_HIGH = (100, 255, 100)       # Verde energía alta
    ENERGY_MID = (255, 200, 100)        # Amarillo energía media
    ENERGY_LOW = (255, 100, 100)        # Rojo energía baja
    
    GRASS_COLOR = (150, 255, 150)       # Verde pasto
    AGE_COLOR = (200, 150, 255)         # Morado edad

# Fuentes
class Fonts:
    TITLE_SIZE = 36
    SUBTITLE_SIZE = 24
    NORMAL_SIZE = 18
    SMALL_SIZE = 14
    TINY_SIZE = 12

# Espaciado
class Spacing:
    PADDING = 20
    MARGIN = 10
    BUTTON_SPACING = 15
    PANEL_PADDING = 15

# Dimensiones de paneles
class PanelSizes:
    # Panel izquierdo (información del burro)
    LEFT_PANEL_WIDTH = 350
    LEFT_PANEL_X = 0
    LEFT_PANEL_Y = 0
    
    # Panel derecho (opciones y acciones)
    RIGHT_PANEL_WIDTH = 350
    RIGHT_PANEL_X = WINDOW_WIDTH - RIGHT_PANEL_WIDTH
    RIGHT_PANEL_Y = 0
    
    # Área del grafo (centro)
    GRAPH_X = LEFT_PANEL_WIDTH
    GRAPH_Y = 0
    GRAPH_WIDTH = WINDOW_WIDTH - LEFT_PANEL_WIDTH - RIGHT_PANEL_WIDTH
    GRAPH_HEIGHT = WINDOW_HEIGHT
    
    # Panel inferior (información de estrellas)
    BOTTOM_PANEL_HEIGHT = 180
    BOTTOM_PANEL_Y = WINDOW_HEIGHT - BOTTOM_PANEL_HEIGHT

# Botones
class ButtonSizes:
    WIDTH = 280
    HEIGHT = 50
    SMALL_WIDTH = 130
    SMALL_HEIGHT = 40

# Animaciones
class Animation:
    STAR_PULSE_SPEED = 0.05             # Velocidad del pulso
    STAR_PULSE_MIN = 0.8                # Escala mínima
    STAR_PULSE_MAX = 1.2                # Escala máxima
    
    TRAVEL_SPEED = 200                  # Píxeles por segundo
    
    FADE_SPEED = 5                      # Velocidad de fade in/out
    
    PARTICLE_LIFETIME = 60              # Frames de vida de partículas
    PARTICLE_COUNT = 10                 # Partículas por efecto

# Escala del grafo
class GraphScale:
    # Factor de escala para convertir coordenadas del JSON a píxeles
    SCALE_FACTOR = 3.0
    OFFSET_X = 50                       # Offset horizontal
    OFFSET_Y = 50                       # Offset vertical
    
    MIN_STAR_RADIUS = 8                 # Radio mínimo de estrella
    MAX_STAR_RADIUS = 25                # Radio máximo de estrella
    
    CONNECTION_WIDTH = 2                # Grosor de conexiones
    ACTIVE_CONNECTION_WIDTH = 4         # Grosor de camino activo

# Iconos y símbolos (usando emojis/caracteres)
class Icons:
    ENERGY = "⚡"
    HEALTH = "💚"
    AGE = "🎂"
    GRASS = "🌾"
    STAR = "⭐"
    DISTANCE = "📏"
    DANGER = "⚠️"
    SUCCESS = "✅"
    INVESTIGATION = "🔬"
    TRAVEL = "🚀"
    EAT = "🍽️"
    DONKEY = "🐴"

# Estados del juego
class GameState:
    MENU = "menu"
    PLAYING = "playing"
    TRAVELING = "traveling"
    INVESTIGATING = "investigating"
    GAME_OVER = "game_over"
    VICTORY = "victory"
    PAUSED = "paused"
    CONFIG = "config"

# Configuración de efectos visuales
class VisualEffects:
    GLOW_ENABLED = True
    PARTICLES_ENABLED = True
    ANIMATIONS_ENABLED = True
    SMOOTH_MOVEMENT = True
    
    GLOW_RADIUS = 30
    GLOW_ALPHA = 100

# Sonidos (placeholders para futuro)
class Sounds:
    CLICK = "click"
    TRAVEL = "travel"
    EAT = "eat"
    DAMAGE = "damage"
    HEAL = "heal"
    DEATH = "death"
    VICTORY = "victory"
