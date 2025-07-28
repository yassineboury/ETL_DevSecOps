#!/usr/bin/env python3
"""
Script utilitaire pour que GitHub Copilot utilise Kenobi en temps réel

Ce script me permet de :
1. Vérifier la conformité avant chaque action
2. Obtenir des conseils Kenobi pour mes tâches
3. Exécuter des actions avec validation automatique
"""

import json
import sys
from pathlib import Path

# Ajouter le chemin pour importer les modules Kenobi
sys.path.insert(0, str(Path(__file__).parent))

from kenobi_integration import (
    get_kenobi_integration,
    kenobi_check,
    kenobi_execute,
    kenobi_guidance,
)


def main():
    """Point d'entrée principal pour l'utilisation de Kenobi"""
    if len(sys.argv) < 2:
        print_usage()
        return

    command = sys.argv[1]

    if command == "check":
        handle_check_command()
    elif command == "execute":
        handle_execute_command()
    elif command == "guidance":
        handle_guidance_command()
    elif command == "summary":
        handle_summary_command()
    elif command == "test":
        handle_test_command()
    else:
        print(f"❌ Commande inconnue: {command}")
        print_usage()


def print_usage():
    """Affiche l'aide d'utilisation"""
    print(
        """
🤖 Kenobi CLI - Assistant Forge-Kenobi pour GitHub Copilot

Usage:
    python kenobi_cli.py <command> [args...]

Commandes:
    check <action_type> <details...>   - Vérifier conformité avant action
    execute <action_type> <details...> - Exécuter action avec validation
    guidance <task_description>        - Obtenir conseils pour une tâche
    summary                           - Résumé de la session Kenobi
    test                             - Test de l'intégration

Exemples:
    python kenobi_cli.py check create_file file_path=src/extract_gitlab.py
    python kenobi_cli.py guidance "Créer un extracteur GitLab"
    python kenobi_cli.py summary
    """
    )


def handle_check_command():
    """Gère la commande check"""
    if len(sys.argv) < 3:
        print("❌ Usage: kenobi_cli.py check <action_type> <key=value>...")
        return

    action_type = sys.argv[2]
    details = parse_details(sys.argv[3:])

    print(f"🔍 Vérification Kenobi pour action: {action_type}")
    result = kenobi_check(action_type, **details)

    print_json_result(result)

    if not result["compliant"]:
        print("\n💡 Recommandations:")
        for rec in result.get("recommendations", []):
            print(f"  • {rec}")


def handle_execute_command():
    """Gère la commande execute"""
    if len(sys.argv) < 3:
        print("❌ Usage: kenobi_cli.py execute <action_type> <key=value>...")
        return

    action_type = sys.argv[2]
    details = parse_details(sys.argv[3:])

    print(f"⚡ Exécution Kenobi pour action: {action_type}")
    result = kenobi_execute(action_type, **details)

    print_json_result(result)

    if result.get("success"):
        print("✅ Action exécutée avec succès !")
    else:
        print("❌ Échec de l'action")
        if "error" in result:
            print(f"Erreur: {result['error']}")


def handle_guidance_command():
    """Gère la commande guidance"""
    if len(sys.argv) < 3:
        print("❌ Usage: kenobi_cli.py guidance <task_description>")
        return

    task = " ".join(sys.argv[2:])

    print(f"💡 Conseils Kenobi pour: {task}")
    result = kenobi_guidance(task)

    print_json_result(result)

    if result.get("recommendations"):
        print("\n🎯 Recommandations spécifiques:")
        for rec in result["recommendations"]:
            print(f"  • {rec}")


def handle_summary_command():
    """Gère la commande summary"""
    print("📊 Résumé de session Kenobi")
    integration = get_kenobi_integration()
    summary = integration.get_session_summary()

    print_json_result(summary)


def handle_test_command():
    """Gère la commande test"""
    print("🧪 Test complet de l'intégration Kenobi")
    print("=" * 50)

    # Test 1: Vérification conforme
    print("\n1. Test fichier conforme:")
    result1 = kenobi_check("create_file", file_path="extract_gitlab_data.py")
    print(
        f"   Résultat: {'✅ Conforme' if result1['compliant'] else '❌ Non conforme'}"
    )

    # Test 2: Vérification non conforme
    print("\n2. Test fichier non conforme:")
    result2 = kenobi_check("create_file", file_path="BadFileName.py")
    print(
        f"   Résultat: {'✅ Conforme' if result2['compliant'] else '❌ Non conforme'}"
    )

    # Test 3: Conseils
    print("\n3. Test conseils:")
    guidance = kenobi_guidance("Créer un extracteur GitLab")
    print(
        f"   Spécifications applicables: {len(guidance.get('applicable_specifications', []))}"
    )
    print(f"   Recommandations: {len(guidance.get('recommendations', []))}")

    # Test 4: Résumé
    print("\n4. Test résumé:")
    integration = get_kenobi_integration()
    summary = integration.get_session_summary()
    print(f"   Actions totales: {summary['session_stats']['total_actions']}")

    print("\n✅ Tests terminés avec succès !")


def parse_details(args):
    """Parse les arguments en format key=value vers un dictionnaire"""
    details = {}
    for arg in args:
        if "=" in arg:
            key, value = arg.split("=", 1)
            details[key] = value
        else:
            # Argument sans valeur, l'ajouter avec True
            details[arg] = True
    return details


def print_json_result(result):
    """Affiche un résultat JSON de manière lisible"""
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
