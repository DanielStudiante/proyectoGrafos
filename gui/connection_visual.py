"""
Renderizado de conexiones entre estrellas.
Responsabilidad: Dibujar las conexiones (aristas) del grafo.
"""

import pygame
import math
from gui.config import Colors, GraphScale


class ConnectionRenderer:
    """
    Renderiza las conexiones entre estrellas.
    
    Responsabilidades (SRP):
    - Dibujar líneas entre nodos
    - Mostrar distancias en las conexiones
    - Aplicar estilos según estado (path seleccionado, etc.)
    """
    
    @staticmethod
    def draw_connection(screen, star1_renderer, star2_renderer, 
                       distance, is_path=False, show_weights=True):
        """
        Dibuja una conexión entre dos estrellas.
        
        Args:
            screen: Superficie de pygame
            star1_renderer: StarRenderer de la estrella origen
            star2_renderer: StarRenderer de la estrella destino
            distance: Distancia entre las estrellas
            is_path: Si es parte del camino seleccionado
            show_weights: Si mostrar la distancia en la línea
        """
        # Coordenadas de inicio y fin
        x1, y1 = star1_renderer.screen_x, star1_renderer.screen_y
        x2, y2 = star2_renderer.screen_x, star2_renderer.screen_y
        
        # Color y grosor según si es parte del path
        if is_path:
            color = Colors.CONNECTION_ACTIVE
            width = GraphScale.ACTIVE_CONNECTION_WIDTH
        else:
            color = Colors.CONNECTION
            width = GraphScale.CONNECTION_WIDTH
        
        # Dibujar línea
        pygame.draw.line(screen, color, (x1, y1), (x2, y2), width)
        
        # Dibujar distancia en el medio de la línea
        if show_weights:
            ConnectionRenderer._draw_distance_label(
                screen, x1, y1, x2, y2, distance, is_path
            )
    
    @staticmethod
    def _draw_distance_label(screen, x1, y1, x2, y2, distance, is_path):
        """Dibuja la etiqueta de distancia en el medio de la conexión."""
        # Posición del label (centro de la línea)
        mid_x = (x1 + x2) // 2
        mid_y = (y1 + y2) // 2
        
        # Crear el texto
        font_size = 18 if is_path else 14
        font = pygame.font.Font(None, font_size)
        text_color = Colors.TEXT_TITLE if is_path else Colors.TEXT_SECONDARY
        text = font.render(f"{distance:.1f}", True, text_color)
        text_rect = text.get_rect(center=(mid_x, mid_y))
        
        # Fondo del label
        bg_rect = text_rect.inflate(6, 4)
        bg_color = Colors.CONNECTION_ACTIVE if is_path else Colors.PANEL_BG
        alpha = 220 if is_path else 180
        
        bg_surface = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
        bg_surface.fill((*bg_color, alpha))
        screen.blit(bg_surface, bg_rect)
        
        # Dibujar texto
        screen.blit(text, text_rect)
    
    @staticmethod
    def draw_all_connections(screen, star_renderers, grafo, 
                           selected_path=None, show_weights=True):
        """
        Dibuja todas las conexiones del grafo.
        
        Args:
            screen: Superficie de pygame
            star_renderers: Dict[str, StarRenderer]
            grafo: GrafoConstelaciones
            selected_path: Lista de estrellas en el camino seleccionado
            show_weights: Si mostrar las distancias
        """
        # Convertir path a set de conexiones
        path_edges = set()
        if selected_path:
            for i in range(len(selected_path) - 1):
                edge = tuple(sorted([selected_path[i], selected_path[i + 1]]))
                path_edges.add(edge)
        
        # Dibujar todas las conexiones
        drawn_edges = set()
        
        for star_label in grafo.estrellas:
            star = grafo.estrellas[star_label]
            
            for connection in star.conexiones:
                neighbor_label = connection.destino.label
                
                # Evitar dibujar la misma arista dos veces
                edge = tuple(sorted([star_label, neighbor_label]))
                if edge in drawn_edges:
                    continue
                drawn_edges.add(edge)
                
                # Verificar si los renderers existen
                if star_label not in star_renderers or neighbor_label not in star_renderers:
                    continue
                
                # Verificar si es parte del path
                is_path = edge in path_edges
                
                # Dibujar la conexión
                ConnectionRenderer.draw_connection(
                    screen,
                    star_renderers[star_label],
                    star_renderers[neighbor_label],
                    connection.distancia,
                    is_path=is_path,
                    show_weights=show_weights
                )
