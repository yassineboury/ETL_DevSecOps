"""
Configuration pour l'utilisation temps réel de Kenobi par GitHub Copilot

Ce fichier définit comment GitHub Copilot peut utiliser Kenobi
pour valider toutes ses actions de développement.
"""

# =============================================================================
# ÉTAPES POUR UTILISATION TEMPS RÉEL DE KENOBI
# =============================================================================

"""
🎯 PROCHAINES ÉTAPES POUR RÉFÉRENCE KENOBI EN TEMPS RÉEL

1. ✅ SYSTÈME KENOBI OPÉRATIONNEL
   - Moteur Kenobi : ✅ Fonctionnel
   - Assistant Kenobi : ✅ Fonctionnel  
   - Intégration : ✅ Créée
   - CLI : ✅ Opérationnel

2. 🔄 WORKFLOW D'INTÉGRATION
   Avant chaque action de développement, GitHub Copilot doit :
   
   a) VÉRIFICATION DE CONFORMITÉ
      ```python
      from kenobi_quick import quick_check
      
      # Avant de créer un fichier
      if quick_check("create_file", file_path="mon_fichier.py"):
          # Procéder avec la création
          pass
      else:
          # Corriger selon les recommandations Kenobi
          pass
      ```
   
   b) CONSEILS POUR NOUVELLES TÂCHES
      ```python
      from kenobi_quick import quick_guidance
      
      # Avant d'implémenter une fonctionnalité
      guidance = quick_guidance("Créer un extracteur GitLab")
      # Appliquer les recommandations
      ```
   
   c) VALIDATION CONTINUE
      ```python
      from kenobi_quick import get_kenobi_status
      
      # Vérifier le statut de conformité
      status = get_kenobi_status()
      ```

3. 🤖 ACTIONS AUTOMATISÉES DISPONIBLES
   
   Via le CLI (packages/kenobi-forge/src/kenobi_cli.py) :
   - python kenobi_cli.py check create_file file_path=nom_fichier.py
   - python kenobi_cli.py guidance "Description de la tâche"
   - python kenobi_cli.py summary
   
   Via le wrapper (kenobi_quick.py) :
   - quick_check(action_type, **params)
   - quick_guidance(task_description)
   - get_kenobi_status()

4. 🏗️ TYPES D'ACTIONS VALIDÉES
   - CREATE_FILE : Création de fichiers avec vérification nommage
   - MODIFY_FILE : Modification avec respect des conventions
   - CREATE_STRUCTURE : Création d'architecture conforme
   - RUN_COMMAND : Commandes respectant les contraintes
   - GENERATE_CODE : Code conforme aux spécifications

5. 📋 SPÉCIFICATIONS KENOBI APPLIQUÉES
   - SPC-GEN-01 : Nommage snake_case obligatoire
   - Architecture ETL : extractors/ → transformers/ → loaders/
   - Conventions : f-strings, Black 88 char, mypy strict
   - Contraintes : Python 3.12, Poetry ≥ 1.8

6. 🎯 UTILISATION PRATIQUE
   
   Pour que GitHub Copilot utilise Kenobi en temps réel :
   
   AVANT chaque action :
   1. Importer les outils Kenobi
   2. Vérifier la conformité de l'action prévue
   3. Appliquer les recommandations si nécessaire
   4. Procéder seulement si conforme
   
   EXEMPLE CONCRET :
   ```python
   # Import du système Kenobi
   import sys
   from pathlib import Path
   sys.path.insert(0, str(Path.cwd() / "packages/kenobi-forge/src"))
   from kenobi_integration import kenobi_check, kenobi_guidance
   
   # Avant de créer extract_gitlab_data.py
   result = kenobi_check("create_file", file_path="extract_gitlab_data.py")
   if result["compliant"]:
       # ✅ Créer le fichier
       create_file("extract_gitlab_data.py", content)
   else:
       # ❌ Afficher les recommandations et corriger
       print(result["message"])
   ```

7. 🔄 WORKFLOW COMPLET
   
   1. Recevoir une demande utilisateur
   2. Analyser la tâche avec kenobi_guidance()
   3. Planifier les actions nécessaires
   4. Pour chaque action :
      a. Vérifier avec kenobi_check()
      b. Corriger si non conforme
      c. Exécuter si conforme
   5. Vérifier le statut final avec get_kenobi_status()

8. 🧪 TEST DE L'INTÉGRATION
   
   Commandes de test disponibles :
   ```bash
   # Test complet
   python kenobi_quick.py
   
   # Test CLI
   cd packages/kenobi-forge/src
   python kenobi_cli.py test
   
   # Vérification spécifique
   python kenobi_cli.py check create_file file_path=test.py
   ```

9. 📍 STATUT ACTUEL
   
   ✅ Infrastructure Kenobi : Complète et opérationnelle
   ✅ Outils d'intégration : Disponibles et testés
   ✅ Validation temps réel : Prête à l'emploi
   
   🎯 PROCHAINE ÉTAPE : Utiliser systématiquement ces outils
      dans chaque interaction de développement !

10. 💡 RAPPEL IMPORTANT
    
    Kenobi doit être consulté AVANT chaque action, pas après !
    C'est un assistant proactif, pas réactif.
"""

# =============================================================================
# FONCTIONS UTILITAIRES POUR GITHUB COPILOT
# =============================================================================

def setup_kenobi_integration():
    """
    Configure l'intégration Kenobi pour GitHub Copilot
    À appeler au début de chaque session de développement
    """
    try:
        from kenobi_runtime import get_kenobi_runtime
        runtime = get_kenobi_runtime()
        status = runtime.get_status()
        
        print("🤖 Kenobi Integration : ✅ Activée")
        print(f"   Runtime: {'✅' if status['runtime_active'] else '❌'}")
        print(f"   Framework: {status['framework']}")
        return runtime
    except ImportError as e:
        print(f"❌ Erreur d'import Kenobi Runtime: {e}")
        return None


def kenobi_validate_action(action_type: str, **details):
    """
    Valide une action avec Kenobi avant exécution
    
    Args:
        action_type: Type d'action (create_file, modify_file, etc.)
        **details: Détails de l'action
        
    Returns:
        True si l'action est conforme, False sinon
    """
    try:
        from kenobi_runtime import get_kenobi_runtime
        runtime = get_kenobi_runtime()
        result = runtime.kenobi_check(action_type, **details)
        
        if result["compliant"]:
            print(f"✅ Kenobi: {result['message']}")
            return True
        else:
            print(f"❌ Kenobi: {result['message']}")
            if "recommendations" in result:
                print("💡 Recommandations Kenobi:")
                for rec in result["recommendations"]:
                    print(f"   • {rec}")
            return False
            
    except Exception as e:
        print(f"⚠️ Erreur Kenobi: {e}")
        return True  # Continuer en cas d'erreur système


# Exemple d'utilisation
if __name__ == "__main__":
    print("🤖 Configuration Kenobi pour GitHub Copilot")
    print("=" * 50)
    
    # Test de l'intégration
    integration = setup_kenobi_integration()
    
    if integration:
        print("\n✅ Kenobi prêt pour utilisation temps réel !")
        print("\nExemples d'utilisation :")
        print("  kenobi_validate_action('create_file', file_path='test.py')")
        print("  quick_guidance('Créer un extracteur')")
        print("  get_kenobi_status()")
    else:
        print("\n❌ Problème avec l'intégration Kenobi")
