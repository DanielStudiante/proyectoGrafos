"""
Launcher para la aplicación gráfica del Burro Científico.
Ejecuta este archivo para iniciar el juego.
"""

import sys
import os

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import pygame
except ImportError:
    print("="*70)
    print("❌ ERROR: Pygame no está instalado")
    print("="*70)
    print("\nPara instalar Pygame, ejecuta:")
    print("  pip install pygame")
    print("\nEn Windows:")
    print("  py -m pip install pygame")
    print("="*70)
    sys.exit(1)

from gui.game import main

if __name__ == "__main__":
    print("="*70)
    print("🚀 Iniciando Simulador del Burro Científico")
    print("="*70)
    print("\nControles:")
    print("  🖱️  Click en estrellas para seleccionar")
    print("  🎮 Botones en panel derecho para acciones")
    print("  ESPACIO = Comer pasto")
    print("  I = Investigar estrella actual")
    print("  ESC = Salir")
    print("\n" + "="*70 + "\n")
    
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error durante la ejecución: {e}")
        import traceback
        traceback.print_exc()
        input("\nPresiona Enter para salir...")
