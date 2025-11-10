"""
Gestor principal del juego.
Responsabilidad: Coordinar el ciclo de vida del juego y gestionar componentes.
"""

import pygame
import sys
from gui.config import (WINDOW_WIDTH, WINDOW_HEIGHT, FPS, TITLE, Colors,
                        GameState, PanelSizes)
from gui.graph_renderer import GraphRenderer
from gui.panels import DonkeyInfoPanel, StarInfoPanel, ActionsPanel, ReachableStarsPanel
from gui.star_editor import StarEditorPanel
from gui.components import Tooltip, Notification
from gui.game_events import GameEventHandler
from gui.game_renderer import GameRenderer
from models.simulator import SimuladorViaje
from algorithms.dijkstra import encontrar_camino_mas_corto
from utils.config_loader import cargar_grafo_desde_json, crear_burro_desde_json


class GameManager:
    """
    Gestor principal del juego.
    
    Responsabilidades (SRP):
    - Inicializar componentes del juego
    - Coordinar el game loop
    - Gestionar estado del juego
    - Actualizar y renderizar componentes
    """
    
    def __init__(self):
        # Inicializar Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        
        # Estado del juego
        self.state = GameState.PLAYING
        self.running = True
        
        # Cargar datos
        self.grafo = cargar_grafo_desde_json()
        self.burro = crear_burro_desde_json()
        self.simulador = SimuladorViaje(self.grafo, self.burro, posicion_inicial=1)
        
        # Renderizador del grafo
        self.graph_renderer = GraphRenderer(
            self.grafo,
            offset_x=PanelSizes.LEFT_PANEL_WIDTH,
            offset_y=0
        )
        
        # Event handler
        self.event_handler = GameEventHandler(self)
        
        # Renderer
        self.renderer = GameRenderer(self.screen, self)
        
        # Paneles UI
        self._create_panels()
        
        # UI Components
        self.tooltip = Tooltip()
        self.notification = Notification(
            PanelSizes.LEFT_PANEL_WIDTH,
            10,
            PanelSizes.GRAPH_WIDTH
        )
        
        # Fuentes
        self.title_font = pygame.font.Font(None, 36)
        self.normal_font = pygame.font.Font(None, 20)
        
        # Estado de interacción
        self.selected_star_id = None
        self.hovered_star_id = None
        
        # Actualizar información inicial
        self._update_ui()
    
    def _create_panels(self):
        """Crea todos los paneles de la interfaz."""
        # Panel izquierdo - Info del burro
        self.donkey_panel = DonkeyInfoPanel(
            PanelSizes.LEFT_PANEL_X,
            PanelSizes.LEFT_PANEL_Y,
            PanelSizes.LEFT_PANEL_WIDTH,
            300
        )
        
        # Panel derecho - Acciones
        self.actions_panel = ActionsPanel(
            PanelSizes.RIGHT_PANEL_X,
            PanelSizes.RIGHT_PANEL_Y,
            PanelSizes.RIGHT_PANEL_WIDTH,
            400,
            on_travel=self.event_handler._on_travel_click,
            on_eat=self.event_handler._on_eat_click,
            on_investigate=self.event_handler._on_investigate_click,
            on_config=self.event_handler._on_config_click
        )
        
        # Panel de estrellas alcanzables
        self.reachable_panel = ReachableStarsPanel(
            PanelSizes.LEFT_PANEL_X,
            320,
            PanelSizes.LEFT_PANEL_WIDTH,
            250
        )
        
        # Panel de información de estrella
        self.star_info_panel = StarInfoPanel(
            PanelSizes.RIGHT_PANEL_X,
            420,
            PanelSizes.RIGHT_PANEL_WIDTH,
            400
        )
        
        # Panel de editor de estrellas
        editor_width = 350
        editor_height = 280
        self.star_editor = StarEditorPanel(
            (WINDOW_WIDTH - editor_width) // 2,
            (WINDOW_HEIGHT - editor_height) // 2,
            editor_width,
            editor_height
        )
        self.star_editor.set_grafo(self.grafo)
    
    def _update_ui(self):
        """Actualiza todos los elementos de la UI."""
        # Actualizar panel del burro
        current_star = self.grafo.obtener_estrella(self.simulador.posicion_actual)
        self.donkey_panel.update(
            self.burro,
            current_star.label if current_star else "Desconocida",
            self.simulador.distancia_total
        )
        
        # Actualizar estrellas alcanzables
        reachable = self.graph_renderer.get_reachable_stars(
            self.simulador.posicion_actual,
            self.burro.donkey_energy
        )
        
        # Añadir labels a las estrellas alcanzables
        for r in reachable:
            star = self.grafo.obtener_estrella(r['id'])
            if star:
                r['label'] = star.label
        
        self.reachable_panel.set_reachable(reachable)
    
    def _update_star_selection(self):
        """Actualiza la información de la estrella seleccionada."""
        if not self.selected_star_id:
            self.star_info_panel.clear()
            self.graph_renderer.set_active_path([])
            return
        
        estrella = self.grafo.obtener_estrella(self.selected_star_id)
        if not estrella:
            return
        
        # Calcular ruta
        resultado = encontrar_camino_mas_corto(
            self.grafo,
            self.simulador.posicion_actual,
            self.selected_star_id
        )
        
        if resultado and resultado['existe']:
            self.star_info_panel.set_star(
                estrella,
                distance=resultado['distancia'],
                energy_needed=resultado['distancia'],
                path=resultado['camino']
            )
            self.graph_renderer.set_active_path(resultado['camino'])
        else:
            self.star_info_panel.set_star(estrella)
            self.graph_renderer.set_active_path([])
    
    def update(self):
        """Actualiza el estado del juego."""
        mouse_pos = pygame.mouse.get_pos()
        
        # Actualizar renderizador del grafo
        self.graph_renderer.update(mouse_pos, self.simulador.posicion_actual)
        
        # Actualizar notificaciones
        self.notification.update()
        
        # Detectar estrella bajo el cursor para tooltip
        self._update_hover_tooltip(mouse_pos)
    
    def _update_hover_tooltip(self, mouse_pos):
        """Actualiza el tooltip de la estrella bajo el cursor."""
        hovered_star_id = self.graph_renderer.get_star_at_position(mouse_pos)
        
        if hovered_star_id != self.hovered_star_id:
            self.hovered_star_id = hovered_star_id
            
            if hovered_star_id:
                star = self.grafo.obtener_estrella(hovered_star_id)
                if star:
                    tooltip_text = f"{star.label}\n"
                    if star.hipergigante:
                        tooltip_text += "⭐ Hipergigante\n"
                    tooltip_text += f"Click para seleccionar"
                    self.tooltip.show(tooltip_text, mouse_pos)
            else:
                self.tooltip.hide()
    
    def run(self):
        """Loop principal del juego."""
        while self.running:
            self.event_handler.handle_events()
            
            if self.state == GameState.PLAYING:
                self.update()
            
            self.renderer.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()
