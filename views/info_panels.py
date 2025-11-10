"""
Paneles informativos de la interfaz.
Responsabilidad: Mostrar información del burro y estrellas.
"""

import pygame
from views.config import (Colors, Fonts, Spacing, Icons)
from views.components import Panel, ProgressBar, InfoLabel


class DonkeyInfoPanel:
    """
    Panel informativo del estado del burro.
    
    Responsabilidades (SRP):
    - Mostrar energía y pasto del burro
    - Mostrar salud y edad
    - Mostrar posición actual y distancia total
    """
    
    def __init__(self, x, y, width, height):
        self.panel = Panel(x, y, width, height, f"{Icons.DONKEY} Estado del Burro")
        
        # Fuentes
        self.title_font = pygame.font.Font(None, Fonts.SUBTITLE_SIZE)
        self.normal_font = pygame.font.Font(None, Fonts.NORMAL_SIZE)
        self.small_font = pygame.font.Font(None, Fonts.SMALL_SIZE)
        
        # Posiciones para elementos
        content_y = y + 60
        content_x = x + Spacing.PANEL_PADDING
        content_width = width - Spacing.PANEL_PADDING * 2
        
        # Barras de progreso
        self.energy_bar = ProgressBar(
            content_x, content_y, content_width, 30, 100, 100,
            label=f"{Icons.ENERGY} "
        )
        
        self.grass_bar = ProgressBar(
            content_x, content_y + 80, content_width, 25, 300, 300,
            color_high=Colors.GRASS_COLOR,
            color_mid=Colors.GRASS_COLOR,
            color_low=Colors.HEALTH_NEGATIVE,
            label=f"{Icons.GRASS} "
        )
        
        # Labels de información
        self.health_label = InfoLabel(
            content_x, content_y + 40,
            Icons.HEALTH, "Salud", "Excelente",
            Colors.HEALTH_POSITIVE
        )
        
        self.age_label = InfoLabel(
            content_x, content_y + 120,
            Icons.AGE, "Edad", "0 / 3567 años luz",
            Colors.AGE_COLOR
        )
        
        self.position_label = InfoLabel(
            content_x, content_y + 145,
            Icons.STAR, "Posición", "Estrella Inicial",
            Colors.TEXT_SECONDARY
        )
        
        self.distance_label = InfoLabel(
            content_x, content_y + 170,
            Icons.DISTANCE, "Distancia recorrida", "0 ly",
            Colors.TEXT_SECONDARY
        )
    
    def update(self, donkey, current_star_name, total_distance):
        """Actualiza la información del burro."""
        # Actualizar barras
        self.energy_bar.update(donkey.donkey_energy)
        self.grass_bar.update(donkey.grass_in_basement)
        
        # Actualizar labels
        health_color = Colors.HEALTH_POSITIVE if donkey.donkey_energy > 50 else Colors.HEALTH_NEGATIVE
        self.health_label.update(donkey.health)
        self.health_label.color = health_color
        
        self.age_label.update(f"{donkey.age:.1f} / {donkey.max_age} años luz")
        self.position_label.update(current_star_name)
        self.distance_label.update(f"{total_distance:.1f} ly")
    
    def draw(self, screen):
        """Dibuja el panel."""
        self.panel.draw(screen, self.title_font)
        
        # Dibujar barras
        self.energy_bar.draw(screen, self.small_font)
        self.grass_bar.draw(screen, self.small_font)
        
        # Dibujar labels
        self.health_label.draw(screen, self.normal_font)
        self.age_label.draw(screen, self.small_font)
        self.position_label.draw(screen, self.small_font)
        self.distance_label.draw(screen, self.small_font)


class StarInfoPanel:
    """
    Panel informativo de estrella seleccionada.
    
    Responsabilidades (SRP):
    - Mostrar propiedades de la estrella
    - Mostrar distancia y energía necesaria
    - Mostrar efectos de investigación
    """
    
    def __init__(self, x, y, width, height):
        self.panel = Panel(x, y, width, height, f"{Icons.STAR} Información de Estrella")
        self.visible = False
        
        # Fuentes
        self.title_font = pygame.font.Font(None, Fonts.SUBTITLE_SIZE)
        self.normal_font = pygame.font.Font(None, Fonts.NORMAL_SIZE)
        self.small_font = pygame.font.Font(None, Fonts.SMALL_SIZE)
        
        self.estrella = None
        self.distance_to_star = None
        self.energy_needed = None
        self.path = None
        
        self.content_x = x + Spacing.PANEL_PADDING
        self.content_y = y + 60
    
    def set_star(self, estrella, distance=None, energy_needed=None, path=None):
        """Establece la estrella a mostrar."""
        self.estrella = estrella
        self.distance_to_star = distance
        self.energy_needed = energy_needed
        self.path = path
        self.visible = True
    
    def clear(self):
        """Limpia la información."""
        self.visible = False
        self.estrella = None
    
    def draw(self, screen):
        """Dibuja el panel."""
        if not self.visible or not self.estrella:
            return
        
        self.panel.draw(screen, self.title_font)
        
        y = self.content_y
        
        # Nombre de la estrella
        name_text = f"{self.estrella.label}"
        if self.estrella.hipergigante:
            name_text += " ⭐"
        name_surface = self.normal_font.render(name_text, True, Colors.TEXT_TITLE)
        screen.blit(name_surface, (self.content_x, y))
        y += 30
        
        # Tipo
        tipo = "Hipergigante" if self.estrella.hipergigante else "Normal"
        tipo_surface = self.small_font.render(f"Tipo: {tipo}", True, Colors.TEXT_SECONDARY)
        screen.blit(tipo_surface, (self.content_x, y))
        y += 25
        
        # Constelaciones
        if self.estrella.constelaciones:
            const_text = f"Constelación: {', '.join(self.estrella.constelaciones)}"
            const_surface = self.small_font.render(const_text, True, Colors.TEXT_SECONDARY)
            screen.blit(const_surface, (self.content_x, y))
            y += 25
        
        # Distancia si está disponible
        if self.distance_to_star is not None:
            dist_surface = self.normal_font.render(
                f"{Icons.DISTANCE} Distancia: {self.distance_to_star:.1f} ly",
                True, Colors.TEXT_PRIMARY
            )
            screen.blit(dist_surface, (self.content_x, y))
            y += 30
        
        # Energía necesaria
        if self.energy_needed is not None:
            energy_surface = self.normal_font.render(
                f"{Icons.ENERGY} Energía necesaria: {self.energy_needed:.1f}",
                True, Colors.TEXT_PRIMARY
            )
            screen.blit(energy_surface, (self.content_x, y))
            y += 30
        
        # Efectos de investigación
        y += 10
        effects_title = self.normal_font.render(
            f"{Icons.INVESTIGATION} Efectos de Investigación:",
            True, Colors.TEXT_TITLE
        )
        screen.blit(effects_title, (self.content_x, y))
        y += 25
        
        # Health impact
        health_color = Colors.HEALTH_POSITIVE if self.estrella.health_impact >= 0 else Colors.HEALTH_NEGATIVE
        health_sign = "+" if self.estrella.health_impact >= 0 else ""
        health_surface = self.small_font.render(
            f"  {Icons.HEALTH} Salud: {health_sign}{self.estrella.health_impact:.1f}",
            True, health_color
        )
        screen.blit(health_surface, (self.content_x, y))
        y += 22
        
        # Life time impact
        life_color = Colors.LIFE_POSITIVE if self.estrella.life_time_impact >= 0 else Colors.LIFE_NEGATIVE
        life_sign = "+" if self.estrella.life_time_impact >= 0 else ""
        life_surface = self.small_font.render(
            f"  {Icons.AGE} Tiempo de vida: {life_sign}{self.estrella.life_time_impact:.1f} años luz",
            True, life_color
        )
        screen.blit(life_surface, (self.content_x, y))
