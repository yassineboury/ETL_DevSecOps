#!/usr/bin/env python3
"""
Wrapper rapide pour utiliser Kenobi en temps réel
Utilisation simple pour GitHub Copilot
"""

from kenobi_runtime import get_kenobi_runtime


def quick_check(action_type: str, **kwargs) -> bool:
    """
    Vérification rapide de conformité Kenobi
    
    Returns:
        True si conforme, False sinon
    """
    runtime = get_kenobi_runtime()
    result = runtime.kenobi_check(action_type, **kwargs)
    
    if result["compliant"]:
        print(f"✅ {result['message']}")
        return True
    else:
        print(f"❌ {result['message']}")
        if "recommendations" in result:
            print("💡 Recommandations:")
            for rec in result["recommendations"]:
                print(f"   • {rec}")
        return False


def quick_guidance(task: str) -> dict:
    """
    Conseils rapides Kenobi pour une tâche
    
    Returns:
        Dictionnaire avec les conseils
    """
    runtime = get_kenobi_runtime()
    guidance = runtime.kenobi_guidance(task)
    
    print(f"🎯 Conseils Kenobi pour: {task}")
    print("=" * 50)
    
    if guidance.get("recommendations"):
        print("📋 Recommandations:")
        for rec in guidance["recommendations"]:
            print(f"   • {rec}")
    
    print("\n🔤 Conventions de nommage:")
    for key, value in guidance["coding_conventions"].items():
        print(f"   • {key}: {value}")
    
    return guidance


def get_kenobi_status() -> dict:
    """
    Statut actuel de Kenobi
    
    Returns:
        Dictionnaire avec le statut
    """
    runtime = get_kenobi_runtime()
    status = runtime.get_status()
    
    print("📊 Statut Kenobi:")
    print(f"   Framework: {status['framework']}")
    print(f"   Runtime actif: {'✅' if status['runtime_active'] else '❌'}")
    print(f"   Kenobi disponible: {'✅' if status['kenobi_available'] else '❌'}")
    
    return status


if __name__ == "__main__":
    print("🤖 Wrapper Kenobi - Tests rapides")
    print("=" * 40)
    
    # Test 1: Fichier conforme
    print("\n1. Test fichier conforme:")
    quick_check("create_file", file_path="extract_gitlab_metrics.py")
    
    # Test 2: Fichier non conforme  
    print("\n2. Test fichier non conforme:")
    quick_check("create_file", file_path="BadNaming.py")
    
    # Test 3: Conseils
    print("\n3. Conseils pour extracteur:")
    quick_guidance("Créer extracteur GitLab")
    
    # Test 4: Statut
    print("\n4. Statut Kenobi:")
    get_kenobi_status()
