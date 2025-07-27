"""
Intégration Kenobi pour GitHub Copilot
Wrapper qui permet à l'IA d'utiliser systématiquement l'assistant Forge-Kenobi
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from forge_kenobi_assistant import (
    ActionType,
    ForgeKenobiAssistant,
    get_forge_kenobi_assistant,
)


class KenobiIntegration:
    """
    Intégration Kenobi pour GitHub Copilot
    
    Permet à l'IA d'utiliser automatiquement l'assistant Forge-Kenobi
    pour toutes les actions de développement.
    """

    def __init__(self, project_root: Optional[str] = None):
        """Initialise l'intégration Kenobi"""
        if project_root is None:
            # Détection automatique de la racine du projet
            current_dir = Path.cwd()
            if "ETL DevSecOps" in str(current_dir):
                # Si on est dans le dossier du projet
                project_root = str(current_dir)
                while not (Path(project_root) / "packages").exists():
                    parent = Path(project_root).parent
                    if parent == Path(project_root):
                        break
                    project_root = str(parent)
            else:
                project_root = "."
        
        self.assistant = get_forge_kenobi_assistant(project_root)
        self.session_actions = []
        
    def check_compliance_before_action(
        self, action_type: str, details: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Vérification de conformité avant toute action
        
        Args:
            action_type: Type d'action (create_file, modify_file, etc.)
            details: Détails de l'action
            
        Returns:
            Résultat de la vérification avec recommandations
        """
        try:
            action_enum = ActionType(action_type)
        except ValueError:
            return {
                "compliant": False,
                "message": f"❌ Type d'action '{action_type}' non reconnu par Kenobi",
                "available_actions": [e.value for e in ActionType]
            }
        
        is_compliant, message = self.assistant.before_action_check(
            action_enum, details
        )
        
        result = {
            "compliant": is_compliant,
            "message": message,
            "kenobi_context": {
                "framework": self.assistant.context.framework,
                "version": self.assistant.context.version,
                "mission": self.assistant.context.mission_objective
            }
        }
        
        if not is_compliant:
            result["recommendations"] = self._get_compliance_recommendations(
                action_enum, details, message
            )
        
        return result
    
    def execute_with_kenobi(
        self, action_type: str, details: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Exécute une action avec validation Kenobi complète
        
        Args:
            action_type: Type d'action
            details: Détails de l'action
            
        Returns:
            Résultat de l'exécution avec contexte Kenobi
        """
        try:
            action_enum = ActionType(action_type)
        except ValueError:
            return {
                "success": False,
                "error": f"Type d'action '{action_type}' non reconnu",
                "kenobi_status": "INVALID_ACTION"
            }
        
        # Exécution avec l'assistant Kenobi
        result = self.assistant.execute_with_compliance(action_enum, details)
        
        # Logging de l'action pour le suivi
        self.session_actions.append({
            "action_type": action_type,
            "details": details,
            "result": result,
            "timestamp": self._get_timestamp()
        })
        
        return result
    
    def get_kenobi_guidance(self, task_description: str) -> Dict[str, Any]:
        """
        Obtient des conseils Kenobi pour une tâche spécifique
        
        Args:
            task_description: Description de la tâche à réaliser
            
        Returns:
            Conseils et recommandations Kenobi
        """
        context = self.assistant.context
        
        guidance = {
            "task": task_description,
            "applicable_specifications": [],
            "coding_conventions": context.coding_conventions,
            "architecture_constraints": context.architecture_rules,
            "recommendations": []
        }
        
        # Identifier les spécifications applicables
        for spec in context.specifications:
            if any(keyword in task_description.lower() for keyword in [
                "file", "create", "modify", "structure", "code", "naming"
            ]):
                guidance["applicable_specifications"].append({
                    "id": spec["id"],
                    "title": spec["title"],
                    "description": spec["description"]
                })
        
        # Recommandations spécifiques
        if "file" in task_description.lower():
            guidance["recommendations"].append(
                "🔤 Nommage: snake_case obligatoire (SPC-GEN-01)"
            )
        
        if "etl" in task_description.lower():
            guidance["recommendations"].append(
                "🏗️ Architecture: Respecter extractors/ → transformers/ → loaders/"
            )
        
        if "code" in task_description.lower():
            guidance["recommendations"].append(
                "✨ Formatage: Black 88 char., f-strings obligatoires"
            )
        
        return guidance
    
    def get_session_summary(self) -> Dict[str, Any]:
        """
        Résumé de la session avec Kenobi
        
        Returns:
            Statistiques et actions de la session
        """
        total_actions = len(self.session_actions)
        successful_actions = sum(
            1 for action in self.session_actions 
            if action["result"].get("success", False)
        )
        
        return {
            "session_stats": {
                "total_actions": total_actions,
                "successful_actions": successful_actions,
                "compliance_rate": (successful_actions / total_actions * 100) if total_actions > 0 else 0
            },
            "kenobi_context": self.assistant.get_context_summary(),
            "recent_actions": self.session_actions[-5:] if self.session_actions else []
        }
    
    def _get_compliance_recommendations(
        self, action_type: ActionType, details: Dict[str, Any], error_message: str
    ) -> List[str]:
        """Génère des recommandations pour corriger les problèmes de conformité"""
        recommendations = []
        
        if "snake_case" in error_message:
            recommendations.append(
                "🔤 Renommer le fichier en snake_case (ex: my_file.py)"
            )
        
        if "f-strings" in error_message:
            recommendations.append(
                "✨ Remplacer .format() et % par des f-strings"
            )
        
        if "Poetry" in error_message:
            recommendations.append(
                "📦 Utiliser 'poetry add <package>' au lieu de pip install"
            )
        
        if "Architecture ETL" in error_message:
            recommendations.append(
                "🏗️ Créer la structure: packages/etl-core/etl/{core,extractors,transformers,loaders}/"
            )
        
        return recommendations
    
    def _get_timestamp(self) -> str:
        """Génère un timestamp pour le logging"""
        from datetime import datetime
        return datetime.now().isoformat()


# Instance globale pour utilisation facile
_kenobi_integration = None


def get_kenobi_integration() -> KenobiIntegration:
    """
    Obtient l'instance globale de l'intégration Kenobi
    
    Returns:
        Instance de KenobiIntegration
    """
    global _kenobi_integration
    if _kenobi_integration is None:
        _kenobi_integration = KenobiIntegration()
    return _kenobi_integration


def kenobi_check(action_type: str, **details) -> Dict[str, Any]:
    """
    Fonction utilitaire pour vérification rapide Kenobi
    
    Args:
        action_type: Type d'action à vérifier
        **details: Détails de l'action
        
    Returns:
        Résultat de la vérification
        
    Example:
        result = kenobi_check("create_file", file_path="src/my_extractor.py")
        if result["compliant"]:
            # Procéder avec l'action
        else:
            # Afficher les recommandations
    """
    integration = get_kenobi_integration()
    return integration.check_compliance_before_action(action_type, details)


def kenobi_execute(action_type: str, **details) -> Dict[str, Any]:
    """
    Fonction utilitaire pour exécution avec Kenobi
    
    Args:
        action_type: Type d'action à exécuter
        **details: Détails de l'action
        
    Returns:
        Résultat de l'exécution
        
    Example:
        result = kenobi_execute("create_file", 
                               file_path="src/extract_gitlab.py", 
                               content="# ETL GitLab")
    """
    integration = get_kenobi_integration()
    return integration.execute_with_kenobi(action_type, details)


def kenobi_guidance(task: str) -> Dict[str, Any]:
    """
    Fonction utilitaire pour obtenir des conseils Kenobi
    
    Args:
        task: Description de la tâche
        
    Returns:
        Conseils et recommandations
        
    Example:
        guidance = kenobi_guidance("Créer un extracteur GitLab")
    """
    integration = get_kenobi_integration()
    return integration.get_kenobi_guidance(task)


if __name__ == "__main__":
    # Test de l'intégration
    integration = KenobiIntegration()
    
    print("🤖 Test de l'intégration Kenobi")
    print("=" * 50)
    
    # Test 1: Vérification de conformité
    print("\n1. Test de vérification de conformité:")
    result = kenobi_check("create_file", file_path="test_file.py")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    # Test 2: Conseils pour une tâche
    print("\n2. Test de conseils Kenobi:")
    guidance = kenobi_guidance("Créer un extracteur GitLab")
    print(json.dumps(guidance, indent=2, ensure_ascii=False))
    
    # Test 3: Résumé de session
    print("\n3. Résumé de session:")
    summary = integration.get_session_summary()
    print(json.dumps(summary, indent=2, ensure_ascii=False))
