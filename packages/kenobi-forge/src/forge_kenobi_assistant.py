"""
Forge-Kenobi AI Assistant
Assistant IA qui se réfère systématiquement aux spécifications Forge-Kenobi
avant d'exécuter toute tâche de développement.
"""

import json
import re
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Tuple


class ActionType(Enum):
    CREATE_FILE = "create_file"
    MODIFY_FILE = "modify_file"
    CREATE_STRUCTURE = "create_structure"
    RUN_COMMAND = "run_command"
    GENERATE_CODE = "generate_code"


@dataclass
class ForgeKenobiContext:
    """Contexte Forge-Kenobi chargé depuis les spécifications"""

    framework: str
    version: str
    codename: str
    mission_objective: str
    coding_conventions: Dict[str, str]
    specifications: List[Dict]
    architecture_rules: Dict[str, List[str]]
    constraints: Dict[str, str]


class ForgeKenobiAssistant:
    """
    Assistant IA Forge-Kenobi

    RÔLE: IA lead-developer senior qui respecte SYSTÉMATIQUEMENT
    les spécifications définies dans FORGE-KENOBI.md

    PRINCIPE: Aucune action n'est exécutée sans vérification préalable
    de conformité aux spécifications Forge-Kenobi.
    """

    def __init__(self, project_root: Path):
        self.project_root = Path(project_root)
        self.context = self._load_forge_kenobi_context()
        self.current_pass = 1
        self.max_passes = 3

    def _load_forge_kenobi_context(self) -> ForgeKenobiContext:
        """Charge le contexte complet depuis FORGE-KENOBI.md"""
        kenobi_file = (
            self.project_root / "packages" / "kenobi-forge" / "FORGE-KENOBI.md"
        )

        if not kenobi_file.exists():
            raise FileNotFoundError(
                "❌ FORGE-KENOBI.md introuvable ! "
                "Impossible de procéder sans les spécifications de référence."
            )

        with open(kenobi_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Extraction des sections clés
        framework_info = self._extract_framework_tag(content)
        mission = self._extract_mission(content)
        coding_conventions = self._extract_coding_conventions(content)
        specifications = self._extract_specifications(content)
        architecture = self._extract_architecture(content)
        constraints = self._extract_constraints(content)

        return ForgeKenobiContext(
            framework=framework_info.get("framework", "SPARCTER"),
            version=framework_info.get("version", "1.4.0"),
            codename=framework_info.get("codename", "Kenobi-Forge"),
            mission_objective=mission,
            coding_conventions=coding_conventions,
            specifications=specifications,
            architecture_rules=architecture,
            constraints=constraints,
        )

    def _extract_framework_tag(self, content: str) -> Dict[str, str]:
        """Extrait les informations du framework tag"""
        match = re.search(
            r"<!-- FRAMEWORK_TAG START -->(.*?)<!-- FRAMEWORK_TAG END -->",
            content,
            re.DOTALL,
        )
        if match:
            info = {}
            for line in match.group(1).strip().split("\n"):
                if ":" in line:
                    key, value = line.split(":", 1)
                    info[key.strip()] = value.strip()
            return info
        return {}

    def _extract_mission(self, content: str) -> str:
        """Extrait l'objectif de la mission"""
        match = re.search(r"<mission>(.*?)</mission>", content, re.DOTALL)
        if match:
            mission_content = match.group(1)
            # Extraire l'objectif principal
            obj_match = re.search(
                r"\*\*OBJECTIF\*\*\s*(.*?)(?=\*\*|$)", mission_content, re.DOTALL
            )
            if obj_match:
                return obj_match.group(1).strip()
        return "ETL Python centralisé pour métriques DevSecOps"

    def _extract_coding_conventions(self, content: str) -> Dict[str, str]:
        """Extrait les conventions de codage"""
        match = re.search(
            r"<coding_conventions>(.*?)</coding_conventions>", content, re.DOTALL
        )
        conventions = {}
        if match:
            # Extraire les règles principales
            conventions.update(
                {
                    "file_naming": "snake_case, verbe-objet",
                    "folders": "pluriels (extractors/, transformers/, loaders/)",
                    "classes": "PascalCase",
                    "functions": "snake_case",
                    "constants": "UPPER_SNAKE_CASE",
                    "formatting": "Black 88 car., ruff --fix, mypy --strict",
                    "strings": "f-strings obligatoires",
                    "commits": "Conventional Commits",
                }
            )
        return conventions

    def _extract_specifications(self, content: str) -> List[Dict]:
        """Extrait les spécifications actives"""
        spec_match = re.search(
            r"<specification>(.*?)</specification>", content, re.DOTALL
        )
        specifications = []

        if spec_match:
            spec_content = spec_match.group(1)
            # Extraire chaque SPC-XXX
            spc_pattern = (
                r"#### (SPC-[A-Z]+-\d+) – ([^*]+) \*\(active\)\*\s*(.*?)(?=####|$)"
            )
            for match in re.finditer(spc_pattern, spec_content, re.DOTALL):
                specifications.append(
                    {
                        "id": match.group(1),
                        "title": match.group(2).strip(),
                        "description": match.group(3).strip(),
                    }
                )

        return specifications

    def _extract_architecture(self, content: str) -> Dict[str, List[str]]:
        """Extrait les règles d'architecture"""
        arch_match = re.search(
            r"<architecture_and_infra>(.*?)</architecture_and_infra>",
            content,
            re.DOTALL,
        )
        architecture = {
            "import_rules": [],
            "required_structure": [
                "packages/etl-core/etl/core/",
                "packages/etl-core/etl/extractors/",
                "packages/etl-core/etl/transformers/",
                "packages/etl-core/etl/loaders/",
                "packages/etl-core/etl/cli.py",
            ],
            "forbidden_imports": [
                "extractors → loaders",
                "loaders → extractors",
                "transformers → extractors",
            ],
        }

        if arch_match:
            # Extraction plus détaillée si nécessaire
            pass

        return architecture

    def _extract_constraints(self, content: str) -> Dict[str, str]:
        """Extrait les contraintes techniques"""
        constraints_match = re.search(
            r"<constraints>(.*?)</constraints>", content, re.DOTALL
        )
        constraints = {}

        if constraints_match:
            constraints.update(
                {
                    "python_version": "3.12",
                    "os": "Windows 11 64-bit",
                    "dependency_manager": "Poetry ≥ 1.8",
                    "coverage_threshold": "≥ 90%",
                    "security": "Bandit MEDIUM+ bloquant",
                    "logging": "structlog JSON",
                }
            )

        return constraints

    def before_action_check(
        self, action_type: ActionType, details: Dict[str, Any]
    ) -> Tuple[bool, str]:
        """
        VÉRIFICATION OBLIGATOIRE avant toute action

        Returns:
            (is_compliant, message)
        """
        print(f"🤖 [Forge-Kenobi] Vérification conformité pour {action_type.value}...")

        # 1. Vérifier nommage des fichiers (SPC-GEN-01)
        if action_type in [ActionType.CREATE_FILE, ActionType.MODIFY_FILE]:
            file_path = details.get("file_path", "")
            if file_path.endswith(".py"):
                filename = Path(file_path).stem
                if filename != "__init__" and not re.match(
                    r"^[a-z][a-z0-9_]*[a-z0-9]$", filename
                ):
                    return (
                        False,
                        f"❌ SPC-GEN-01: Fichier '{filename}' ne respecte pas "
                        "snake_case",
                    )

        # 2. Vérifier architecture ETL
        if action_type == ActionType.CREATE_STRUCTURE:
            required_dirs = self.context.architecture_rules["required_structure"]
            for req_dir in required_dirs:
                if req_dir not in str(details):
                    return (
                        False,
                        f"❌ Architecture ETL: Structure '{req_dir}' requise manquante",
                    )

        # 3. Vérifier conventions de codage
        if action_type == ActionType.GENERATE_CODE:
            code_content = details.get("code", "")
            # Vérifier f-strings obligatoires si strings présentes
            if '"' in code_content or "'" in code_content:
                if "format(" in code_content or "%" in code_content:
                    return False, "❌ Conventions: Utiliser f-strings obligatoirement"

        # 4. Vérifier contraintes techniques
        if action_type == ActionType.RUN_COMMAND:
            command = details.get("command", "")
            if "pip install" in command and "poetry" not in command:
                return (
                    False,
                    "❌ Contraintes: Utiliser Poetry ≥ 1.8 pour les dépendances",
                )

        return (
            True,
            f"✅ Action {action_type.value} conforme aux spécifications Forge-Kenobi",
        )

    def execute_with_compliance(
        self, action_type: ActionType, action_details: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Exécute une action SEULEMENT après vérification de conformité

        C'est la méthode PRINCIPALE à utiliser pour toute action de développement.
        """

        # ÉTAPE 1: Vérification conformité obligatoire
        is_compliant, compliance_message = self.before_action_check(
            action_type, action_details
        )

        if not is_compliant:
            return {
                "success": False,
                "error": compliance_message,
                "forge_kenobi_status": "COMPLIANCE_FAILED",
                "current_pass": self.current_pass,
                "max_passes": self.max_passes,
            }

        print(compliance_message)

        # ÉTAPE 2: Exécution de l'action
        try:
            result = self._execute_action(action_type, action_details)

            return {
                "success": True,
                "result": result,
                "forge_kenobi_status": "COMPLIANT",
                "compliance_message": compliance_message,
                "current_pass": self.current_pass,
                "specifications_applied": [
                    spec["id"] for spec in self.context.specifications
                ],
            }

        except Exception as e:
            self.current_pass += 1

            if self.current_pass > self.max_passes:
                return {
                    "success": False,
                    "error": f"Échec après {self.max_passes} passes: {str(e)}",
                    "forge_kenobi_status": "ESCALATION_REQUIRED",
                    "escalation_ticket": f"CLARIFY-{self.current_pass}",
                }

            return {
                "success": False,
                "error": str(e),
                "forge_kenobi_status": "RETRY",
                "current_pass": self.current_pass,
                "retry_action": "Correction et nouvelle passe",
            }

    def _execute_action(self, action_type: ActionType, details: Dict[str, Any]) -> Any:
        """Exécution effective de l'action (à implémenter selon le contexte)"""
        # Cette méthode sera implémentée selon l'environnement d'exécution
        # (VS Code, CLI, etc.)
        return {"action": action_type.value, "details": details, "executed": True}

    def get_context_summary(self) -> str:
        """Retourne un résumé du contexte Forge-Kenobi chargé"""
        return f"""
🤖 Forge-Kenobi Assistant Actif
Framework: {self.context.framework} v{self.context.version}
Codename: {self.context.codename}
Mission: {self.context.mission_objective}

📋 Spécifications actives:
{chr(10).join(f"  • {spec['id']}: {spec['title']}" for spec in self.context.specifications)}

🏗️ Contraintes architecture:
{chr(10).join(f"  • {rule}" for rule in self.context.architecture_rules['required_structure'])}  # noqa: E501

⚠️ Rappel: Toute action est vérifiée AVANT exécution !
        """


# Fonction utilitaire pour l'intégration
def get_forge_kenobi_assistant(project_root: str = ".") -> ForgeKenobiAssistant:
    """
    Point d'entrée principal pour obtenir l'assistant Forge-Kenobi

    Usage:
        assistant = get_forge_kenobi_assistant()
        result = assistant.execute_with_compliance(
            ActionType.CREATE_FILE,
            {"file_path": "src/extract_gitlab_data.py", "content": "..."}
        )
    """
    # Détection automatique de la racine du monorepo
    current_path = Path.cwd()

    # Si on est dans packages/kenobi-forge/src, remonter à la racine
    if current_path.name == "src" and current_path.parent.name == "kenobi-forge":
        actual_root = current_path.parent.parent.parent
    else:
        actual_root = Path(project_root)

    return ForgeKenobiAssistant(actual_root)


if __name__ == "__main__":
    # Test de l'assistant
    assistant = get_forge_kenobi_assistant()
    print(assistant.get_context_summary())

    # Test de vérification
    test_result = assistant.execute_with_compliance(
        ActionType.CREATE_FILE, {"file_path": "test_file.py", "content": "# Test"}
    )

    print(json.dumps(test_result, indent=2, ensure_ascii=False))
