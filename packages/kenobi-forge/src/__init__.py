"""
Package Kenobi-Forge
Assistant IA pour développement selon spécifications SPARCTER
"""

from .forge_kenobi_assistant import ForgeKenobiAssistant, get_forge_kenobi_assistant
from .forge_kenobi_engine import ForgeKenobiEngine
from .kenobi_integration import (
    KenobiIntegration,
    get_kenobi_integration,
    kenobi_check,
    kenobi_execute,
    kenobi_guidance,
)

__version__ = "1.4.0"
__framework__ = "SPARCTER"

__all__ = [
    "ForgeKenobiAssistant",
    "ForgeKenobiEngine",
    "KenobiIntegration",
    "get_forge_kenobi_assistant",
    "get_kenobi_integration",
    "kenobi_check",
    "kenobi_execute",
    "kenobi_guidance",
]
