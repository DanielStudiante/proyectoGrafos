"""
Punto de entrada del juego del Burro Científico.
Responsabilidad: Iniciar la aplicación gráfica.
"""

from views.game_manager import GameManager


def main():
    """Punto de entrada de la aplicación gráfica."""
    game = GameManager()
    game.run()


if __name__ == "__main__":
    main()
