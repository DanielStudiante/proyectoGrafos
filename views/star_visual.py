"""
Renderizado visual de estrellas individuales.
Responsabilidad: Dibujar y animar una estrella con sus efectos visuales.
"""

import pygame
import math
from views.config import Colors, GraphScale, Animation, VisualEffects


class StarRenderer:
    """
    Renderiza una estrella individual con efectos visuales.
    
    Responsabilidades (SRP):
    - Calcular posición y tamaño visual
    - Animar efectos (pulso, glow)
    - Detectar interacción del mouse
    - Dibujar la estrella y su etiqueta
    """
    
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
    
    def get_color(self, is_current=False, is_visited=False, grafo=None):
        """
        Determina el color de la estrella según su estado y constelación.
        
        REQUERIMIENTO: Cada constelación debe tener un color diferente.
        Si una estrella pertenece a varias constelaciones, se resalta en ROJO.
        """
        # Prioridad 1: Estrella actual (donde está el burro)
        if is_current:
            return Colors.STAR_CURRENT
        
        # Prioridad 2: Hover (interacción del usuario)
        elif self.hover:
            return Colors.STAR_HOVER
        
        # Prioridad 3: Múltiples constelaciones - ROJO (REQUERIMIENTO)
        elif grafo and len(self.estrella.constelaciones) > 1:
            return Colors.STAR_MULTI_CONSTELLATION
        
        # Prioridad 4: Visitada
        elif is_visited:
            return Colors.STAR_VISITED
        
        # Prioridad 5: Color por constelación (REQUERIMIENTO)
        elif grafo and self.estrella.constelaciones:
            # Obtener el color de la primera constelación
            primera_constelacion = self.estrella.constelaciones[0]
            color_index = grafo.obtener_color_constelacion(primera_constelacion)
            return Colors.CONSTELLATION_COLORS.get(color_index, Colors.STAR_NORMAL)
        
        # Prioridad 6: Hipergigante (fallback)
        elif self.estrella.hipergigante:
            return Colors.STAR_HYPERGIANT
        
        # Default
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
    
    def draw(self, screen, is_current=False, is_visited=False, grafo=None):
        """Dibuja la estrella con su color según constelación."""
        color = self.get_color(is_current, is_visited, grafo)
        
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
            self._draw_glow(screen, draw_radius)
        
        # Estrella principal
        pygame.draw.circle(screen, color, (self.screen_x, self.screen_y), draw_radius)
        
        # Borde si es hipergigante
        if self.estrella.hipergigante:
            pygame.draw.circle(screen, Colors.TEXT_TITLE, 
                             (self.screen_x, self.screen_y), draw_radius + 2, 2)
        
        # Label (solo si hay hover o es actual)
        if self.hover or is_current:
            self._draw_label(screen)
    
    def _draw_glow(self, screen, draw_radius):
        """Dibuja el efecto de brillo alrededor de la estrella."""
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


class DonkeyRenderer:
    """
    Renderiza el burro en la estrella actual.
    
    Responsabilidades (SRP):
    - Dibujar el burro como figura
    - Animar rebote del burro
    - Posicionar sobre la estrella actual
    """
    
    def __init__(self):
        self.bounce = 0
        self.bounce_speed = 0.1
    
    def update(self):
        """Actualiza la animación del burro."""
        self.bounce += self.bounce_speed
        if self.bounce > math.pi * 2:
            self.bounce -= math.pi * 2
    
    def draw(self, screen, star_renderer):
        """Dibuja el burro encima de la estrella."""
        if not star_renderer:
            return
        
        # Calcular rebote (movimiento vertical)
        bounce_offset = math.sin(self.bounce) * 5
        
        # Posición del burro (encima de la estrella con rebote)
        donkey_x = star_renderer.screen_x
        donkey_y = star_renderer.screen_y - star_renderer.radius - 35 + bounce_offset
        
        # Tamaño del burro
        donkey_size = 18
        
        # Glow effect
        if VisualEffects.GLOW_ENABLED:
            self._draw_glow(screen, donkey_x, donkey_y, donkey_size)
        
        # Dibujar el burro como una figura simple
        self._draw_donkey_body(screen, donkey_x, donkey_y, donkey_size)
        self._draw_donkey_label(screen, donkey_x, donkey_y, donkey_size)
    
    def _draw_glow(self, screen, x, y, size):
        """Dibuja el brillo alrededor del burro."""
        glow_surface = pygame.Surface((size * 4, size * 4), pygame.SRCALPHA)
        for i in range(size + 12, 0, -2):
            alpha = int((i / (size + 12)) * 80)
            glow_color = (255, 200, 100, alpha)  # Dorado
            pygame.draw.circle(glow_surface, glow_color, 
                             (size * 2, size * 2), i)
        glow_rect = glow_surface.get_rect(center=(int(x), int(y)))
        screen.blit(glow_surface, glow_rect)
    
    def _draw_donkey_body(self, screen, x, y, size):
        """Dibuja el cuerpo del burro."""
        body_color = (139, 90, 43)  # Marrón burro
        outline_color = (90, 60, 30)  # Marrón oscuro
        
        # Cuerpo principal (elipse)
        body_rect = pygame.Rect(0, 0, size * 2, size * 1.3)
        body_rect.center = (int(x), int(y))
        pygame.draw.ellipse(screen, outline_color, body_rect)
        pygame.draw.ellipse(screen, body_color, body_rect.inflate(-4, -4))
        
        # Cabeza (círculo)
        head_x = int(x - size * 0.7)
        head_y = int(y - size * 0.3)
        head_radius = int(size * 0.6)
        pygame.draw.circle(screen, outline_color, (head_x, head_y), head_radius)
        pygame.draw.circle(screen, body_color, (head_x, head_y), head_radius - 2)
        
        # Orejas (dos líneas hacia arriba)
        ear_length = int(size * 0.5)
        pygame.draw.line(screen, outline_color, 
                        (head_x - 3, head_y - head_radius + 2),
                        (head_x - 5, head_y - head_radius - ear_length), 3)
        pygame.draw.line(screen, outline_color, 
                        (head_x + 3, head_y - head_radius + 2),
                        (head_x + 5, head_y - head_radius - ear_length), 3)
        
        # Patas (4 líneas)
        leg_length = int(size * 0.6)
        leg_y_start = body_rect.bottom - 2
        pygame.draw.line(screen, outline_color, 
                        (body_rect.left + 5, leg_y_start), 
                        (body_rect.left + 5, leg_y_start + leg_length), 3)
        pygame.draw.line(screen, outline_color, 
                        (body_rect.left + 10, leg_y_start), 
                        (body_rect.left + 10, leg_y_start + leg_length), 3)
        pygame.draw.line(screen, outline_color, 
                        (body_rect.right - 10, leg_y_start), 
                        (body_rect.right - 10, leg_y_start + leg_length), 3)
        pygame.draw.line(screen, outline_color, 
                        (body_rect.right - 5, leg_y_start), 
                        (body_rect.right - 5, leg_y_start + leg_length), 3)
    
    def _draw_donkey_label(self, screen, x, y, size):
        """Dibuja la etiqueta BURRO."""
        leg_length = int(size * 0.6)
        font = pygame.font.Font(None, 16)
        label_text = font.render("BURRO", True, Colors.TEXT_PRIMARY)
        label_rect = label_text.get_rect(center=(int(x), int(y + size + leg_length + 8)))
        
        # Fondo del label
        bg_rect = label_rect.inflate(6, 2)
        bg_surface = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
        bg_surface.fill((*Colors.PANEL_BG, 200))
        screen.blit(bg_surface, bg_rect)
        screen.blit(label_text, label_rect)
