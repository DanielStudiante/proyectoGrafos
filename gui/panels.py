"""
Paneles de información y control de la interfaz.
"""

import pygame
from gui.config import (Colors, Fonts, PanelSizes, Spacing, Icons,
                        ButtonSizes)
from gui.components import Panel, ProgressBar, InfoLabel, Button


class DonkeyInfoPanel:
    """Panel que muestra información del burro."""
    
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
    """Panel que muestra información de la estrella seleccionada."""
    
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


class ActionsPanel:
    """Panel de acciones disponibles."""
    
    def __init__(self, x, y, width, height, on_travel=None, on_eat=None, 
                 on_investigate=None, on_config=None):
        self.panel = Panel(x, y, width, height, "🎮 Acciones")
        
        # Fuentes
        self.title_font = pygame.font.Font(None, Fonts.SUBTITLE_SIZE)
        self.button_font = pygame.font.Font(None, Fonts.NORMAL_SIZE)
        
        # Callbacks
        self.on_travel = on_travel
        self.on_eat = on_eat
        self.on_investigate = on_investigate
        self.on_config = on_config
        
        # Botones
        btn_x = x + (width - ButtonSizes.WIDTH) // 2
        btn_y = y + 60
        btn_spacing = ButtonSizes.HEIGHT + Spacing.BUTTON_SPACING
        
        self.travel_button = Button(
            btn_x, btn_y, ButtonSizes.WIDTH, ButtonSizes.HEIGHT,
            f"{Icons.TRAVEL} Viajar a Estrella", on_travel
        )
        
        self.eat_button = Button(
            btn_x, btn_y + btn_spacing, ButtonSizes.WIDTH, ButtonSizes.HEIGHT,
            f"{Icons.EAT} Comer Pasto (5 kg)", on_eat
        )
        
        self.investigate_button = Button(
            btn_x, btn_y + btn_spacing * 2, ButtonSizes.WIDTH, ButtonSizes.HEIGHT,
            f"{Icons.INVESTIGATION} Investigar", on_investigate
        )
        
        self.config_button = Button(
            btn_x, btn_y + btn_spacing * 3, ButtonSizes.SMALL_WIDTH, ButtonSizes.SMALL_HEIGHT,
            "⚙️ Configurar", on_config
        )
        
        self.buttons = [
            self.travel_button,
            self.eat_button,
            self.investigate_button,
            self.config_button
        ]
    
    def update(self, mouse_pos, mouse_pressed, can_travel=False, has_grass=True):
        """Actualiza el estado de los botones."""
        self.travel_button.set_enabled(can_travel)
        self.eat_button.set_enabled(has_grass)
        
        for button in self.buttons:
            button.update(mouse_pos, mouse_pressed)
    
    def draw(self, screen):
        """Dibuja el panel."""
        self.panel.draw(screen, self.title_font)
        
        for button in self.buttons:
            button.draw(screen, self.button_font)


class ReachableStarsPanel:
    """Panel que muestra estrellas alcanzables."""
    
    def __init__(self, x, y, width, height):
        self.panel = Panel(x, y, width, height, "🌟 Estrellas Alcanzables")
        
        # Fuentes
        self.title_font = pygame.font.Font(None, Fonts.SUBTITLE_SIZE)
        self.normal_font = pygame.font.Font(None, Fonts.SMALL_SIZE)
        
        self.reachable = []
        self.content_x = x + Spacing.PANEL_PADDING
        self.content_y = y + 60
        
        # Scroll
        self.scroll_offset = 0
        self.max_visible = 5
    
    def set_reachable(self, reachable_list):
        """Establece la lista de estrellas alcanzables."""
        self.reachable = reachable_list
        self.scroll_offset = 0
    
    def draw(self, screen):
        """Dibuja el panel."""
        self.panel.draw(screen, self.title_font)
        
        if not self.reachable:
            no_stars = self.normal_font.render(
                "No hay estrellas alcanzables",
                True, Colors.TEXT_SECONDARY
            )
            screen.blit(no_stars, (self.content_x, self.content_y))
            return
        
        y = self.content_y
        visible_count = 0
        
        for i, star_info in enumerate(self.reachable):
            if i < self.scroll_offset:
                continue
            if visible_count >= self.max_visible:
                break
            
            # Nombre y distancia
            label = star_info.get('label', f"Estrella {star_info['id']}")
            text = f"{label}: {star_info['distancia']:.0f} ly"
            text_surface = self.normal_font.render(text, True, Colors.TEXT_PRIMARY)
            screen.blit(text_surface, (self.content_x, y))
            
            y += 25
            visible_count += 1
