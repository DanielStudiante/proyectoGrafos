"""
Manejo de eventos del juego.
Responsabilidad: Procesar y responder a eventos de usuario (mouse, teclado).
"""

import pygame
from views.config import Colors, Icons, GameState
from algorithms.dijkstra import encontrar_camino_mas_corto
from utils.config_saver import save_grafo_to_json


class GameEventHandler:
    """
    Maneja todos los eventos del juego.
    
    Responsabilidades (SRP):
    - Procesar eventos de Pygame (teclado, mouse)
    - Delegar acciones a callbacks del GameManager
    - Gestionar interacciones UI (clicks en paneles, estrellas)
    """
    
    def __init__(self, game_manager):
        """
        Args:
            game_manager: Instancia del GameManager
        """
        self.gm = game_manager
        self.mouse_pressed_last_frame = False
    
    def handle_events(self):
        """Procesa todos los eventos de la cola de Pygame."""
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]
        
        for event in pygame.event.get():
            self._handle_single_event(event, mouse_pos)
        
        # Actualizar paneles con estado del mouse
        self._update_panels_state(mouse_pos, mouse_pressed)
        
        self.mouse_pressed_last_frame = mouse_pressed
    
    def _handle_single_event(self, event, mouse_pos):
        """Procesa un evento individual."""
        if event.type == pygame.QUIT:
            self.gm.running = False
        
        elif event.type == pygame.KEYDOWN:
            self._handle_keyboard(event)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self._handle_mouse_button(event, mouse_pos)
    
    def _handle_keyboard(self, event):
        """Maneja eventos de teclado."""
        if event.key == pygame.K_ESCAPE:
            self.gm.running = False
        elif event.key == pygame.K_SPACE:
            self._on_eat_click()
        elif event.key == pygame.K_i:
            self._on_investigate_click()
    
    def _handle_mouse_button(self, event, mouse_pos):
        """Maneja clicks del mouse."""
        if event.button == 1:  # Click izquierdo
            self._handle_left_click(mouse_pos)
        elif event.button == 3:  # Click derecho
            self._handle_right_click(mouse_pos)
    
    def _handle_left_click(self, mouse_pos):
        """Maneja click izquierdo."""
        # Prioridad al panel inter-galáctico si está visible
        if self.gm.intergalactic_panel.visible:
            result = self.gm.intergalactic_panel.handle_click(mouse_pos)
            
            if result == "travel":
                self._execute_intergalactic_travel()
            elif result == "cancel":
                pass  # Ya se cierra automáticamente
        # Prioridad al editor si está visible
        elif self.gm.star_editor.visible:
            result = self.gm.star_editor.handle_click(mouse_pos)
            
            if result == "save":
                self._save_config()
            elif result == "close":
                self.gm._update_ui()
        # Verificar si se hace clic en el panel de información de estrella
        elif self.gm.star_info_panel.visible:
            if self.gm.star_info_panel.handle_click(mouse_pos):
                # Se cerró el panel, no hacer nada más
                return
            # Si no se cerró, permitir seleccionar otra estrella
            star_id = self.gm.graph_renderer.get_star_at_position(mouse_pos)
            if star_id:
                self.gm.selected_star_id = star_id
                self.gm._update_star_selection()
        else:
            # Click en una estrella
            star_id = self.gm.graph_renderer.get_star_at_position(mouse_pos)
            if star_id:
                self.gm.selected_star_id = star_id
                self.gm._update_star_selection()
    
    def _handle_right_click(self, mouse_pos):
        """Maneja click derecho (abrir editor de estrella)."""
        star_id = self.gm.graph_renderer.get_star_at_position(mouse_pos)
        if star_id:
            self.gm.star_editor.show(star_id)
    
    def _update_panels_state(self, mouse_pos, mouse_pressed):
        """Actualiza el estado de los paneles con el mouse."""
        # Verificar si estamos en una hipergigante
        current_star = self.gm.grafo.obtener_estrella(self.gm.simulador.posicion_actual)
        is_hypergiant = current_star.hipergigante if current_star else False
        
        self.gm.actions_panel.update(
            mouse_pos,
            mouse_pressed and not self.mouse_pressed_last_frame,
            can_travel=(self.gm.selected_star_id is not None and 
                       self.gm.selected_star_id != self.gm.simulador.posicion_actual),
            has_grass=(self.gm.burro.grass_in_basement > 0),
            is_on_hypergiant=is_hypergiant
        )
    
    def _save_config(self):
        """Guarda la configuración al JSON."""
        try:
            save_grafo_to_json(self.gm.grafo)
            self.gm.notification.show(
                "✅ Configuración guardada en config.json",
                Colors.HEALTH_POSITIVE
            )
        except Exception as e:
            self.gm.notification.show(
                f"❌ Error al guardar: {e}",
                Colors.HEALTH_NEGATIVE
            )
    
    # ==================== CALLBACKS DE ACCIONES ====================
    
    def _on_travel_click(self):
        """Callback: Viajar a estrella seleccionada."""
        if not self.gm.selected_star_id or \
           self.gm.selected_star_id == self.gm.simulador.posicion_actual:
            return
        
        # Calcular ruta
        resultado = encontrar_camino_mas_corto(
            self.gm.grafo,
            self.gm.simulador.posicion_actual,
            self.gm.selected_star_id
        )
        
        # Debug
        self._debug_travel(resultado)
        
        if not resultado or not resultado['existe']:
            self.gm.notification.add(
                f"{Icons.DANGER} No hay ruta disponible",
                Colors.TEXT_DANGER
            )
            return
        
        # Verificar energía
        if resultado['distancia'] > self.gm.burro.donkey_energy:
            self.gm.notification.add(
                f"{Icons.DANGER} Energía insuficiente: "
                f"{self.gm.burro.donkey_energy:.1f}/{resultado['distancia']:.1f}",
                Colors.TEXT_DANGER
            )
            return
        
        # Realizar viaje
        exito = self.gm.simulador.viajar_a(self.gm.selected_star_id, verbose=False)
        
        if exito:
            star = self.gm.grafo.obtener_estrella(self.gm.selected_star_id)
            self.gm.notification.add(
                f"{Icons.SUCCESS} Viaje exitoso a {star.label}",
                Colors.TEXT_SUCCESS
            )
            self.gm._update_ui()
            
            # Verificar si sigue vivo
            if not self.gm.burro.alive:
                self.gm.state = GameState.GAME_OVER
                self.gm.notification.add(
                    f"💀 El burro ha muerto...",
                    Colors.TEXT_DANGER,
                    duration=300
                )
        else:
            self.gm.notification.add(
                f"{Icons.DANGER} No se pudo completar el viaje",
                Colors.TEXT_DANGER
            )
    
    def _on_eat_click(self):
        """Callback: Comer pasto."""
        if self.gm.burro.grass_in_basement <= 0:
            self.gm.notification.add(
                f"{Icons.DANGER} No hay pasto disponible",
                Colors.TEXT_DANGER
            )
            return
        
        exito = self.gm.simulador.comer_pasto(5)
        
        if exito:
            self.gm.notification.add(
                f"{Icons.EAT} El burro comió pasto",
                Colors.TEXT_SUCCESS
            )
            self.gm._update_ui()
        else:
            self.gm.notification.add(
                f"{Icons.DANGER} No se pudo comer",
                Colors.TEXT_DANGER
            )
    
    def _on_investigate_click(self):
        """Callback: Investigar estrella actual."""
        exito = self.gm.simulador.investigar_estrella(tiempo_investigacion=5.0)
        
        if exito:
            self.gm.notification.add(
                f"{Icons.INVESTIGATION} Investigación completada",
                Colors.TEXT_SUCCESS
            )
            self.gm._update_ui()
            
            # Verificar si sigue vivo
            if not self.gm.burro.alive:
                self.gm.state = GameState.GAME_OVER
        else:
            self.gm.notification.add(
                f"{Icons.DANGER} No se pudo investigar",
                Colors.TEXT_DANGER
            )
    
    def _on_config_click(self):
        """Callback: Abrir configuración."""
        self.gm.notification.add(
            "⚙️ Configuración (próximamente)",
            Colors.TEXT_SECONDARY
        )
    
    def _on_calculate_route_click(self):
        """
        Callback: Calcular ruta óptima (REQUERIMIENTO 1.2).
        
        Encuentra la ruta que permite visitar la mayor cantidad de estrellas
        con los valores iniciales del burro.
        """
        from algorithms.max_stars_route import encontrar_ruta_maxima_estrellas, obtener_nombres_ruta
        
        self.gm.notification.add(
            "🔍 Calculando ruta óptima...",
            Colors.TEXT_INFO
        )
        
        # Calcular ruta óptima
        resultado = encontrar_ruta_maxima_estrellas(
            self.gm.grafo,
            self.gm.burro,
            self.gm.simulador.posicion_actual,
            verbose=True  # Imprimir información en consola
        )
        
        # Guardar la ruta óptima en el game manager
        self.gm.optimal_route = resultado['ruta']
        self.gm.show_optimal_route = True
        self.gm.optimal_route_with_grass = []  # Limpiar la otra ruta
        
        # Mostrar resultado al usuario
        nombres = obtener_nombres_ruta(self.gm.grafo, resultado['ruta'])
        ruta_str = ' → '.join(nombres[:5])  # Mostrar primeras 5 estrellas
        if len(nombres) > 5:
            ruta_str += f" ... (+{len(nombres)-5} más)"
        
        self.gm.notification.add(
            f"✅ Ruta óptima: {resultado['estrellas_visitadas']} estrellas\n{ruta_str}",
            Colors.TEXT_SUCCESS,
            duration=5000
        )
    
    def _on_optimal_route_grass_click(self):
        """
        Callback: Calcular ruta óptima con recarga de pasto (REQUERIMIENTO 2.0).
        
        Encuentra la ruta que permite visitar la mayor cantidad de estrellas
        considerando recarga automática de pasto cuando energía < 50%.
        """
        from algorithms.optimal_route_with_grass import encontrar_ruta_optima_con_pasto
        from algorithms.max_stars_route import obtener_nombres_ruta
        
        self.gm.notification.add(
            "🔍 Calculando ruta con recarga de pasto...",
            Colors.TEXT_INFO
        )
        
        # Calcular ruta óptima con pasto
        resultado = encontrar_ruta_optima_con_pasto(
            self.gm.grafo,
            self.gm.burro,
            self.gm.simulador.posicion_actual,
            verbose=True
        )
        
        # Guardar en el game manager
        self.gm.optimal_route_with_grass = resultado['ruta']
        self.gm.show_optimal_route = True
        self.gm.optimal_route = []  # Limpiar la otra ruta
        
        # Mostrar resultado
        nombres = obtener_nombres_ruta(self.gm.grafo, resultado['ruta'])
        ruta_str = ' → '.join(nombres[:5])
        if len(nombres) > 5:
            ruta_str += f" ... (+{len(nombres)-5} más)"
        
        self.gm.notification.add(
            f"✅ Ruta con pasto: {resultado['estrellas_visitadas']} estrellas, {resultado['pasto_usado']} kg usados\n{ruta_str}",
            Colors.TEXT_SUCCESS,
            duration=6000
        )
    
    def _on_intergalactic_travel_click(self):
        """
        Callback: Abrir panel de viaje inter-galáctico (REQUERIMIENTO c).
        
        Solo disponible cuando el burro está en una hipergigante.
        """
        from utils.intergalactic import get_reachable_constellations
        
        current_star = self.gm.grafo.obtener_estrella(self.gm.simulador.posicion_actual)
        
        if not current_star or not current_star.hipergigante:
            self.gm.notification.add(
                "⚠️ Debes estar en una hipergigante para viajar inter-galácticamente",
                Colors.TEXT_DANGER,
                duration=4000
            )
            return
        
        # Obtener galaxias alcanzables (≤2 saltos) - pasamos star_id
        available_galaxies = get_reachable_constellations(
            self.gm.grafo,
            self.gm.simulador.posicion_actual  # Usar star_id, no constellation name
        )
        
        if not available_galaxies:
            self.gm.notification.add(
                "⚠️ No hay galaxias alcanzables desde aquí",
                Colors.TEXT_DANGER,
                duration=4000
            )
            return
        
        # Mostrar panel de selección
        self.gm.intergalactic_panel.show(
            self.gm.simulador.posicion_actual,
            available_galaxies
        )
        self.gm.notification.add(
            "🌌 Selecciona tu destino inter-galáctico",
            Colors.TEXT_INFO
        )
    
    def _execute_intergalactic_travel(self):
        """
        Ejecuta el viaje inter-galáctico a la estrella seleccionada.
        """
        destination_id = self.gm.intergalactic_panel.selected_destination
        if destination_id is None:
            return
        
        # Obtener estrella de destino
        destination_star = self.gm.grafo.obtener_estrella(destination_id)
        if not destination_star:
            self.gm.notification.add(
                f"{Icons.DANGER} Estrella de destino no encontrada",
                Colors.TEXT_DANGER
            )
            return
        
        # Ejecutar viaje inter-galáctico (recarga energía y pasto, sin coste)
        self.gm.burro.intergalactic_travel()
        
        # Actualizar posición del burro
        self.gm.simulador.posicion_actual = destination_id
        
        # Cerrar panel
        self.gm.intergalactic_panel.hide()
        
        # Actualizar UI
        self.gm._update_ui()
        
        # Reproducir sonido de viaje
        if hasattr(self.gm, 'sound_manager'):
            self.gm.sound_manager.play_travel()
        
        # Notificación de éxito
        self.gm.notification.add(
            f"🌌 ¡Viaje inter-galáctico a {destination_star.label}!\n"
            f"⚡ Energía: {self.gm.burro.donkey_energy:.1f}% | "
            f"🌾 Pasto: {self.gm.burro.grass_in_basement:.1f} kg",
            Colors.TEXT_SUCCESS,
            duration=5000
        )
    
    def _debug_travel(self, resultado):
        """Imprime información de debug para el viaje."""
        print(f"\n🔍 DEBUG VIAJE:")
        print(f"   Desde: {self.gm.simulador.posicion_actual}")
        print(f"   Hacia: {self.gm.selected_star_id}")
        print(f"   Energía del burro: {self.gm.burro.donkey_energy}")
        
        if resultado and resultado['existe']:
            print(f"   Distancia necesaria: {resultado['distancia']}")
            print(f"   Puede viajar: {resultado['distancia'] <= self.gm.burro.donkey_energy}")
        else:
            print(f"   No hay ruta disponible")
