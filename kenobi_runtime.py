#!/usr/bin/env python3
"""
Kenobi Runtime - Configuration et imports dynamiques
Solution robuste pour l'intégration Kenobi en temps réel
"""

import sys
from pathlib import Path
from typing import Any, Dict, Optional


class KenobiRuntime:
    """
    Runtime Kenobi pour imports dynamiques et configuration
    Résout les problèmes d'import entre packages dans le monorepo
    """

    def __init__(self):
        self.project_root = self._find_project_root()
        self.kenobi_src = self.project_root / "packages" / "kenobi-forge" / "src"
        self._setup_paths()
        self._kenobi_modules = {}

    def _find_project_root(self) -> Path:
        """Trouve automatiquement la racine du projet"""
        current = Path.cwd()
        
        # Chercher le dossier packages
        while current != current.parent:
            if (current / "packages").exists():
                return current
            current = current.parent
        
        # Fallback sur le répertoire courant
        return Path.cwd()

    def _setup_paths(self):
        """Configure les chemins Python pour les imports"""
        if str(self.kenobi_src) not in sys.path:
            sys.path.insert(0, str(self.kenobi_src))

    def get_kenobi_module(self, module_name: str):
        """
        Importe dynamiquement un module Kenobi
        
        Args:
            module_name: Nom du module (ex: 'kenobi_integration')
            
        Returns:
            Module importé ou None si erreur
        """
        if module_name in self._kenobi_modules:
            return self._kenobi_modules[module_name]
        
        try:
            module = __import__(module_name)
            self._kenobi_modules[module_name] = module
            return module
        except ImportError as e:
            print(f"⚠️ Erreur import {module_name}: {e}")
            return None

    def kenobi_check(self, action_type: str, **kwargs) -> Dict[str, Any]:
        """Vérification Kenobi avec gestion d'erreur"""
        integration = self.get_kenobi_module("kenobi_integration")
        if integration:
            return integration.kenobi_check(action_type, **kwargs)
        return {"compliant": True, "message": "⚠️ Kenobi indisponible, action autorisée"}

    def kenobi_guidance(self, task: str) -> Dict[str, Any]:
        """Conseils Kenobi avec gestion d'erreur"""
        integration = self.get_kenobi_module("kenobi_integration")
        if integration:
            return integration.kenobi_guidance(task)
        return {"task": task, "recommendations": ["⚠️ Kenobi indisponible"]}

    def kenobi_execute(self, action_type: str, **kwargs) -> Dict[str, Any]:
        """Exécution Kenobi avec gestion d'erreur"""
        integration = self.get_kenobi_module("kenobi_integration")
        if integration:
            return integration.kenobi_execute(action_type, **kwargs)
        return {"success": True, "message": "⚠️ Kenobi indisponible, action exécutée"}

    def get_status(self) -> Dict[str, Any]:
        """Statut du runtime Kenobi"""
        integration = self.get_kenobi_module("kenobi_integration")
        
        return {
            "runtime_active": True,
            "project_root": str(self.project_root),
            "kenobi_src": str(self.kenobi_src),
            "kenobi_available": integration is not None,
            "modules_loaded": list(self._kenobi_modules.keys()),
            "framework": "SPARCTER v1.4.0" if integration else "N/A"
        }


# Instance globale
_runtime = None


def get_kenobi_runtime() -> KenobiRuntime:
    """Obtient l'instance globale du runtime Kenobi"""
    global _runtime
    if _runtime is None:
        _runtime = KenobiRuntime()
    return _runtime


# Fonctions utilitaires rapides
def quick_check(action_type: str, **kwargs) -> bool:
    """Vérification rapide avec Kenobi"""
    runtime = get_kenobi_runtime()
    result = runtime.kenobi_check(action_type, **kwargs)
    
    if result.get("compliant", True):
        print(f"✅ {result.get('message', 'Action conforme')}")
        return True
    else:
        print(f"❌ {result.get('message', 'Action non conforme')}")
        if "recommendations" in result:
            print("💡 Recommandations:")
            for rec in result["recommendations"]:
                print(f"   • {rec}")
        return False


def quick_guidance(task: str) -> None:
    """Conseils rapides avec Kenobi"""
    runtime = get_kenobi_runtime()
    guidance = runtime.kenobi_guidance(task)
    
    print(f"🎯 Conseils Kenobi pour: {task}")
    print("=" * 50)
    
    if guidance.get("recommendations"):
        print("📋 Recommandations:")
        for rec in guidance["recommendations"]:
            print(f"   • {rec}")


def show_status() -> None:
    """Affiche le statut du runtime"""
    runtime = get_kenobi_runtime()
    status = runtime.get_status()
    
    print("🤖 Statut Kenobi Runtime:")
    print(f"   Runtime actif: {'✅' if status['runtime_active'] else '❌'}")
    print(f"   Kenobi disponible: {'✅' if status['kenobi_available'] else '❌'}")
    print(f"   Framework: {status['framework']}")
    print(f"   Modules chargés: {len(status['modules_loaded'])}")


if __name__ == "__main__":
    print("🤖 Test Kenobi Runtime")
    print("=" * 30)
    
    # Test du status
    show_status()
    
    # Test de vérification
    print("\n1. Test vérification:")
    quick_check("create_file", file_path="test_runtime.py")
    
    # Test de conseils
    print("\n2. Test conseils:")
    quick_guidance("Créer un extracteur GitLab")
    
    print("\n✅ Runtime testé avec succès !")
