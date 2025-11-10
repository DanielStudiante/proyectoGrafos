"""
Renderizado del estado del juego.
Responsabilidad: Dibujar todos los elementos visuales del juego en pantalla.
"""

import pygame
from views.config import (WINDOW_WIDTH, WINDOW_HEIGHT, Colors, GameState, PanelSizes)


class GameRenderer:
    """
    Renderiza el estado completo del juego.
    
    Responsabilidades (SRP):
    - Dibujar fondo y áreas
    - Coordinar dibujado de todos los paneles
    - Renderizar estado de Game Over
    """
    
    def __init__(self, screen, game_manager):
        """
        Args:
            screen: Superficie de pygame donde dibujar
            game_manager: Instancia del GameManager con todos los componentes
        """
        self.screen = screen
        self.gm = game_manager
    
    def draw(self):
        """Dibuja todos los elementos del juego."""
        # 1. Fondo
        self.screen.fill(Colors.BACKGROUND)
        
        # 2. Área del grafo con fondo especial
        self._draw_graph_area()
        
        # 3. Grafo de constelaciones
        self._draw_graph()
        
        # 4. Paneles UI
        self._draw_panels()
        
        # 5. Editor de estrellas (encima)
        self.gm.star_editor.draw(self.screen)
        
        # 6. Notificaciones y tooltip
        self._draw_overlays()
        
        # 7. Game Over si aplica
        if self.gm.state == GameState.GAME_OVER:
            self._draw_game_over()
        
        # 8. Actualizar pantalla
        pygame.display.flip()
    
    def _draw_graph_area(self):
        """Dibuja el área de fondo del grafo."""
        graph_area = pygame.Rect(
            PanelSizes.LEFT_PANEL_WIDTH, 0,
            PanelSizes.GRAPH_WIDTH, PanelSizes.GRAPH_HEIGHT
        )
        pygame.draw.rect(self.screen, Colors.SPACE_DARK, graph_area)
    
    def _draw_graph(self):
        """Dibuja el grafo de constelaciones con el burro."""
        visited_stars = set(self.gm.simulador.historial_viaje)
        self.gm.graph_renderer.draw(
            self.screen,
            current_star_id=self.gm.simulador.posicion_actual,
            visited_stars=visited_stars
        )
    
    def _draw_panels(self):
        """Dibuja todos los paneles de información."""
        self.gm.donkey_panel.draw(self.screen)
        self.gm.reachable_panel.draw(self.screen)
        self.gm.actions_panel.draw(self.screen)
        self.gm.star_info_panel.draw(self.screen)
    
    def _draw_overlays(self):
        """Dibuja notificaciones y tooltips."""
        self.gm.notification.draw(self.screen, self.gm.normal_font)
        self.gm.tooltip.draw(self.screen, pygame.font.Font(None, 16))
    
    def _draw_game_over(self):
        """Dibuja la pantalla de Game Over."""
        # Overlay oscuro
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        # Título
        title = self.gm.title_font.render("💀 GAME OVER 💀", True, Colors.TEXT_DANGER)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
        self.screen.blit(title, title_rect)
        
        # Estadísticas finales
        self._draw_game_over_stats()
        
        # Instrucciones
        restart = self.gm.normal_font.render(
            "Presiona ESC para salir",
            True, Colors.TEXT_SECONDARY
        )
        restart_rect = restart.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 100))
        self.screen.blit(restart, restart_rect)
    
    def _draw_game_over_stats(self):
        """Dibuja las estadísticas finales en Game Over."""
        resumen = self.gm.simulador.obtener_resumen_viaje()
        stats = [
            f"Estrellas visitadas: {resumen['estrellas_visitadas']}",
            f"Distancia recorrida: {resumen['distancia_total']:.1f} ly",
            f"Edad final: {resumen['edad']:.1f} años luz",
        ]
        
        y = WINDOW_HEIGHT // 2
        for stat in stats:
            stat_surface = self.gm.normal_font.render(stat, True, Colors.TEXT_PRIMARY)
            stat_rect = stat_surface.get_rect(center=(WINDOW_WIDTH // 2, y))
            self.screen.blit(stat_surface, stat_rect)
            y += 30
