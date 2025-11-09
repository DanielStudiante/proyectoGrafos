"""
Gestor principal del juego con interfaz gráfica.
Implementa el patrón MVC y gestión de estados.
"""

import pygame
import sys
from gui.config import (WINDOW_WIDTH, WINDOW_HEIGHT, FPS, TITLE, Colors,
                        GameState, PanelSizes, Icons)
from gui.graph_renderer import GraphRenderer
from gui.panels import DonkeyInfoPanel, StarInfoPanel, ActionsPanel, ReachableStarsPanel
from gui.components import Tooltip, Notification
from models.simulator import SimuladorViaje
from algorithms.dijkstra import encontrar_camino_mas_corto
from utils.config_loader import cargar_grafo_desde_json, crear_burro_desde_json


class GameManager:
    """Gestor principal del juego."""
    
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
        self.mouse_pressed_last_frame = False
        
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
            on_travel=self._on_travel_click,
            on_eat=self._on_eat_click,
            on_investigate=self._on_investigate_click,
            on_config=self._on_config_click
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
    
    def _on_travel_click(self):
        """Callback cuando se hace click en viajar."""
        if self.selected_star_id and self.selected_star_id != self.simulador.posicion_actual:
            # Verificar si es alcanzable
            resultado = encontrar_camino_mas_corto(
                self.grafo,
                self.simulador.posicion_actual,
                self.selected_star_id
            )
            
            # DEBUG: Imprimir valores
            print(f"\n🔍 DEBUG VIAJE:")
            print(f"   Desde: {self.simulador.posicion_actual}")
            print(f"   Hacia: {self.selected_star_id}")
            print(f"   Energía del burro: {self.burro.donkey_energy}")
            if resultado and resultado['existe']:
                print(f"   Distancia necesaria: {resultado['distancia']}")
                print(f"   Puede viajar: {resultado['distancia'] <= self.burro.donkey_energy}")
            else:
                print(f"   No hay ruta disponible")
            
            if resultado and resultado['existe']:
                if resultado['distancia'] <= self.burro.donkey_energy:
                    # Realizar viaje
                    exito = self.simulador.viajar_a(self.selected_star_id, verbose=False)
                    
                    if exito:
                        star = self.grafo.obtener_estrella(self.selected_star_id)
                        self.notification.add(
                            f"{Icons.SUCCESS} Viaje exitoso a {star.label}",
                            Colors.TEXT_SUCCESS
                        )
                        self._update_ui()
                        
                        # Verificar si el burro sigue vivo
                        if not self.burro.alive:
                            self.state = GameState.GAME_OVER
                            self.notification.add(
                                f"💀 El burro ha muerto...",
                                Colors.TEXT_DANGER,
                                duration=300
                            )
                    else:
                        self.notification.add(
                            f"{Icons.DANGER} No se pudo completar el viaje",
                            Colors.TEXT_DANGER
                        )
                else:
                    self.notification.add(
                        f"{Icons.DANGER} Energía insuficiente: {self.burro.donkey_energy:.1f}/{resultado['distancia']:.1f}",
                        Colors.TEXT_DANGER
                    )
                    print(f"   ❌ No puedes viajar - Energía insuficiente")
            else:
                self.notification.add(
                    f"{Icons.DANGER} No hay ruta disponible",
                    Colors.TEXT_DANGER
                )
    
    def _on_eat_click(self):
        """Callback cuando se hace click en comer."""
        if self.burro.grass_in_basement > 0:
            exito = self.simulador.comer_pasto(5)
            if exito:
                self.notification.add(
                    f"{Icons.EAT} El burro comió pasto",
                    Colors.TEXT_SUCCESS
                )
                self._update_ui()
            else:
                self.notification.add(
                    f"{Icons.DANGER} No se pudo comer",
                    Colors.TEXT_DANGER
                )
        else:
            self.notification.add(
                f"{Icons.DANGER} No hay pasto disponible",
                Colors.TEXT_DANGER
            )
    
    def _on_investigate_click(self):
        """Callback cuando se hace click en investigar."""
        exito = self.simulador.investigar_estrella(tiempo_investigacion=5.0)
        if exito:
            self.notification.add(
                f"{Icons.INVESTIGATION} Investigación completada",
                Colors.TEXT_SUCCESS
            )
            self._update_ui()
            
            # Verificar si sigue vivo
            if not self.burro.alive:
                self.state = GameState.GAME_OVER
        else:
            self.notification.add(
                f"{Icons.DANGER} No se pudo investigar",
                Colors.TEXT_DANGER
            )
    
    def _on_config_click(self):
        """Callback para abrir configuración."""
        self.notification.add(
            "⚙️ Configuración (próximamente)",
            Colors.TEXT_SECONDARY
        )
    
    def handle_events(self):
        """Maneja todos los eventos de Pygame."""
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    self._on_eat_click()
                elif event.key == pygame.K_i:
                    self._on_investigate_click()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Click izquierdo
                    # Verificar si se hizo click en una estrella
                    star_id = self.graph_renderer.get_star_at_position(mouse_pos)
                    if star_id:
                        self.selected_star_id = star_id
                        self._update_star_selection()
        
        # Actualizar paneles con estado del mouse
        self.actions_panel.update(
            mouse_pos,
            mouse_pressed and not self.mouse_pressed_last_frame,
            can_travel=(self.selected_star_id is not None and 
                       self.selected_star_id != self.simulador.posicion_actual),
            has_grass=(self.burro.grass_in_basement > 0)
        )
        
        self.mouse_pressed_last_frame = mouse_pressed
    
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
    
    def draw(self):
        """Dibuja todos los elementos del juego."""
        # Fondo
        self.screen.fill(Colors.BACKGROUND)
        
        # Área del grafo con fondo especial
        graph_area = pygame.Rect(
            PanelSizes.LEFT_PANEL_WIDTH, 0,
            PanelSizes.GRAPH_WIDTH, PanelSizes.GRAPH_HEIGHT
        )
        pygame.draw.rect(self.screen, Colors.SPACE_DARK, graph_area)
        
        # Dibujar grafo
        visited_stars = set(self.simulador.historial_viaje)
        self.graph_renderer.draw(
            self.screen,
            current_star_id=self.simulador.posicion_actual,
            visited_stars=visited_stars
        )
        
        # Dibujar paneles
        self.donkey_panel.draw(self.screen)
        self.reachable_panel.draw(self.screen)
        self.actions_panel.draw(self.screen)
        self.star_info_panel.draw(self.screen)
        
        # Dibujar notificaciones
        self.notification.draw(self.screen, self.normal_font)
        
        # Dibujar tooltip
        self.tooltip.draw(self.screen, pygame.font.Font(None, 16))
        
        # Dibujar Game Over si aplica
        if self.state == GameState.GAME_OVER:
            self._draw_game_over()
        
        # Actualizar pantalla
        pygame.display.flip()
    
    def _draw_game_over(self):
        """Dibuja la pantalla de Game Over."""
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        # Título
        title = self.title_font.render("💀 GAME OVER 💀", True, Colors.TEXT_DANGER)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
        self.screen.blit(title, title_rect)
        
        # Resumen
        resumen = self.simulador.obtener_resumen_viaje()
        stats = [
            f"Estrellas visitadas: {resumen['estrellas_visitadas']}",
            f"Distancia recorrida: {resumen['distancia_total']:.1f} ly",
            f"Edad final: {resumen['edad']:.1f} años luz",
        ]
        
        y = WINDOW_HEIGHT // 2
        for stat in stats:
            stat_surface = self.normal_font.render(stat, True, Colors.TEXT_PRIMARY)
            stat_rect = stat_surface.get_rect(center=(WINDOW_WIDTH // 2, y))
            self.screen.blit(stat_surface, stat_rect)
            y += 30
        
        # Instrucciones
        restart = self.normal_font.render("Presiona ESC para salir", True, Colors.TEXT_SECONDARY)
        restart_rect = restart.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 100))
        self.screen.blit(restart, restart_rect)
    
    def run(self):
        """Loop principal del juego."""
        while self.running:
            self.handle_events()
            
            if self.state == GameState.PLAYING:
                self.update()
            
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()


def main():
    """Punto de entrada de la aplicación gráfica."""
    game = GameManager()
    game.run()


if __name__ == "__main__":
    main()
