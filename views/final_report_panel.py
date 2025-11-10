"""
Panel de reporte final del viaje (REQUERIMIENTO 0.5).

Muestra estadísticas completas del viaje:
- Estrellas visitadas
- Galaxias (constelaciones) visitadas
- Consumo de pasto por estrella
- Tiempo invertido en investigaciones
"""

import pygame
from typing import Optional
from backend.constellation import GrafoConstelaciones
from backend.simulator import SimuladorViaje


class FinalReportPanel:
    """
    Panel de reporte final del viaje.
    
    REQUERIMIENTO 0.5: Mostrar al equipo científico un reporte completo
    de todas las estrellas visitadas, galaxias, consumo de alimento y tiempo.
    """
    
    def __init__(self, x: int, y: int, width: int, height: int):
        """
        Inicializa el panel de reporte.
        
        Args:
            x, y: Posición del panel
            width, height: Dimensiones del panel
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.visible = False
        self.simulador = None
        self.scroll_offset = 0
        self.max_scroll = 0
        
        # Colores
        self.bg_color = (25, 25, 35, 240)
        self.title_color = (255, 220, 100)
        self.subtitle_color = (100, 200, 255)
        self.text_color = (230, 230, 230)
        self.success_color = (100, 255, 100)
        self.warning_color = (255, 200, 100)
        
        # Fuentes
        self.title_font = pygame.font.Font(None, 36)
        self.subtitle_font = pygame.font.Font(None, 26)
        self.text_font = pygame.font.Font(None, 22)
        self.small_font = pygame.font.Font(None, 18)
        
        # Botones
        self.close_button_rect = pygame.Rect(x + width - 45, y + 10, 35, 35)
        
    def show(self, simulador: SimuladorViaje):
        """
        Muestra el panel con los datos del simulador.
        
        Args:
            simulador: Instancia del SimuladorViaje con el historial
        """
        self.simulador = simulador
        self.visible = True
        self.scroll_offset = 0
        
    def hide(self):
        """Oculta el panel."""
        self.visible = False
        
    def handle_event(self, event) -> bool:
        """
        Maneja eventos del panel.
        
        Args:
            event: Evento de pygame
            
        Returns:
            True si el evento fue manejado
        """
        if not self.visible:
            return False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            
            # Botón cerrar
            if self.close_button_rect.collidepoint(mouse_pos):
                self.hide()
                return True
        
        elif event.type == pygame.MOUSEWHEEL:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.scroll_offset -= event.y * 30
                self.scroll_offset = max(0, min(self.scroll_offset, self.max_scroll))
                return True
        
        return False
    
    def draw(self, screen: pygame.Surface):
        """
        Dibuja el panel en la pantalla.
        
        Args:
            screen: Superficie de pygame donde dibujar
        """
        if not self.visible or not self.simulador:
            return
        
        # Crear superficie con transparencia
        panel_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        panel_surface.fill(self.bg_color)
        
        # Borde dorado
        pygame.draw.rect(panel_surface, self.title_color, 
                        (0, 0, self.rect.width, self.rect.height), 4)
        
        # Título principal
        title = self.title_font.render("📊 REPORTE FINAL DEL VIAJE", True, self.title_color)
        panel_surface.blit(title, (20, 15))
        
        # Botón cerrar
        pygame.draw.circle(panel_surface, (200, 50, 50),
                          (self.close_button_rect.centerx - self.rect.x,
                           self.close_button_rect.centery - self.rect.y), 15)
        close_text = self.text_font.render("✕", True, (255, 255, 255))
        panel_surface.blit(close_text, 
                          (self.close_button_rect.x - self.rect.x + 9,
                           self.close_button_rect.y - self.rect.y + 7))
        
        # Contenido scrolleable
        content_y = 70
        
        # 1. Resumen general
        content_y = self._draw_general_summary(panel_surface, content_y)
        
        # 2. Estrellas visitadas
        content_y = self._draw_visited_stars(panel_surface, content_y)
        
        # 3. Constelaciones visitadas
        content_y = self._draw_visited_constellations(panel_surface, content_y)
        
        # 4. Consumo de pasto
        content_y = self._draw_grass_consumption(panel_surface, content_y)
        
        # 5. Tiempo de investigación
        content_y = self._draw_investigation_time(panel_surface, content_y)
        
        # 6. Estado final del burro
        content_y = self._draw_final_status(panel_surface, content_y)
        
        # Calcular scroll máximo
        self.max_scroll = max(0, content_y - self.rect.height + 50)
        
        # Dibujar en la pantalla
        screen.blit(panel_surface, self.rect.topleft)
    
    def _draw_general_summary(self, surface, y_start):
        """Dibuja el resumen general."""
        y = y_start - self.scroll_offset
        
        if y < 60 or y > self.rect.height - 50:
            return y_start + 150
        
        # Título sección
        subtitle = self.subtitle_font.render("🎯 RESUMEN GENERAL", True, self.subtitle_color)
        surface.blit(subtitle, (20, y))
        y += 40
        
        # Datos generales
        datos = [
            f"⭐ Estrellas visitadas: {len(self.simulador.historial_viaje)}",
            f"🌌 Constelaciones visitadas: {len(self.simulador.constelaciones_visitadas)}",
            f"📏 Distancia total recorrida: {self.simulador.distancia_total:.1f} años luz",
            f"⚡ Energía final: {self.simulador.donkey.donkey_energy:.1f}%",
            f"🌾 Pasto restante: {self.simulador.donkey.grass_in_basement:.0f} kg",
            f"🎂 Edad final: {self.simulador.donkey.age:.1f} años luz",
        ]
        
        for dato in datos:
            text = self.text_font.render(dato, True, self.text_color)
            surface.blit(text, (40, y))
            y += 30
        
        return y_start + 150
    
    def _draw_visited_stars(self, surface, y_start):
        """Dibuja la lista de estrellas visitadas."""
        y = y_start - self.scroll_offset
        
        subtitle = self.subtitle_font.render("⭐ ESTRELLAS VISITADAS", True, self.subtitle_color)
        if 60 < y < self.rect.height - 50:
            surface.blit(subtitle, (20, y))
        y += 40
        
        for i, star_id in enumerate(self.simulador.historial_viaje, 1):
            if y < 60 or y > self.rect.height - 50:
                y += 25
                continue
            
            estrella = self.simulador.grafo.obtener_estrella(star_id)
            if estrella:
                # Nombre de la estrella
                text = f"{i}. {estrella.label} (ID: {star_id})"
                star_text = self.text_font.render(text, True, self.text_color)
                surface.blit(star_text, (40, y))
                
                # Constelaciones
                const_text = f"   Galaxias: {', '.join(estrella.constelaciones)}"
                const_surface = self.small_font.render(const_text, True, (180, 180, 180))
                surface.blit(const_surface, (60, y + 20))
                
                y += 50
        
        return y_start + 40 + len(self.simulador.historial_viaje) * 50
    
    def _draw_visited_constellations(self, surface, y_start):
        """Dibuja las constelaciones visitadas."""
        y = y_start - self.scroll_offset
        
        subtitle = self.subtitle_font.render("🌌 GALAXIAS VISITADAS", True, self.subtitle_color)
        if 60 < y < self.rect.height - 50:
            surface.blit(subtitle, (20, y))
        y += 40
        
        for i, const_name in enumerate(sorted(self.simulador.constelaciones_visitadas), 1):
            if y < 60 or y > self.rect.height - 50:
                y += 30
                continue
            
            text = f"{i}. {const_name}"
            const_text = self.text_font.render(text, True, self.text_color)
            surface.blit(const_text, (40, y))
            y += 30
        
        return y_start + 40 + len(self.simulador.constelaciones_visitadas) * 30
    
    def _draw_grass_consumption(self, surface, y_start):
        """Dibuja el consumo de pasto por estrella."""
        y = y_start - self.scroll_offset
        
        subtitle = self.subtitle_font.render("🌾 CONSUMO DE PASTO", True, self.subtitle_color)
        if 60 < y < self.rect.height - 50:
            surface.blit(subtitle, (20, y))
        y += 40
        
        total_pasto = sum(self.simulador.pasto_consumido_por_estrella.values())
        
        if total_pasto > 0:
            for star_id, kg_consumidos in self.simulador.pasto_consumido_por_estrella.items():
                if y < 60 or y > self.rect.height - 50:
                    y += 30
                    continue
                
                estrella = self.simulador.grafo.obtener_estrella(star_id)
                if estrella:
                    text = f"  {estrella.label}: {kg_consumidos:.0f} kg"
                    grass_text = self.text_font.render(text, True, self.text_color)
                    surface.blit(grass_text, (40, y))
                    y += 30
            
            # Total
            if 60 < y < self.rect.height - 50:
                total_text = f"  TOTAL: {total_pasto:.0f} kg"
                total_surface = self.text_font.render(total_text, True, self.success_color)
                surface.blit(total_surface, (40, y))
            y += 40
        else:
            if 60 < y < self.rect.height - 50:
                no_grass_text = self.text_font.render("  No se consumió pasto", True, (150, 150, 150))
                surface.blit(no_grass_text, (40, y))
            y += 40
        
        return y_start + 80 + len(self.simulador.pasto_consumido_por_estrella) * 30
    
    def _draw_investigation_time(self, surface, y_start):
        """Dibuja el tiempo de investigación por estrella."""
        y = y_start - self.scroll_offset
        
        subtitle = self.subtitle_font.render("🔬 TIEMPO DE INVESTIGACIÓN", True, self.subtitle_color)
        if 60 < y < self.rect.height - 50:
            surface.blit(subtitle, (20, y))
        y += 40
        
        total_tiempo = sum(self.simulador.tiempo_investigacion_por_estrella.values())
        
        if total_tiempo > 0:
            for star_id, horas in self.simulador.tiempo_investigacion_por_estrella.items():
                if y < 60 or y > self.rect.height - 50:
                    y += 30
                    continue
                
                estrella = self.simulador.grafo.obtener_estrella(star_id)
                if estrella:
                    text = f"  {estrella.label}: {horas:.1f} horas"
                    time_text = self.text_font.render(text, True, self.text_color)
                    surface.blit(time_text, (40, y))
                    y += 30
            
            # Total
            if 60 < y < self.rect.height - 50:
                total_text = f"  TOTAL: {total_tiempo:.1f} horas"
                total_surface = self.text_font.render(total_text, True, self.success_color)
                surface.blit(total_surface, (40, y))
            y += 40
        else:
            if 60 < y < self.rect.height - 50:
                no_time_text = self.text_font.render("  No se realizaron investigaciones", True, (150, 150, 150))
                surface.blit(no_time_text, (40, y))
            y += 40
        
        return y_start + 80 + len(self.simulador.tiempo_investigacion_por_estrella) * 30
    
    def _draw_final_status(self, surface, y_start):
        """Dibuja el estado final del burro."""
        y = y_start - self.scroll_offset
        
        if y < 60 or y > self.rect.height - 100:
            return y_start + 150
        
        subtitle = self.subtitle_font.render("🐴 ESTADO FINAL DEL BURRO", True, self.subtitle_color)
        surface.blit(subtitle, (20, y))
        y += 40
        
        # Estado de salud
        health_color = self.success_color if self.simulador.donkey.health in ["Excelente", "Buena"] else self.warning_color
        health_text = f"💚 Salud: {self.simulador.donkey.health}"
        health_surface = self.text_font.render(health_text, True, health_color)
        surface.blit(health_surface, (40, y))
        y += 30
        
        # Estado de vida
        alive_text = "✅ VIVO" if self.simulador.donkey.alive else "💀 MUERTO"
        alive_color = self.success_color if self.simulador.donkey.alive else (255, 50, 50)
        alive_surface = self.text_font.render(alive_text, True, alive_color)
        surface.blit(alive_surface, (40, y))
        y += 40
        
        # Mensaje de cierre
        closing_text = "¡Misión completada! Gracias por explorar el universo."
        closing_surface = self.small_font.render(closing_text, True, self.title_color)
        closing_rect = closing_surface.get_rect(center=(self.rect.width // 2, y + 20))
        surface.blit(closing_surface, closing_rect)
        
        return y_start + 150
