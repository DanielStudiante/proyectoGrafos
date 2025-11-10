"""
Módulo de re-exportación de paneles.
Mantiene compatibilidad con imports existentes.
"""

from gui.info_panels import DonkeyInfoPanel, StarInfoPanel
from gui.action_panels import ActionsPanel, ReachableStarsPanel

__all__ = [
    'DonkeyInfoPanel',
    'StarInfoPanel',
    'ActionsPanel',
    'ReachableStarsPanel'
]
