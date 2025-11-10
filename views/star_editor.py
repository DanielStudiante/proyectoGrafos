"""
Panel de editor de estrellas para ajustar propiedades en tiempo real
"""
import pygame
from views.config import Colors, PanelSizes
from views.components import Panel, Button


class SimpleLabel:
    """Etiqueta de texto simple."""
    
    def __init__(self, x, y, text, font_size=18, color=None):
        self.x = x
        self.y = y
        self.text = text
        self.font_size = font_size
        self.color = color or Colors.TEXT_PRIMARY
        self.font = pygame.font.Font(None, font_size)
    
    def update(self, text):
        """Actualiza el texto."""
        self.text = text
    
    def draw(self, screen):
        """Dibuja la etiqueta."""
        text_surface = self.font.render(str(self.text), True, self.color)
        screen.blit(text_surface, (self.x, self.y))


class StarEditorPanel:
    """Panel para editar propiedades de estrellas."""
    
    def __init__(self, x, y, width, height):
        self.panel = Panel(x, y, width, height, "⚙️ Editor de Estrella")
        self.visible = False
        self.current_star = None
        self.grafo = None
        
        # Botones de incremento/decremento
        button_width = 30
        button_height = 25
        spacing = 5
        start_y = 50
        
        # Energía (amountOfEnergy)
        self.energy_label = SimpleLabel(x + 10, y + start_y, "Pasto: 0 kg", font_size=18)
        self.energy_minus = Button(x + width - 90, y + start_y, button_width, button_height, "-")
        self.energy_plus = Button(x + width - 50, y + start_y, button_width, button_height, "+")
        
        # Tiempo para comer (timeToEat)
        self.time_label = SimpleLabel(x + 10, y + start_y + 35, "Tiempo/kg: 0h", font_size=18)
        self.time_minus = Button(x + width - 90, y + start_y + 35, button_width, button_height, "-")
        self.time_plus = Button(x + width - 50, y + start_y + 35, button_width, button_height, "+")
        
        # Tiempo de estadía (stayDuration)
        self.stay_label = SimpleLabel(x + 10, y + start_y + 70, "Estadía: 0h", font_size=18)
        self.stay_minus = Button(x + width - 90, y + start_y + 70, button_width, button_height, "-")
        self.stay_plus = Button(x + width - 50, y + start_y + 70, button_width, button_height, "+")
        
        # Impacto en salud (healthImpact)
        self.health_label = SimpleLabel(x + 10, y + start_y + 105, "Energía: 0", font_size=18)
        self.health_minus = Button(x + width - 90, y + start_y + 105, button_width, button_height, "-")
        self.health_plus = Button(x + width - 50, y + start_y + 105, button_width, button_height, "+")
        
        # Impacto en vida (lifeTimeImpact)
        self.life_label = SimpleLabel(x + 10, y + start_y + 140, "Vida: 0 años", font_size=18)
        self.life_minus = Button(x + width - 90, y + start_y + 140, button_width, button_height, "-")
        self.life_plus = Button(x + width - 50, y + start_y + 140, button_width, button_height, "+")
        
        # Botones de acción
        self.save_button = Button(x + 10, y + height - 40, width - 110, 30, "💾 Guardar en JSON")
        self.close_button = Button(x + width - 90, y + height - 40, 80, 30, "❌ Cerrar")
        
        # Nombre de estrella
        self.star_name_label = SimpleLabel(x + 10, y + 20, "Selecciona una estrella", font_size=20)
    
    def set_grafo(self, grafo):
        """Establece el grafo para editar."""
        self.grafo = grafo
    
    def show(self, star_id):
        """Muestra el editor para una estrella específica."""
        if not self.grafo:
            return
        
        self.current_star = self.grafo.obtener_estrella(star_id)
        if self.current_star:
            self.visible = True
            self._update_labels()
    
    def hide(self):
        """Oculta el editor."""
        self.visible = False
        self.current_star = None
    
    def _update_labels(self):
        """Actualiza las etiquetas con los valores actuales."""
        if not self.current_star:
            return
        
        self.star_name_label.update(f"⭐ {self.current_star.label}")
        self.energy_label.update(f"Pasto: {int(self.current_star.amount_of_energy)} kg")
        self.time_label.update(f"Tiempo/kg: {self.current_star.time_to_eat:.1f}h")
        self.stay_label.update(f"Estadía: {self.current_star.stay_duration:.1f}h")
        
        health = self.current_star.health_impact
        health_str = f"+{health:.1f}" if health >= 0 else f"{health:.1f}"
        self.health_label.update(f"Energía: {health_str}")
        
        life = self.current_star.life_time_impact
        life_str = f"+{life:.1f}" if life >= 0 else f"{life:.1f}"
        self.life_label.update(f"Vida: {life_str} años")
    
    def handle_click(self, pos):
        """Maneja clics en los botones."""
        if not self.visible or not self.current_star:
            return None
        
        # Energía
        if self.energy_minus.rect.collidepoint(pos):
            self.current_star.amount_of_energy = max(0, self.current_star.amount_of_energy - 1)
            self._update_labels()
        elif self.energy_plus.rect.collidepoint(pos):
            self.current_star.amount_of_energy = min(10, self.current_star.amount_of_energy + 1)
            self._update_labels()
        
        # Tiempo para comer
        elif self.time_minus.rect.collidepoint(pos):
            self.current_star.time_to_eat = max(0.5, self.current_star.time_to_eat - 0.5)
            self._update_labels()
        elif self.time_plus.rect.collidepoint(pos):
            self.current_star.time_to_eat = min(10, self.current_star.time_to_eat + 0.5)
            self._update_labels()
        
        # Tiempo de estadía
        elif self.stay_minus.rect.collidepoint(pos):
            self.current_star.stay_duration = max(1, self.current_star.stay_duration - 1)
            self._update_labels()
        elif self.stay_plus.rect.collidepoint(pos):
            self.current_star.stay_duration = min(20, self.current_star.stay_duration + 1)
            self._update_labels()
        
        # Impacto en salud
        elif self.health_minus.rect.collidepoint(pos):
            self.current_star.health_impact -= 0.5
            self._update_labels()
        elif self.health_plus.rect.collidepoint(pos):
            self.current_star.health_impact += 0.5
            self._update_labels()
        
        # Impacto en vida
        elif self.life_minus.rect.collidepoint(pos):
            self.current_star.life_time_impact -= 1
            self._update_labels()
        elif self.life_plus.rect.collidepoint(pos):
            self.current_star.life_time_impact += 1
            self._update_labels()
        
        # Guardar
        elif self.save_button.rect.collidepoint(pos):
            return "save"
        
        # Cerrar
        elif self.close_button.rect.collidepoint(pos):
            self.hide()
            return "close"
        
        return None
    
    def draw(self, screen):
        """Dibuja el panel del editor."""
        if not self.visible:
            return
        
        # Crear una fuente para los botones
        button_font = pygame.font.Font(None, 20)
        
        self.panel.draw(screen)
        
        # Labels
        self.star_name_label.draw(screen)
        self.energy_label.draw(screen)
        self.time_label.draw(screen)
        self.stay_label.draw(screen)
        self.health_label.draw(screen)
        self.life_label.draw(screen)
        
        # Botones de incremento
        self.energy_minus.draw(screen, button_font)
        self.energy_plus.draw(screen, button_font)
        self.time_minus.draw(screen, button_font)
        self.time_plus.draw(screen, button_font)
        self.stay_minus.draw(screen, button_font)
        self.stay_plus.draw(screen, button_font)
        self.health_minus.draw(screen, button_font)
        self.health_plus.draw(screen, button_font)
        self.life_minus.draw(screen, button_font)
        self.life_plus.draw(screen, button_font)
        
        # Botones de acción
        action_font = pygame.font.Font(None, 18)
        self.save_button.draw(screen, action_font)
        self.close_button.draw(screen, action_font)
