"""
Script de prueba rápida para verificar que todos los módulos se importen correctamente.
"""

print("🧪 Verificando módulos...")
print("=" * 70)

try:
    print("✓ Importando models...")
    from models.star import Estrella
    from models.graph import Graph, Vertex
    from models.constellation import GrafoConstelaciones
    from models.donkey import Donkey
    from models.simulator import SimuladorViaje
    from models.travel_manager import TravelManager
    print("  ✅ models OK")
    
    print("\n✓ Importando algorithms...")
    from algorithms.dijkstra import dijkstra, encontrar_camino_mas_corto
    from algorithms.bellman_ford import bellman_ford
    print("  ✅ algorithms OK")
    
    print("\n✓ Importando utils...")
    from utils.config_loader import cargar_grafo_desde_json, crear_burro_desde_json
    print("  ✅ utils OK")
    
    print("\n✓ Verificando Pygame...")
    try:
        import pygame
        print("  ✅ Pygame instalado")
    except ImportError:
        print("  ⚠️  Pygame NO instalado (ejecuta: pip install pygame)")
        print("     La GUI no funcionará sin Pygame")
    
    print("\n✓ Importando GUI...")
    from gui.config import Colors, WINDOW_WIDTH
    from gui.components import Button, Panel, ProgressBar
    from gui.graph_renderer import GraphRenderer, StarRenderer
    from gui.panels import DonkeyInfoPanel, StarInfoPanel
    from gui.game import GameManager
    print("  ✅ GUI modules OK")
    
    print("\n" + "=" * 70)
    print("✅ TODOS LOS MÓDULOS SE IMPORTARON CORRECTAMENTE")
    print("=" * 70)
    
    print("\n📋 Próximos pasos:")
    print("  1. Para jugar con GUI: python play.py")
    print("  2. Para usar versión terminal: python main.py")
    
except ImportError as e:
    print(f"\n❌ ERROR DE IMPORTACIÓN:")
    print(f"   {e}")
    print("\n💡 Verifica que todos los archivos estén en su lugar")
    import traceback
    traceback.print_exc()

except Exception as e:
    print(f"\n❌ ERROR INESPERADO:")
    print(f"   {e}")
    import traceback
    traceback.print_exc()
