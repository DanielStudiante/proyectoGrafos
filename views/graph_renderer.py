"""
Coordinador de renderizado del grafo de constelaciones.
Responsabilidad: Orquestar la visualización completa del grafo.
"""

import pygame
from views.config import GraphScale
from views.star_visual import StarRenderer, DonkeyRenderer
from views.connection_visual import ConnectionRenderer


class GraphRenderer:
    """
    Renderiza el grafo completo de constelaciones.
    
    Responsabilidades (SRP):
    - Crear y gestionar StarRenderers
    - Coordinar dibujado de conexiones
    - Coordinar dibujado de estrellas
    - Gestionar transformaciones de coordenadas (zoom, pan)
    - Renderizar el burro
    """
    
    def __init__(self, grafo, offset_x=0, offset_y=0):
        self.grafo = grafo
        self.offset_x = offset_x + GraphScale.OFFSET_X
        self.offset_y = offset_y + GraphScale.OFFSET_Y
        
        # Transformaciones de vista (inicializar ANTES de crear renderers)
        self.zoom = 1.0
        self.pan_x = 0
        self.pan_y = 0
        
        # Renderizadores
        self.star_renderers = {}
        self._create_star_renderers()
        
        # Burro
        self.donkey_renderer = DonkeyRenderer()
        
        # Camino activo
        self.active_path = []
    
    def _create_star_renderers(self):
        """Crea un StarRenderer para cada estrella del grafo."""
        for star_id, estrella in self.grafo.estrellas.items():
            screen_x, screen_y = self._world_to_screen(estrella.x, estrella.y)
            self.star_renderers[star_id] = StarRenderer(estrella, screen_x, screen_y)
    
    def _world_to_screen(self, world_x, world_y):
        """Convierte coordenadas del mundo a coordenadas de pantalla."""
        screen_x = int(world_x * GraphScale.SCALE_FACTOR + self.offset_x + self.pan_x)
        screen_y = int(world_y * GraphScale.SCALE_FACTOR + self.offset_y + self.pan_y)
        return screen_x, screen_y
    
    def update(self, mouse_pos, current_star_id=None):
        """
        Actualiza el estado de todos los elementos visuales.
        
        Args:
            mouse_pos: Posición actual del mouse
            current_star_id: ID de la estrella donde está el burro
        """
        # Actualizar burro
        self.donkey_renderer.update()
        
        # Actualizar estrellas
        for star_id, renderer in self.star_renderers.items():
            is_current = (star_id == current_star_id)
            renderer.update(mouse_pos, is_current)
    
    def draw(self, screen, current_star_id=None, visited_stars=None):
        """
        Dibuja el grafo completo.
        
        Args:
            screen: Superficie de pygame donde dibujar
            current_star_id: ID de la estrella actual (donde está el burro)
            visited_stars: Set de IDs de estrellas ya visitadas
        """
        visited_stars = visited_stars or set()
        
        # 1. Conexiones (fondo)
        self._draw_all_connections(screen)
        
        # 2. Camino activo (resaltado)
        if self.active_path:
            self._draw_active_path(screen)
        
        # 3. Estrellas
        for star_id, renderer in self.star_renderers.items():
            is_current = (star_id == current_star_id)
            is_visited = star_id in visited_stars
            renderer.draw(screen, is_current, is_visited)
        
        # 4. Burro (encima de todo)
        if current_star_id is not None:
            current_renderer = self.star_renderers.get(current_star_id)
            if current_renderer:
                self.donkey_renderer.draw(screen, current_renderer)
    
    def _draw_all_connections(self, screen):
        """Dibuja todas las conexiones del grafo."""
        drawn_connections = set()
        
        for star_id, vertex in self.grafo.graph.items():
            star1_renderer = self.star_renderers.get(star_id)
            if not star1_renderer:
                continue
            
            for neighbor_vertex, distance in vertex.get_connections().items():
                neighbor_id = neighbor_vertex.id
                
                # Evitar duplicados
                connection_key = tuple(sorted([star_id, neighbor_id]))
                if connection_key in drawn_connections:
                    continue
                drawn_connections.add(connection_key)
                
                star2_renderer = self.star_renderers.get(neighbor_id)
                if not star2_renderer:
                    continue
                
                ConnectionRenderer.draw_connection(
                    screen,
                    star1_renderer,
                    star2_renderer,
                    distance,
                    is_path=False,
                    show_weights=True
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
                    star1_renderer,
                    star2_renderer,
                    distance,
                    is_path=True,
                    show_weights=True
                )
    
    def set_active_path(self, path):
        """
        Establece el camino activo a destacar visualmente.
        
        Args:
            path: Lista de IDs de estrellas que forman el camino
        """
        self.active_path = path or []
    
    def get_star_at_position(self, pos):
        """
        Obtiene la estrella en una posición de pantalla.
        
        Args:
            pos: Tupla (x, y) con la posición en pantalla
            
        Returns:
            ID de la estrella o None si no hay ninguna
        """
        for star_id, renderer in self.star_renderers.items():
            if renderer.contains_point(pos):
                return star_id
        return None
    
    def get_reachable_stars(self, from_star_id, max_energy):
        """
        Obtiene las estrellas alcanzables desde una posición con energía máxima.
        
        Args:
            from_star_id: ID de la estrella de origen
            max_energy: Energía máxima disponible
            
        Returns:
            Lista de IDs de estrellas alcanzables
        """
        from algorithms.dijkstra import obtener_estrellas_alcanzables
        return obtener_estrellas_alcanzables(self.grafo, from_star_id, max_energy)
