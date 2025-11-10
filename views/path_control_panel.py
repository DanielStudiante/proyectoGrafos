"""
Panel de control de caminos bloqueados.

REQUERIMIENTO 0.5: Permite a los científicos bloquear/habilitar caminos
debido al paso de cometas y meteoritos.
"""

import pygame
from typing import Optional, Tuple
from backend.constellation import GrafoConstelaciones


class PathControlPanel:
    """
    Panel para controlar el bloqueo/habilitación de caminos.
    
    REQUERIMIENTO 0.5: Los científicos pueden bloquear caminos en cualquier
    momento debido a cometas y meteoritos.
    """
    
    def __init__(self, x: int, y: int, width: int, height: int, grafo: GrafoConstelaciones):
        """
        Inicializa el panel de control de caminos.
        
        Args:
            x, y: Posición del panel
            width, height: Dimensiones del panel
            grafo: Grafo de constelaciones
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.grafo = grafo
        self.visible = False
        self.selected_path = None  # (from_id, to_id)
        self.scroll_offset = 0
        self.max_scroll = 0
        
        # Colores
        self.bg_color = (40, 40, 50, 230)
        self.title_color = (255, 255, 255)
        self.blocked_color = (255, 80, 80)
        self.active_color = (80, 255, 80)
        self.hover_color = (100, 100, 150)
        self.text_color = (230, 230, 230)
        
        # Fuentes
        self.title_font = pygame.font.Font(None, 28)
        self.subtitle_font = pygame.font.Font(None, 22)
        self.text_font = pygame.font.Font(None, 20)
        self.small_font = pygame.font.Font(None, 18)
        
        # Botones
        self.close_button_rect = pygame.Rect(x + width - 35, y + 5, 30, 30)
        self.toggle_all_button = pygame.Rect(x + 10, y + height - 45, width - 20, 35)
        
    def toggle_visibility(self):
        """Alterna la visibilidad del panel."""
        self.visible = not self.visible
        self.scroll_offset = 0
        
    def show(self):
        """Muestra el panel."""
        self.visible = True
        
    def hide(self):
        """Oculta el panel."""
        self.visible = False
        
    def get_all_paths(self) -> list:
        """
        Obtiene todos los caminos del grafo con su estado.
        
        Returns:
            Lista de tuplas (from_id, to_id, from_label, to_label, blocked, distance)
        """
        paths = []
        for vertex_id, vertex in self.grafo.graph.items():
            estrella_from = self.grafo.obtener_estrella(vertex_id)
            
            for neighbor_vertex, distance in vertex.get_all_connections().items():
                neighbor_id = neighbor_vertex.id
                estrella_to = self.grafo.obtener_estrella(neighbor_id)
                
                blocked = vertex.is_edge_blocked(neighbor_id)
                
                paths.append((
                    vertex_id,
                    neighbor_id,
                    estrella_from.label if estrella_from else f"ID:{vertex_id}",
                    estrella_to.label if estrella_to else f"ID:{neighbor_id}",
                    blocked,
                    distance
                ))
        
        return sorted(paths, key=lambda x: (x[0], x[1]))
    
    def toggle_path(self, from_id: int, to_id: int):
        """
        Alterna el estado de bloqueo de un camino.
        
        Args:
            from_id: ID de la estrella origen
            to_id: ID de la estrella destino
        """
        if self.grafo.esta_camino_bloqueado(from_id, to_id):
            self.grafo.habilitar_camino(from_id, to_id)
            print(f"🟢 CAMINO HABILITADO: {from_id} → {to_id}")
        else:
            self.grafo.bloquear_camino(from_id, to_id)
            print(f"🔴 CAMINO BLOQUEADO: {from_id} → {to_id}")
    
    def block_all_paths(self):
        """Bloquea todos los caminos."""
        for vertex_id, vertex in self.grafo.graph.items():
            for neighbor_vertex in vertex.get_all_connections().keys():
                vertex.block_edge(neighbor_vertex.id)
        print("🔴 TODOS LOS CAMINOS BLOQUEADOS")
    
    def unblock_all_paths(self):
        """Habilita todos los caminos."""
        for vertex_id, vertex in self.grafo.graph.items():
            vertex.blocked_edges.clear()
        print("🟢 TODOS LOS CAMINOS HABILITADOS")
    
    def handle_event(self, event) -> bool:
        """
        Maneja eventos del panel.
        
        Args:
            event: Evento de pygame
            
        Returns:
            True si el evento fue manejado, False si no
        """
        if not self.visible:
            return False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            
            # Botón cerrar
            if self.close_button_rect.collidepoint(mouse_pos):
                self.hide()
                return True
            
            # Botón toggle all
            if self.toggle_all_button.collidepoint(mouse_pos):
                # Verificar si hay algún camino bloqueado
                bloqueados = self.grafo.obtener_caminos_bloqueados()
                if bloqueados:
                    self.unblock_all_paths()
                else:
                    self.block_all_paths()
                return True
            
            # Click en lista de caminos
            paths = self.get_all_paths()
            y_start = self.rect.y + 70
            item_height = 50
            
            for i, path in enumerate(paths):
                item_y = y_start + i * item_height - self.scroll_offset
                
                if item_y < self.rect.y + 70:
                    continue
                if item_y > self.rect.bottom - 100:
                    break
                
                item_rect = pygame.Rect(
                    self.rect.x + 10,
                    item_y,
                    self.rect.width - 20,
                    item_height - 5
                )
                
                if item_rect.collidepoint(mouse_pos):
                    from_id, to_id = path[0], path[1]
                    self.toggle_path(from_id, to_id)
                    return True
        
        elif event.type == pygame.MOUSEWHEEL:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.scroll_offset -= event.y * 20
                self.scroll_offset = max(0, min(self.scroll_offset, self.max_scroll))
                return True
        
        return False
    
    def draw(self, screen: pygame.Surface):
        """
        Dibuja el panel en la pantalla.
        
        Args:
            screen: Superficie de pygame donde dibujar
        """
        if not self.visible:
            return
        
        # Crear superficie con transparencia
        panel_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        panel_surface.fill(self.bg_color)
        
        # Borde
        pygame.draw.rect(panel_surface, (100, 100, 150), 
                        (0, 0, self.rect.width, self.rect.height), 3)
        
        # Título
        title = self.title_font.render("🛡️ CONTROL DE CAMINOS", True, self.title_color)
        panel_surface.blit(title, (10, 10))
        
        # Subtítulo
        subtitle = self.small_font.render("Bloquear/Habilitar caminos (Req. 0.5)", True, (200, 200, 200))
        panel_surface.blit(subtitle, (10, 40))
        
        # Botón cerrar
        pygame.draw.circle(panel_surface, (200, 50, 50),
                          (self.close_button_rect.centerx - self.rect.x,
                           self.close_button_rect.centery - self.rect.y), 12)
        close_text = self.text_font.render("✕", True, (255, 255, 255))
        panel_surface.blit(close_text, 
                          (self.close_button_rect.x - self.rect.x + 7,
                           self.close_button_rect.y - self.rect.y + 5))
        
        # Lista de caminos
        paths = self.get_all_paths()
        y_offset = 70
        item_height = 50
        
        # Calcular scroll máximo
        total_height = len(paths) * item_height
        visible_height = self.rect.height - 160
        self.max_scroll = max(0, total_height - visible_height)
        
        # Dibujar caminos
        mouse_pos = pygame.mouse.get_pos()
        
        for i, (from_id, to_id, from_label, to_label, blocked, distance) in enumerate(paths):
            item_y = y_offset + i * item_height - self.scroll_offset
            
            # Culling: solo dibujar items visibles
            if item_y < 70 or item_y > self.rect.height - 100:
                continue
            
            # Fondo del item
            item_rect = pygame.Rect(10, item_y, self.rect.width - 20, item_height - 5)
            
            # Detectar hover
            absolute_rect = pygame.Rect(
                self.rect.x + item_rect.x,
                self.rect.y + item_rect.y,
                item_rect.width,
                item_rect.height
            )
            
            is_hover = absolute_rect.collidepoint(mouse_pos)
            
            # Color de fondo según estado
            if is_hover:
                bg = self.hover_color
            elif blocked:
                bg = (80, 40, 40, 200)
            else:
                bg = (40, 80, 40, 200)
            
            pygame.draw.rect(panel_surface, bg, item_rect, border_radius=5)
            pygame.draw.rect(panel_surface, (100, 100, 100), item_rect, 2, border_radius=5)
            
            # Estado (bloqueado/habilitado)
            status_color = self.blocked_color if blocked else self.active_color
            status_text = "🔴 BLOQUEADO" if blocked else "🟢 HABILITADO"
            status_surface = self.small_font.render(status_text, True, status_color)
            panel_surface.blit(status_surface, (item_rect.x + 10, item_y + 5))
            
            # Camino
            path_text = f"{from_label} → {to_label}"
            path_surface = self.text_font.render(path_text, True, self.text_color)
            panel_surface.blit(path_surface, (item_rect.x + 10, item_y + 25))
            
            # Distancia
            dist_text = f"{distance:.0f} ly"
            dist_surface = self.small_font.render(dist_text, True, (180, 180, 180))
            panel_surface.blit(dist_surface, 
                             (item_rect.right - 60, item_y + 28))
        
        # Botón toggle all
        bloqueados = self.grafo.obtener_caminos_bloqueados()
        toggle_text = "🟢 HABILITAR TODOS" if bloqueados else "🔴 BLOQUEAR TODOS"
        toggle_color = self.active_color if bloqueados else self.blocked_color
        
        toggle_button_local = pygame.Rect(
            self.toggle_all_button.x - self.rect.x,
            self.toggle_all_button.y - self.rect.y,
            self.toggle_all_button.width,
            self.toggle_all_button.height
        )
        
        pygame.draw.rect(panel_surface, toggle_color, toggle_button_local, border_radius=5)
        pygame.draw.rect(panel_surface, (200, 200, 200), toggle_button_local, 2, border_radius=5)
        
        toggle_surface = self.subtitle_font.render(toggle_text, True, (255, 255, 255))
        text_rect = toggle_surface.get_rect(center=toggle_button_local.center)
        panel_surface.blit(toggle_surface, text_rect)
        
        # Contador
        total_paths = len(paths)
        blocked_count = len(bloqueados)
        counter_text = f"Bloqueados: {blocked_count}/{total_paths}"
        counter_surface = self.small_font.render(counter_text, True, (200, 200, 200))
        panel_surface.blit(counter_surface, (10, self.rect.height - 80))
        
        # Dibujar en la pantalla
        screen.blit(panel_surface, self.rect.topleft)
