"""
Paneles de acciones de la interfaz.
Responsabilidad: Gestionar botones de acción y estrellas alcanzables.
"""

import pygame
from views.config import (Colors, Fonts, Spacing, Icons, ButtonSizes)
from views.components import Panel, Button


class ActionsPanel:
    """
    Panel con botones de acciones disponibles.
    
    Responsabilidades (SRP):
    - Mostrar botones de acción (viajar, comer, investigar)
    - Gestionar callbacks de botones
    - Actualizar estado de botones según contexto
    """
    
    def __init__(self, x, y, width, height, on_travel=None, on_eat=None, 
                 on_investigate=None, on_config=None, on_calculate_route=None,
                 on_optimal_route_grass=None, on_intergalactic_travel=None):
        self.panel = Panel(x, y, width, height, "🎮 Acciones")
        
        # Fuentes
        self.title_font = pygame.font.Font(None, Fonts.SUBTITLE_SIZE)
        self.button_font = pygame.font.Font(None, Fonts.NORMAL_SIZE)
        
        # Callbacks
        self.on_travel = on_travel
        self.on_eat = on_eat
        self.on_investigate = on_investigate
        self.on_config = on_config
        self.on_calculate_route = on_calculate_route
        self.on_optimal_route_grass = on_optimal_route_grass
        self.on_intergalactic_travel = on_intergalactic_travel
        
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
        
        # Botón para calcular ruta óptima (REQUERIMIENTO 1.2)
        self.calculate_route_button = Button(
            btn_x, btn_y + btn_spacing * 4, ButtonSizes.WIDTH, ButtonSizes.HEIGHT,
            "⭐ Máximo de Estrellas", on_calculate_route
        )
        
        # Botón para ruta óptima con pasto (REQUERIMIENTO 2.0)
        self.optimal_grass_button = Button(
            btn_x, btn_y + btn_spacing * 5, ButtonSizes.WIDTH, ButtonSizes.HEIGHT,
            "🌾 Ruta con Pasto", on_optimal_route_grass
        )
        
        # Botón para viaje inter-galáctico (REQUERIMIENTO c)
        self.intergalactic_button = Button(
            btn_x, btn_y + btn_spacing * 6, ButtonSizes.WIDTH, ButtonSizes.HEIGHT,
            "🌌 Viaje Inter-Galáctico", on_intergalactic_travel
        )
        
        self.buttons = [
            self.travel_button,
            self.eat_button,
            self.investigate_button,
            self.config_button,
            self.calculate_route_button,
            self.optimal_grass_button,
            self.intergalactic_button
        ]
    
    def update(self, mouse_pos, mouse_pressed, can_travel=False, has_grass=True, 
               is_on_hypergiant=False):
        """Actualiza el estado de los botones."""
        self.travel_button.set_enabled(can_travel)
        self.eat_button.set_enabled(has_grass)
        self.intergalactic_button.set_enabled(is_on_hypergiant)
        
        for button in self.buttons:
            button.update(mouse_pos, mouse_pressed)
    
    def draw(self, screen):
        """Dibuja el panel."""
        self.panel.draw(screen, self.title_font)
        
        for button in self.buttons:
            button.draw(screen, self.button_font)


class ReachableStarsPanel:
    """
    Panel de estrellas alcanzables desde posición actual.
    
    Responsabilidades (SRP):
    - Mostrar lista de estrellas alcanzables
    - Mostrar distancia a cada estrella
    - Gestionar scroll si hay muchas estrellas
    """
    
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
