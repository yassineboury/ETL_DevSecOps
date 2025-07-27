#!/usr/bin/env python3
"""
Forge-Kenobi Compliance Engine
Système de vérification automatique de conformité aux spécifications Forge-Kenobi
"""

import json
import re
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional


class ComplianceStatus(Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    WARNING = "WARNING"
    SKIP = "SKIP"


@dataclass
class ComplianceRule:
    """Règle de conformité Forge-Kenobi"""

    id: str
    title: str
    description: str
    category: str
    severity: str
    active: bool = True


@dataclass
class ComplianceResult:
    """Résultat de vérification d'une règle"""

    rule_id: str
    status: ComplianceStatus
    message: str
    details: Optional[Dict] = None


class ForgeKenobiEngine:
    """
    Moteur de conformité Forge-Kenobi

    Vérifie que tout code/structure respecte les spécifications définies
    dans FORGE-KENOBI.md et les documents associés.
    """

    def __init__(self, project_root: Path):
        self.project_root = Path(project_root)
        self.kenobi_config = self._load_kenobi_config()
        self.rules = self._load_compliance_rules()

    def _load_kenobi_config(self) -> Dict:
        """Charge la configuration depuis FORGE-KENOBI.md"""
        kenobi_file = (
            self.project_root / "packages" / "kenobi-forge" / "FORGE-KENOBI.md"
        )

        if not kenobi_file.exists():
            raise FileNotFoundError(f"FORGE-KENOBI.md not found at {kenobi_file}")

        with open(kenobi_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Extract framework tag
        framework_match = re.search(
            r"<!-- FRAMEWORK_TAG START -->(.*?)<!-- FRAMEWORK_TAG END -->",
            content,
            re.DOTALL,
        )
        if framework_match:
            framework_info = {}
            for line in framework_match.group(1).strip().split("\n"):
                if ":" in line:
                    key, value = line.split(":", 1)
                    framework_info[key.strip()] = value.strip()
            return framework_info

        return {}

    def _load_compliance_rules(self) -> List[ComplianceRule]:
        """Charge les règles de conformité depuis les spécifications"""
        rules = []

        # Règles de base depuis FORGE-KENOBI.md
        rules.extend(
            [
                ComplianceRule(
                    id="SPC-GEN-01",
                    title="Nommage global",
                    description="Fichiers snake_case, colonnes "
                    "<source>_<metric>_<unit>",
                    category="naming",
                    severity="ERROR",
                ),
                ComplianceRule(
                    id="SPC-GEN-02",
                    title="Format dates",
                    description="ISO/Epoch → UTC → JJ-MM-YYYY",
                    category="formatting",
                    severity="ERROR",
                ),
                ComplianceRule(
                    id="SPC-GEN-03",
                    title="Agrégation hebdo",
                    description="Semaine ISO lundi 00h UTC → dimanche 23h59 UTC",
                    category="aggregation",
                    severity="ERROR",
                ),
                ComplianceRule(
                    id="SPC-GEN-04",
                    title="Seuils CI",
                    description="Couverture ≥90%, Bandit MEDIUM+ KO, mypy 0 erreur",
                    category="quality",
                    severity="ERROR",
                ),
                ComplianceRule(
                    id="SPC-GEN-05",
                    title="Retry HTTP",
                    description="Codes 408,429,5xx → 3 retries (1-4-9s + jitter 10%)",
                    category="resilience",
                    severity="ERROR",
                ),
            ]
        )

        return rules

    def check_file_naming(self, file_path: Path) -> ComplianceResult:
        """Vérifie SPC-GEN-01 : nommage des fichiers"""
        if file_path.suffix == ".py":
            # Fichiers Python doivent être en snake_case
            name = file_path.stem
            if not re.match(r"^[a-z][a-z0-9_]*[a-z0-9]$", name) and name != "__init__":
                return ComplianceResult(
                    rule_id="SPC-GEN-01",
                    status=ComplianceStatus.FAIL,
                    message=f"Fichier {file_path.name} ne respecte pas snake_case",
                    details={"expected_pattern": "snake_case", "actual": name},
                )

        return ComplianceResult(
            rule_id="SPC-GEN-01",
            status=ComplianceStatus.PASS,
            message=f"Nommage conforme pour {file_path.name}",
        )

    def check_project_structure(self) -> List[ComplianceResult]:
        """Vérifie la structure du projet selon l'architecture Forge-Kenobi"""
        results = []

        # Vérifier présence des dossiers obligatoires pour ETL
        etl_required_dirs = [
            "packages/etl-core/etl/core",
            "packages/etl-core/etl/extractors",
            "packages/etl-core/etl/transformers",
            "packages/etl-core/etl/loaders",
            "packages/etl-core/tests/unit",
            "packages/etl-core/tests/integration",
        ]

        for required_dir in etl_required_dirs:
            dir_path = self.project_root / required_dir
            if not dir_path.exists():
                results.append(
                    ComplianceResult(
                        rule_id="ARCH-001",
                        status=ComplianceStatus.FAIL,
                        message=f"Dossier obligatoire manquant: {required_dir}",
                        details={"missing_directory": required_dir},
                    )
                )
            else:
                results.append(
                    ComplianceResult(
                        rule_id="ARCH-001",
                        status=ComplianceStatus.PASS,
                        message=f"Structure conforme: {required_dir}",
                    )
                )

        return results

    def check_coding_conventions(self, file_path: Path) -> List[ComplianceResult]:
        """Vérifie les conventions de codage"""
        results = []

        if file_path.suffix == ".py" and file_path.exists():
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Vérifier présence docstrings pour classes/fonctions
            class_pattern = r"class\s+\w+.*?:"
            function_pattern = r"def\s+\w+.*?:"

            classes = re.findall(class_pattern, content)
            functions = re.findall(function_pattern, content)

            if classes or functions:
                # Vérifier présence de docstrings
                docstring_pattern = r'""".*?"""'
                docstrings = re.findall(docstring_pattern, content, re.DOTALL)

                if len(docstrings) < len(classes) + len(functions):
                    results.append(
                        ComplianceResult(
                            rule_id="CODE-DOC-01",
                            status=ComplianceStatus.WARNING,
                            message=f"Docstrings manquantes dans {file_path.name}",
                            details={
                                "classes_count": len(classes),
                                "functions_count": len(functions),
                                "docstrings_count": len(docstrings),
                            },
                        )
                    )

        return results

    def run_full_compliance_check(self) -> Dict[str, Any]:
        """Exécute une vérification complète de conformité"""
        all_results = []

        # 1. Vérifier structure projet
        all_results.extend(self.check_project_structure())

        # 2. Vérifier nommage des fichiers Python
        for py_file in self.project_root.rglob("*.py"):
            if "venv" not in str(py_file) and ".git" not in str(py_file):
                all_results.append(self.check_file_naming(py_file))
                all_results.extend(self.check_coding_conventions(py_file))

        # 3. Compilation des résultats
        compliance_report = {
            "framework": self.kenobi_config.get("framework", "UNKNOWN"),
            "version": self.kenobi_config.get("version", "UNKNOWN"),
            "codename": self.kenobi_config.get("codename", "UNKNOWN"),
            "date": self.kenobi_config.get("date", "UNKNOWN"),
            "total_checks": len(all_results),
            "passed": len(
                [r for r in all_results if r.status == ComplianceStatus.PASS]
            ),
            "failed": len(
                [r for r in all_results if r.status == ComplianceStatus.FAIL]
            ),
            "warnings": len(
                [r for r in all_results if r.status == ComplianceStatus.WARNING]
            ),
            "results": [
                {
                    "rule_id": r.rule_id,
                    "status": r.status.value,
                    "message": r.message,
                    "details": r.details,
                }
                for r in all_results
            ],
        }

        return compliance_report

    def generate_compliance_report(self, output_file: Optional[Path] = None) -> Path:
        """Génère un rapport de conformité complet"""
        report = self.run_full_compliance_check()

        if output_file is None:
            output_file = self.project_root / "forge-kenobi-compliance-report.json"

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        return output_file


def main():
    """Point d'entrée CLI"""
    import argparse

    parser = argparse.ArgumentParser(description="Forge-Kenobi Compliance Engine")
    parser.add_argument(
        "--project-root", type=Path, default=".", help="Racine du projet"
    )
    parser.add_argument("--output", type=Path, help="Fichier de sortie pour le rapport")
    parser.add_argument(
        "--check-only", action="store_true", help="Affichage console uniquement"
    )

    args = parser.parse_args()

    # Détection automatique de la racine du monorepo
    current_path = Path.cwd()

    # Si on est dans packages/kenobi-forge/src, remonter à la racine
    if current_path.name == "src" and current_path.parent.name == "kenobi-forge":
        project_root = current_path.parent.parent.parent
    else:
        project_root = args.project_root

    engine = ForgeKenobiEngine(project_root)

    if args.check_only:
        report = engine.run_full_compliance_check()
        print("🔍 Forge-Kenobi Compliance Check")
        print(f"Framework: {report['framework']} v{report['version']}")
        print(f"✅ Passed: {report['passed']}")
        print(f"❌ Failed: {report['failed']}")
        print(f"⚠️  Warnings: {report['warnings']}")

        if report["failed"] > 0:
            print("\n❌ Échecs de conformité:")
            for result in report["results"]:
                if result["status"] == "FAIL":
                    print(f"  - {result['rule_id']}: {result['message']}")
    else:
        output_file = engine.generate_compliance_report(args.output)
        print(f"📊 Rapport de conformité généré: {output_file}")


if __name__ == "__main__":
    main()
