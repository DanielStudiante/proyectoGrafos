"""
Gestor de sonidos del juego.
Responsabilidad: Reproducir efectos de sonido en momentos clave.
"""

import pygame
import os


class SoundManager:
    """
    Gestor de sonidos del juego.
    
    Responsabilidades (SRP):
    - Cargar archivos de sonido
    - Reproducir efectos en momentos específicos
    - Controlar volumen
    """
    
    def __init__(self, enabled: bool = True):
        """
        Inicializa el gestor de sonidos.
        
        Args:
            enabled: Si False, no reproduce sonidos
        """
        self.enabled = enabled
        self.sounds = {}
        
        # Inicializar pygame mixer si está habilitado
        if self.enabled:
            try:
                pygame.mixer.init()
                self.volume = 0.7
                self._load_sounds()
            except Exception as e:
                print(f"⚠️  No se pudo inicializar el sistema de sonido: {e}")
                self.enabled = False
    
    def _load_sounds(self):
        """Carga los archivos de sonido."""
        sound_dir = "sounds"
        
        # Crear directorio si no existe
        if not os.path.exists(sound_dir):
            os.makedirs(sound_dir)
            print(f"📁 Directorio '{sound_dir}/' creado. Coloca archivos .wav ahí.")
        
        # Definir rutas de sonidos
        sound_files = {
            'death': 'death.wav',
            'click': 'click.wav',
            'travel': 'travel.wav',
            'eat': 'eat.wav',
            'heal': 'heal.wav',
            'damage': 'damage.wav',
            'victory': 'victory.wav',
        }
        
        # Intentar cargar cada sonido
        for name, filename in sound_files.items():
            path = os.path.join(sound_dir, filename)
            if os.path.exists(path):
                try:
                    self.sounds[name] = pygame.mixer.Sound(path)
                    self.sounds[name].set_volume(self.volume)
                    print(f"🔊 Sonido cargado: {name}")
                except Exception as e:
                    print(f"⚠️  Error cargando {name}: {e}")
    
    def play(self, sound_name: str):
        """
        Reproduce un sonido.
        
        Args:
            sound_name: Nombre del sonido ('death', 'click', etc.)
        """
        if not self.enabled:
            return
        
        if sound_name in self.sounds:
            try:
                self.sounds[sound_name].play()
            except Exception as e:
                print(f"⚠️  Error reproduciendo {sound_name}: {e}")
        else:
            # Si no existe el archivo, usar sonido sintético de pygame
            if sound_name == 'death':
                self._play_synthetic_death_sound()
    
    def _play_synthetic_death_sound(self):
        """Genera un sonido sintético de muerte usando pygame (sin archivo)."""
        try:
            # Crear un sonido sintético simple
            # Frecuencia descendente para simular "muerte"
            duration = 500  # milisegundos
            sample_rate = 22050
            
            # Nota: pygame.sndarray requiere numpy, usamos un approach simple
            # Si no hay archivo, simplemente imprimimos
            print("💀 ¡EL BURRO HA MUERTO!")
            
        except Exception as e:
            print(f"⚠️  Error generando sonido sintético: {e}")
    
    def play_death(self):
        """Reproduce el sonido de muerte del burro."""
        print("\n" + "="*70)
        print("💀 ¡EL BURRO HA MUERTO! 💀")
        print("="*70 + "\n")
        self.play('death')
    
    def play_click(self):
        """Reproduce sonido de click."""
        self.play('click')
    
    def play_travel(self):
        """Reproduce sonido de viaje."""
        self.play('travel')
    
    def play_eat(self):
        """Reproduce sonido de comer."""
        self.play('eat')
    
    def play_heal(self):
        """Reproduce sonido de curación."""
        self.play('heal')
    
    def play_damage(self):
        """Reproduce sonido de daño."""
        self.play('damage')
    
    def play_victory(self):
        """Reproduce sonido de victoria."""
        self.play('victory')
    
    def set_volume(self, volume: float):
        """
        Establece el volumen general.
        
        Args:
            volume: Volumen de 0.0 a 1.0
        """
        self.volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            sound.set_volume(self.volume)
    
    def toggle(self):
        """Activa/desactiva los sonidos."""
        self.enabled = not self.enabled
        return self.enabled
