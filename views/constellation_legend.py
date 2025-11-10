"""
Leyenda de constelaciones y sus colores.
Muestra qué color corresponde a cada constelación.
"""

import pygame
from views.config import Colors, Fonts, Spacing


class ConstellationLegend:
    """
    Muestra una leyenda con los colores de cada constelación.
    
    REQUERIMIENTO: Cada constelación debe tener un color diferente.
    Esta leyenda ayuda al usuario a identificar las constelaciones.
    """
    
    def __init__(self, grafo, x, y, width=300, max_height=200):
        self.grafo = grafo
        self.x = x
        self.y = y
        self.width = width
        self.max_height = max_height
        
        # Fuentes
        try:
            self.font_title = pygame.font.Font(None, Fonts.SUBTITLE_SIZE)
            self.font_item = pygame.font.Font(None, Fonts.SMALL_SIZE)
        except:
            self.font_title = pygame.font.SysFont('Arial', Fonts.SUBTITLE_SIZE)
            self.font_item = pygame.font.SysFont('Arial', Fonts.SMALL_SIZE)
    
    def draw(self, screen):
        """Dibuja la leyenda de constelaciones."""
        constelaciones = sorted(self.grafo.listar_constelaciones())
        
        if not constelaciones:
            return
        
        # Fondo del panel
        panel_height = min(
            self.max_height,
            60 + len(constelaciones) * 25 + Spacing.PADDING * 2
        )
        
        panel_rect = pygame.Rect(self.x, self.y, self.width, panel_height)
        pygame.draw.rect(screen, Colors.PANEL_BG, panel_rect)
        pygame.draw.rect(screen, Colors.PANEL_BORDER, panel_rect, 2)
        
        # Título
        title_surface = self.font_title.render("Constelaciones", True, Colors.TEXT_TITLE)
        title_rect = title_surface.get_rect(
            centerx=self.x + self.width // 2,
            top=self.y + Spacing.PADDING
        )
        screen.blit(title_surface, title_rect)
        
        # Items
        item_y = self.y + 50
        
        for i, nombre_constelacion in enumerate(constelaciones):
            if item_y + 25 > self.y + panel_height - Spacing.PADDING:
                break  # No caben más items
            
            # Obtener color de la constelación
            color_index = self.grafo.obtener_color_constelacion(nombre_constelacion)
            color = Colors.CONSTELLATION_COLORS.get(color_index, Colors.STAR_NORMAL)
            
            # Círculo de color
            circle_x = self.x + Spacing.PADDING + 10
            circle_y = item_y + 10
            pygame.draw.circle(screen, color, (circle_x, circle_y), 8)
            pygame.draw.circle(screen, Colors.TEXT_PRIMARY, (circle_x, circle_y), 8, 1)
            
            # Nombre de la constelación
            text_surface = self.font_item.render(nombre_constelacion, True, Colors.TEXT_PRIMARY)
            text_rect = text_surface.get_rect(
                left=circle_x + 20,
                centery=circle_y
            )
            screen.blit(text_surface, text_rect)
            
            # Contar estrellas en esta constelación
            star_count = len(self.grafo.obtener_constelacion(nombre_constelacion))
            count_text = f"({star_count})"
            count_surface = self.font_item.render(count_text, True, Colors.TEXT_SECONDARY)
            count_rect = count_surface.get_rect(
                right=self.x + self.width - Spacing.PADDING,
                centery=circle_y
            )
            screen.blit(count_surface, count_rect)
            
            item_y += 25
        
        # Nota sobre estrellas con múltiples constelaciones
        note_y = self.y + panel_height - 30
        if note_y > item_y + 10:
            # Círculo rojo de ejemplo
            circle_x = self.x + Spacing.PADDING + 10
            pygame.draw.circle(screen, Colors.STAR_MULTI_CONSTELLATION, 
                             (circle_x, note_y + 10), 6)
            
            # Texto explicativo
            note_text = "= Múltiples constelaciones"
            note_surface = self.font_item.render(note_text, True, Colors.TEXT_SECONDARY)
            note_rect = note_surface.get_rect(
                left=circle_x + 15,
                centery=note_y + 10
            )
            screen.blit(note_surface, note_rect)


class ScaleLegend:
    """
    Muestra la escala del tablero (200um x 200um mínimo).
    """
    
    def __init__(self, x, y, width=300):
        self.x = x
        self.y = y
        self.width = width
        
        try:
            self.font = pygame.font.Font(None, Fonts.SMALL_SIZE)
        except:
            self.font = pygame.font.SysFont('Arial', Fonts.SMALL_SIZE)
    
    def draw(self, screen, board_width_um, board_height_um):
        """
        Dibuja información sobre la escala del tablero.
        
        Args:
            board_width_um: Ancho del tablero en unidades de medida
            board_height_um: Alto del tablero en unidades de medida
        """
        # Fondo
        panel_rect = pygame.Rect(self.x, self.y, self.width, 80)
        pygame.draw.rect(screen, Colors.PANEL_BG, panel_rect)
        pygame.draw.rect(screen, Colors.PANEL_BORDER, panel_rect, 2)
        
        # Título
        title = "Escala del Tablero"
        title_surface = self.font.render(title, True, Colors.TEXT_TITLE)
        title_rect = title_surface.get_rect(
            centerx=self.x + self.width // 2,
            top=self.y + 10
        )
        screen.blit(title_surface, title_rect)
        
        # Dimensiones
        dims_text = f"{board_width_um} um × {board_height_um} um"
        dims_surface = self.font.render(dims_text, True, Colors.TEXT_PRIMARY)
        dims_rect = dims_surface.get_rect(
            centerx=self.x + self.width // 2,
            top=self.y + 35
        )
        screen.blit(dims_surface, dims_rect)
        
        # Nota
        note = "Vías bidireccionales"
        note_surface = self.font.render(note, True, Colors.TEXT_SECONDARY)
        note_rect = note_surface.get_rect(
            centerx=self.x + self.width // 2,
            top=self.y + 55
        )
        screen.blit(note_surface, note_rect)
