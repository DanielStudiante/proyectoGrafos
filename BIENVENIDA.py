"""
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║        🐴  BURRO CIENTÍFICO - EXPLORADOR DE CONSTELACIONES  ✨       ║
║                                                                      ║
║              Simulador de Viajes Interestelares                      ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝

📋 DESCRIPCIÓN:
   Controla un burro científico que explora constelaciones, viajando
   entre estrellas, investigando fenómenos y gestionando recursos.
   
🎮 MODOS DE JUEGO:

   1. MODO GRÁFICO (Recomendado) 🎨
      ─────────────────────────────────────────────────────────
      • Interfaz visual completa con Pygame
      • Grafo interactivo de estrellas
      • Paneles de información en tiempo real
      • Animaciones y efectos visuales
      • Click para seleccionar destinos
      
      Ejecutar:  python play.py
      
   
   2. MODO TERMINAL ⌨️
      ─────────────────────────────────────────────────────────
      • Interfaz basada en texto
      • Configuración de efectos antes del viaje
      • Sistema de menús interactivo
      
      Ejecutar:  python main.py


📚 CARACTERÍSTICAS:

   ⭐ Sistema de Estrellas
      • Estrellas normales y hipergigantes
      • Coordenadas espaciales únicas
      • Agrupadas en constelaciones
   
   🔬 Sistema de Investigación
      • Efectos en la salud del burro
      • Ganancia o pérdida de tiempo de vida
      • Configurables antes del viaje
   
   🧠 Algoritmos de Pathfinding
      • Dijkstra para caminos más cortos
      • Cálculo de estrellas alcanzables
      • Optimización de rutas
   
   💚 Gestión de Recursos
      • Energía del burro
      • Pasto para recuperación
      • Edad y tiempo de vida


🎯 OBJETIVO:
   Explorar el máximo de estrellas posible sin que el burro muera.
   Gestiona cuidadosamente tu energía, pasto y efectos de investigación.


📖 DOCUMENTACIÓN:
   • README_GUI.md        - Guía completa de la interfaz gráfica
   • README_EFECTOS.md    - Sistema de efectos de investigación
   • RESUMEN_FINAL.md     - Resumen de implementación completo


🔧 REQUISITOS:
   • Python 3.10+
   • Pygame 2.5+ (para modo gráfico)
   
   Instalar: pip install pygame


🚀 INICIO RÁPIDO:

   1. Verificar que todo esté bien:
      python test_imports.py
   
   2. Jugar con interfaz gráfica:
      python play.py
   
   3. O usar versión terminal:
      python main.py


💡 TIPS:
   • Las estrellas hipergigantes (⭐) dan bonus de energía y pasto
   • Algunos experimentos mejoran tu salud, otros la empeoran
   • Gestiona bien tu pasto para emergencias
   • Planifica rutas largas con cuidado


╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║            ¡Buena suerte en tu exploración espacial! 🌌              ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
"""

if __name__ == "__main__":
    print(__doc__)
    print("\n¿Qué quieres hacer?")
    print("  1. Jugar con interfaz gráfica (python play.py)")
    print("  2. Jugar en terminal (python main.py)")
    print("  3. Verificar instalación (python test_imports.py)")
    print("\nElige una opción y ejecuta el comando correspondiente.")
