"""
Panel de viaje inter-galáctico.
Aparece cuando el burro está en una estrella hipergigante.
"""

import pygame
from typing import List, Dict, Optional
from views.config import Colors, PanelSizes
from views.components import Panel, Button


class IntergalacticTravelPanel:
    """
    Panel para seleccionar destino de viaje inter-galáctico.
    
    Responsabilidades (SRP):
    - Mostrar galaxias alcanzables
    - Listar estrellas de destino
    - Confirmar viaje
    """
    
    def __init__(self, x, y, width, height):
        self.panel = Panel(x, y, width, height, "🌌 Viaje Inter-Galáctico")
        self.visible = False
        
        self.current_star_id = None
        self.grafo = None
        self.donkey = None
        
        # Posición del panel
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        # Galaxias alcanzables
        self.available_galaxies = {}  # {nombre: distancia}
        self.selected_galaxy = None
        
        # Estrellas de destino
        self.destination_stars = []
        self.selected_destination = None
        
        # Botones
        button_y = y + 50
        self.galaxy_buttons = []
        self.star_buttons = []
        
        self.travel_button = Button(
            x + 10,
            y + height - 80,
            width - 20,
            30,
            "🚀 VIAJAR"
        )
        
        self.cancel_button = Button(
            x + 10,
            y + height - 40,
            width - 20,
            30,
            "❌ Cancelar"
        )
        
        # Fonts
        self.font = pygame.font.Font(None, 18)
        self.title_font = pygame.font.Font(None, 22)
        
        # Scroll
        self.scroll_offset = 0
        
        # Callback
        self.on_travel = None
    
    def set_data(self, grafo, donkey):
        """Establece el grafo y el burro."""
        self.grafo = grafo
        self.donkey = donkey
    
    def show(self, star_id: int, available_galaxies: Dict[str, int]):
        """
        Muestra el panel para un viaje desde una hipergigante.
        
        Args:
            star_id: ID de la hipergigante actual
            available_galaxies: Dict {nombre_galaxia: distancia_en_saltos}
        """
        self.visible = True
        self.current_star_id = star_id
        self.available_galaxies = available_galaxies
        self.selected_galaxy = None
        self.destination_stars = []
        self.selected_destination = None
        self._create_galaxy_buttons()
    
    def hide(self):
        """Oculta el panel."""
        self.visible = False
        self.current_star_id = None
        self.selected_galaxy = None
        self.destination_stars = []
        self.selected_destination = None
    
    def _create_galaxy_buttons(self):
        """Crea botones para seleccionar galaxia."""
        self.galaxy_buttons = []
        y_offset = 0
        
        for i, (galaxy_name, distance) in enumerate(sorted(self.available_galaxies.items())):
            button = Button(
                self.x + 10,
                self.y + 80 + y_offset,
                self.width - 20,
                25,
                f"{galaxy_name} ({distance} saltos)"
            )
            button.data = galaxy_name
            self.galaxy_buttons.append(button)
            y_offset += 30
    
    def _create_star_buttons(self):
        """Crea botones para seleccionar estrella de destino."""
        if not self.grafo or not self.selected_galaxy:
            return
        
        from utils.intergalactic import get_stars_in_constellation
        
        self.destination_stars = get_stars_in_constellation(
            self.grafo,
            self.selected_galaxy
        )
        
        self.star_buttons = []
        y_offset = 0
        
        for star in self.destination_stars:
            icon = "⭐" if star['hipergigante'] else "✨"
            button = Button(
                self.x + 10,
                self.y + 80 + y_offset,
                self.width - 20,
                25,
                f"{icon} {star['label']}"
            )
            button.data = star['id']
            self.star_buttons.append(button)
            y_offset += 30
    
    def handle_click(self, pos):
        """
        Maneja clics en el panel.
        
        Returns:
            'travel' si se confirma el viaje, 'cancel' si se cancela, None si nada
        """
        if not self.visible:
            return None
        
        # Botón de viajar
        if self.travel_button.rect.collidepoint(pos):
            if self.selected_destination is not None:
                return 'travel'
        
        # Botón de cancelar
        if self.cancel_button.rect.collidepoint(pos):
            self.hide()
            return 'cancel'
        
        # Si hay galaxia seleccionada, verificar botón de volver
        if self.selected_galaxy is not None:
            # Área del botón "← Volver a galaxias"
            back_rect = pygame.Rect(self.x + 10, self.y + 50, 200, 20)
            if back_rect.collidepoint(pos):
                self.selected_galaxy = None
                self.selected_destination = None
                self.star_buttons = []
                return None
            
            # Mostrar estrellas de la galaxia seleccionada
            for button in self.star_buttons:
                if button.rect.collidepoint(pos):
                    self.selected_destination = button.data
                    return None
        else:
            # Si no hay galaxia seleccionada, mostrar galaxias
            for button in self.galaxy_buttons:
                if button.rect.collidepoint(pos):
                    self.selected_galaxy = button.data
                    self._create_star_buttons()
                    return None
        
        return None
    
    def draw(self, screen):
        """Dibuja el panel."""
        if not self.visible:
            return
        
        self.panel.draw(screen)
        
        # Título
        if self.selected_galaxy is None:
            title_text = "Selecciona una Galaxia:"
            self.galaxy_buttons and [btn.draw(screen, self.font) for btn in self.galaxy_buttons]
        else:
            title_text = f"Destino en {self.selected_galaxy}:"
            self.star_buttons and [btn.draw(screen, self.font) for btn in self.star_buttons]
            
            # Botón de volver
            back_text = self.font.render("← Volver a galaxias", True, Colors.TEXT_INFO)
            back_rect = back_text.get_rect(topleft=(self.x + 10, self.y + 50))
            screen.blit(back_text, back_rect)
        
        title_surface = self.title_font.render(title_text, True, Colors.TEXT_TITLE)
        screen.blit(title_surface, (self.x + 10, self.y + 25))
        
        # Información
        if self.selected_destination is not None:
            info_text = f"Destino seleccionado: Estrella #{self.selected_destination}"
            info_surface = self.font.render(info_text, True, Colors.TEXT_SUCCESS)
            screen.blit(info_surface, (self.x + 10, self.y + self.height - 120))
            
            # Beneficios
            benefits_y = self.y + self.height - 140
            benefit_font = pygame.font.Font(None, 16)
            benefits = [
                "⚡ +50% energía actual",
                "🌾 x2 pasto en bodega",
                "🚀 Viaje instantáneo (sin edad)"
            ]
            for i, benefit in enumerate(benefits):
                text = benefit_font.render(benefit, True, Colors.TEXT_INFO)
                screen.blit(text, (self.x + 10, benefits_y - (i * 18)))
        
        # Botones de acción
        action_font = pygame.font.Font(None, 18)
        
        # Travel button - solo habilitado si hay destino seleccionado
        if self.selected_destination is not None:
            self.travel_button.draw(screen, action_font)
        
        self.cancel_button.draw(screen, action_font)
