"""
Componentes UI reutilizables.
Implementa widgets comunes con estilo consistente.
"""

import pygame
from views.config import Colors, Fonts, ButtonSizes, Spacing


class Button:
    """Botón interactivo con estados hover y click."""
    
    def __init__(self, x, y, width, height, text, callback=None, 
                 enabled=True, style='normal'):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.enabled = enabled
        self.style = style
        
        self.hovered = False
        self.pressed = False
        
    def update(self, mouse_pos, mouse_pressed):
        """Actualiza el estado del botón."""
        if not self.enabled:
            self.hovered = False
            self.pressed = False
            return
        
        self.hovered = self.rect.collidepoint(mouse_pos)
        
        if self.hovered and mouse_pressed:
            self.pressed = True
        elif self.pressed and not mouse_pressed:
            # Click completado
            self.pressed = False
            if self.callback:
                self.callback()
        elif not mouse_pressed:
            self.pressed = False
    
    def draw(self, screen, font):
        """Dibuja el botón."""
        # Determinar color de fondo
        if not self.enabled:
            bg_color = Colors.BUTTON_DISABLED
            text_color = Colors.TEXT_SECONDARY
        elif self.pressed:
            bg_color = Colors.BUTTON_ACTIVE
            text_color = Colors.TEXT_PRIMARY
        elif self.hovered:
            bg_color = Colors.BUTTON_HOVER
            text_color = Colors.TEXT_PRIMARY
        else:
            bg_color = Colors.BUTTON_BG
            text_color = Colors.TEXT_SECONDARY
        
        # Dibujar fondo
        pygame.draw.rect(screen, bg_color, self.rect, border_radius=8)
        pygame.draw.rect(screen, Colors.PANEL_BORDER, self.rect, 2, border_radius=8)
        
        # Dibujar texto
        text_surface = font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    
    def set_enabled(self, enabled):
        """Habilita o deshabilita el botón."""
        self.enabled = enabled


class Panel:
    """Panel contenedor para agrupar elementos."""
    
    def __init__(self, x, y, width, height, title=None, color=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.title = title
        self.bg_color = color or Colors.PANEL_BG
        self.elements = []
        
    def draw(self, screen, title_font=None, content_font=None):
        """Dibuja el panel y su contenido."""
        # Fondo
        pygame.draw.rect(screen, self.bg_color, self.rect, border_radius=10)
        pygame.draw.rect(screen, Colors.PANEL_BORDER, self.rect, 2, border_radius=10)
        
        # Título si existe
        if self.title and title_font:
            title_surface = title_font.render(self.title, True, Colors.TEXT_TITLE)
            title_rect = title_surface.get_rect(
                centerx=self.rect.centerx,
                top=self.rect.top + Spacing.PADDING
            )
            screen.blit(title_surface, title_rect)


class ProgressBar:
    """Barra de progreso con color dinámico."""
    
    def __init__(self, x, y, width, height, max_value, current_value=0,
                 color_high=None, color_mid=None, color_low=None,
                 show_text=True, label=""):
        self.rect = pygame.Rect(x, y, width, height)
        self.max_value = max_value
        self.current_value = current_value
        
        self.color_high = color_high or Colors.ENERGY_HIGH
        self.color_mid = color_mid or Colors.ENERGY_MID
        self.color_low = color_low or Colors.ENERGY_LOW
        
        self.show_text = show_text
        self.label = label
        
    def update(self, current_value):
        """Actualiza el valor actual."""
        self.current_value = max(0, min(current_value, self.max_value))
    
    def get_color(self):
        """Determina el color basado en el porcentaje."""
        percentage = self.current_value / self.max_value if self.max_value > 0 else 0
        
        if percentage > 0.6:
            return self.color_high
        elif percentage > 0.3:
            return self.color_mid
        else:
            return self.color_low
    
    def draw(self, screen, font=None):
        """Dibuja la barra de progreso."""
        # Borde
        pygame.draw.rect(screen, Colors.PANEL_BORDER, self.rect, 2, border_radius=5)
        
        # Fondo
        bg_rect = self.rect.inflate(-4, -4)
        pygame.draw.rect(screen, Colors.SPACE_DARK, bg_rect, border_radius=3)
        
        # Barra de progreso
        if self.current_value > 0:
            percentage = self.current_value / self.max_value
            progress_width = int((self.rect.width - 4) * percentage)
            progress_rect = pygame.Rect(
                self.rect.x + 2,
                self.rect.y + 2,
                progress_width,
                self.rect.height - 4
            )
            pygame.draw.rect(screen, self.get_color(), progress_rect, border_radius=3)
        
        # Texto
        if self.show_text and font:
            text = f"{self.label}{self.current_value:.1f}/{self.max_value:.0f}"
            text_surface = font.render(text, True, Colors.TEXT_PRIMARY)
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect)


class InfoLabel:
    """Etiqueta de información con icono y valor."""
    
    def __init__(self, x, y, icon, label, value, color=None):
        self.x = x
        self.y = y
        self.icon = icon
        self.label = label
        self.value = value
        self.color = color or Colors.TEXT_PRIMARY
        
    def update(self, value):
        """Actualiza el valor."""
        self.value = value
    
    def draw(self, screen, font):
        """Dibuja la etiqueta."""
        text = f"{self.icon} {self.label}: {self.value}"
        text_surface = font.render(text, True, self.color)
        screen.blit(text_surface, (self.x, self.y))


class Tooltip:
    """Tooltip que aparece al hacer hover."""
    
    def __init__(self):
        self.text = ""
        self.visible = False
        self.position = (0, 0)
        self.padding = 10
        
    def show(self, text, position):
        """Muestra el tooltip en una posición."""
        self.text = text
        self.position = position
        self.visible = True
    
    def hide(self):
        """Oculta el tooltip."""
        self.visible = False
    
    def draw(self, screen, font):
        """Dibuja el tooltip."""
        if not self.visible or not self.text:
            return
        
        # Renderizar texto
        lines = self.text.split('\n')
        surfaces = [font.render(line, True, Colors.TEXT_PRIMARY) for line in lines]
        
        # Calcular tamaño del tooltip
        max_width = max(s.get_width() for s in surfaces)
        total_height = sum(s.get_height() for s in surfaces) + (len(surfaces) - 1) * 5
        
        width = max_width + self.padding * 2
        height = total_height + self.padding * 2
        
        # Ajustar posición para que no salga de la pantalla
        x, y = self.position
        if x + width > screen.get_width():
            x = screen.get_width() - width - 10
        if y + height > screen.get_height():
            y = screen.get_height() - height - 10
        
        # Dibujar fondo
        bg_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(screen, Colors.PANEL_BG, bg_rect, border_radius=5)
        pygame.draw.rect(screen, Colors.PANEL_BORDER, bg_rect, 2, border_radius=5)
        
        # Dibujar texto
        current_y = y + self.padding
        for surface in surfaces:
            screen.blit(surface, (x + self.padding, current_y))
            current_y += surface.get_height() + 5


class Notification:
    """Sistema de notificaciones temporales."""
    
    def __init__(self, x, y, width):
        self.x = x
        self.y = y
        self.width = width
        self.notifications = []  # Lista de (texto, color, tiempo_restante)
        
    def add(self, text, color=Colors.TEXT_PRIMARY, duration=180):
        """Añade una notificación."""
        self.notifications.append({
            'text': text,
            'color': color,
            'time': duration,
            'alpha': 255
        })
    
    def update(self):
        """Actualiza las notificaciones."""
        for notif in self.notifications[:]:
            notif['time'] -= 1
            
            # Fade out en los últimos 60 frames
            if notif['time'] < 60:
                notif['alpha'] = int((notif['time'] / 60) * 255)
            
            if notif['time'] <= 0:
                self.notifications.remove(notif)
    
    def draw(self, screen, font):
        """Dibuja las notificaciones."""
        y_offset = 0
        for notif in self.notifications:
            # Crear superficie con alpha
            text_surface = font.render(notif['text'], True, notif['color'])
            text_surface.set_alpha(notif['alpha'])
            
            # Fondo semi-transparente
            text_rect = text_surface.get_rect(centerx=self.x + self.width // 2, top=self.y + y_offset)
            bg_rect = text_rect.inflate(20, 10)
            
            bg_surface = pygame.Surface((bg_rect.width, bg_rect.height))
            bg_surface.set_alpha(int(notif['alpha'] * 0.7))
            bg_surface.fill(Colors.PANEL_BG)
            
            screen.blit(bg_surface, bg_rect)
            screen.blit(text_surface, text_rect)
            
            y_offset += text_rect.height + 15
