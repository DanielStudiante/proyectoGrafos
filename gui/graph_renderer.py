"""
Sistema de renderizado del grafo de estrellas.
Maneja la visualización, interacción y animaciones del grafo.
"""

import pygame
import math
from gui.config import (Colors, GraphScale, Animation, VisualEffects,
                        PanelSizes, Icons)


class StarRenderer:
    """Renderiza una estrella individual con efectos visuales."""
    
    def __init__(self, estrella, screen_x, screen_y):
        self.estrella = estrella
        self.screen_x = screen_x
        self.screen_y = screen_y
        
        # Estado visual
        self.pulse_offset = 0
        self.glow_alpha = 0
        self.hover = False
        
        # Radio en pantalla
        self.radius = self._calculate_radius()
        
    def _calculate_radius(self):
        """Calcula el radio visual de la estrella."""
        base_radius = self.estrella.radius * 10
        return max(GraphScale.MIN_STAR_RADIUS, 
                   min(GraphScale.MAX_STAR_RADIUS, base_radius))
    
    def get_color(self, is_current=False, is_visited=False):
        """Determina el color de la estrella según su estado."""
        if is_current:
            return Colors.STAR_CURRENT
        elif self.hover:
            return Colors.STAR_HOVER
        elif is_visited:
            return Colors.STAR_VISITED
        elif self.estrella.hipergigante:
            return Colors.STAR_HYPERGIANT
        else:
            return Colors.STAR_NORMAL
    
    def update(self, mouse_pos, is_current=False):
        """Actualiza el estado de la estrella."""
        # Detectar hover
        dx = mouse_pos[0] - self.screen_x
        dy = mouse_pos[1] - self.screen_y
        distance = math.sqrt(dx*dx + dy*dy)
        self.hover = distance < self.radius
        
        # Animar pulso para estrella actual
        if is_current:
            self.pulse_offset += Animation.STAR_PULSE_SPEED
            if self.pulse_offset > math.pi * 2:
                self.pulse_offset -= math.pi * 2
        else:
            self.pulse_offset = 0
        
        # Glow en hover
        if self.hover:
            self.glow_alpha = min(255, self.glow_alpha + 15)
        else:
            self.glow_alpha = max(0, self.glow_alpha - 15)
    
    def draw(self, screen, is_current=False, is_visited=False):
        """Dibuja la estrella."""
        color = self.get_color(is_current, is_visited)
        
        # Calcular radio con pulso
        pulse_scale = 1.0
        if is_current and VisualEffects.ANIMATIONS_ENABLED:
            pulse = math.sin(self.pulse_offset)
            pulse_scale = Animation.STAR_PULSE_MIN + \
                         (Animation.STAR_PULSE_MAX - Animation.STAR_PULSE_MIN) * \
                         ((pulse + 1) / 2)
        
        draw_radius = int(self.radius * pulse_scale)
        
        # Glow effect
        if VisualEffects.GLOW_ENABLED and (self.hover or is_current):
            glow_surface = pygame.Surface((draw_radius * 4, draw_radius * 4), pygame.SRCALPHA)
            glow_radius = int(draw_radius * 1.5)
            
            # Gradiente de glow
            for i in range(glow_radius, 0, -2):
                alpha = int((i / glow_radius) * self.glow_alpha * 0.3)
                glow_color = (*Colors.STAR_GLOW, alpha)
                pygame.draw.circle(glow_surface, glow_color, 
                                 (draw_radius * 2, draw_radius * 2), i)
            
            glow_rect = glow_surface.get_rect(center=(self.screen_x, self.screen_y))
            screen.blit(glow_surface, glow_rect)
        
        # Estrella principal
        pygame.draw.circle(screen, color, (self.screen_x, self.screen_y), draw_radius)
        
        # Borde si es hipergigante
        if self.estrella.hipergigante:
            pygame.draw.circle(screen, Colors.TEXT_TITLE, 
                             (self.screen_x, self.screen_y), draw_radius + 2, 2)
        
        # Label (solo si hay hover o es actual)
        if self.hover or is_current:
            self._draw_label(screen)
    
    def _draw_label(self, screen):
        """Dibuja el nombre de la estrella."""
        font = pygame.font.Font(None, 20)
        text_surface = font.render(self.estrella.label, True, Colors.TEXT_PRIMARY)
        text_rect = text_surface.get_rect(
            centerx=self.screen_x,
            bottom=self.screen_y - self.radius - 5
        )
        
        # Fondo del label
        bg_rect = text_rect.inflate(8, 4)
        bg_surface = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
        bg_surface.fill((*Colors.PANEL_BG, 200))
        screen.blit(bg_surface, bg_rect)
        
        screen.blit(text_surface, text_rect)
    
    def contains_point(self, point):
        """Verifica si un punto está dentro de la estrella."""
        dx = point[0] - self.screen_x
        dy = point[1] - self.screen_y
        return math.sqrt(dx*dx + dy*dy) < self.radius


class ConnectionRenderer:
    """Renderiza conexiones entre estrellas."""
    
    @staticmethod
    def draw_connection(screen, star1_pos, star2_pos, distance, 
                       is_active=False, alpha=255):
        """Dibuja una conexión entre dos estrellas."""
        color = Colors.CONNECTION_ACTIVE if is_active else Colors.CONNECTION
        width = GraphScale.ACTIVE_CONNECTION_WIDTH if is_active else GraphScale.CONNECTION_WIDTH
        
        # Crear superficie con alpha
        if alpha < 255:
            # Para transparencia, dibujamos en una superficie temporal
            surface = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
            pygame.draw.line(surface, (*color, alpha), star1_pos, star2_pos, width)
            screen.blit(surface, (0, 0))
        else:
            pygame.draw.line(screen, color, star1_pos, star2_pos, width)
        
        # Mostrar distancia en conexiones activas
        if is_active:
            ConnectionRenderer._draw_distance_label(screen, star1_pos, star2_pos, distance)
    
    @staticmethod
    def _draw_distance_label(screen, pos1, pos2, distance):
        """Dibuja la etiqueta de distancia en el medio de la conexión."""
        mid_x = (pos1[0] + pos2[0]) // 2
        mid_y = (pos1[1] + pos2[1]) // 2
        
        font = pygame.font.Font(None, 16)
        text = f"{distance:.0f} ly"
        text_surface = font.render(text, True, Colors.TEXT_SECONDARY)
        text_rect = text_surface.get_rect(center=(mid_x, mid_y))
        
        # Fondo
        bg_rect = text_rect.inflate(6, 3)
        pygame.draw.rect(screen, Colors.SPACE_DARK, bg_rect, border_radius=3)
        
        screen.blit(text_surface, text_rect)


class GraphRenderer:
    """Renderiza el grafo completo de constelaciones."""
    
    def __init__(self, grafo, offset_x=0, offset_y=0):
        self.grafo = grafo
        self.offset_x = offset_x + GraphScale.OFFSET_X
        self.offset_y = offset_y + GraphScale.OFFSET_Y
        
        # Scroll y zoom (inicializar ANTES de crear renderers)
        self.zoom = 1.0
        self.pan_x = 0
        self.pan_y = 0
        
        # Crear renderizadores de estrellas
        self.star_renderers = {}
        self._create_star_renderers()
        
        # Camino activo
        self.active_path = []
        
    def _create_star_renderers(self):
        """Crea renderizadores para cada estrella."""
        for star_id, estrella in self.grafo.estrellas.items():
            screen_x, screen_y = self._world_to_screen(estrella.x, estrella.y)
            self.star_renderers[star_id] = StarRenderer(estrella, screen_x, screen_y)
    
    def _world_to_screen(self, world_x, world_y):
        """Convierte coordenadas del mundo a coordenadas de pantalla."""
        screen_x = int(world_x * GraphScale.SCALE_FACTOR + self.offset_x + self.pan_x)
        screen_y = int(world_y * GraphScale.SCALE_FACTOR + self.offset_y + self.pan_y)
        return screen_x, screen_y
    
    def update(self, mouse_pos, current_star_id=None):
        """Actualiza el estado del grafo."""
        for star_id, renderer in self.star_renderers.items():
            is_current = (star_id == current_star_id)
            renderer.update(mouse_pos, is_current)
    
    def draw(self, screen, current_star_id=None, visited_stars=None):
        """Dibuja el grafo completo."""
        visited_stars = visited_stars or set()
        
        # 1. Dibujar conexiones primero (debajo de las estrellas)
        self._draw_connections(screen)
        
        # 2. Dibujar camino activo
        if self.active_path:
            self._draw_active_path(screen)
        
        # 3. Dibujar estrellas
        for star_id, renderer in self.star_renderers.items():
            is_current = (star_id == current_star_id)
            is_visited = star_id in visited_stars
            renderer.draw(screen, is_current, is_visited)
    
    def _draw_connections(self, screen):
        """Dibuja todas las conexiones entre estrellas."""
        drawn_connections = set()
        
        for star_id, vertex in self.grafo.graph.items():
            star1_renderer = self.star_renderers.get(star_id)
            if not star1_renderer:
                continue
            
            for neighbor_vertex, distance in vertex.get_connections().items():
                neighbor_id = neighbor_vertex.id
                
                # Evitar dibujar la misma conexión dos veces
                connection_key = tuple(sorted([star_id, neighbor_id]))
                if connection_key in drawn_connections:
                    continue
                drawn_connections.add(connection_key)
                
                star2_renderer = self.star_renderers.get(neighbor_id)
                if not star2_renderer:
                    continue
                
                ConnectionRenderer.draw_connection(
                    screen,
                    (star1_renderer.screen_x, star1_renderer.screen_y),
                    (star2_renderer.screen_x, star2_renderer.screen_y),
                    distance
                )
    
    def _draw_active_path(self, screen):
        """Dibuja el camino activo resaltado."""
        for i in range(len(self.active_path) - 1):
            star1_id = self.active_path[i]
            star2_id = self.active_path[i + 1]
            
            star1_renderer = self.star_renderers.get(star1_id)
            star2_renderer = self.star_renderers.get(star2_id)
            
            if not star1_renderer or not star2_renderer:
                continue
            
            # Obtener distancia
            vertex = self.grafo.graph.get(star1_id)
            if vertex:
                neighbor_vertex = self.grafo.get_vertex(star2_id)
                distance = vertex.get_connections().get(neighbor_vertex, 0)
                
                ConnectionRenderer.draw_connection(
                    screen,
                    (star1_renderer.screen_x, star1_renderer.screen_y),
                    (star2_renderer.screen_x, star2_renderer.screen_y),
                    distance,
                    is_active=True
                )
    
    def set_active_path(self, path):
        """Establece el camino activo a destacar."""
        self.active_path = path or []
    
    def get_star_at_position(self, pos):
        """Obtiene la estrella en una posición de pantalla."""
        for star_id, renderer in self.star_renderers.items():
            if renderer.contains_point(pos):
                return star_id
        return None
    
    def get_reachable_stars(self, from_star_id, max_energy):
        """Obtiene estrellas alcanzables desde una posición con energía máxima."""
        from algorithms.dijkstra import obtener_estrellas_alcanzables
        return obtener_estrellas_alcanzables(self.grafo, from_star_id, max_energy)
