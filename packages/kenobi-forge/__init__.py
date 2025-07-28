"""
Kenobi-Forge Package
Assistant IA pour développement ETL DevSecOps selon SPARCTER v1.4.0
"""

# Import explicite pour éviter F403
from .src.forge_kenobi_assistant import ForgeKenobiAssistant
from .src.forge_kenobi_engine import ForgeKenobiEngine
from .src.kenobi_cli import main as kenobi_main

__version__ = "1.4.0"

__all__ = ["ForgeKenobiAssistant", "ForgeKenobiEngine", "kenobi_main"]
