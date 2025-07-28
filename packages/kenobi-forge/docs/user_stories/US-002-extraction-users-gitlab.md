# US-002 : Extraction des utilisateurs GitLab ONCF

## Contexte
Suite à la validation de la connexion GitLab (US-001), nous devons maintenant extraire les données utilisateurs de GitLab ONCF pour alimenter notre système ETL DevSecOps.

## Objectif
Développer un extracteur capable de récupérer la liste complète des utilisateurs GitLab ONCF avec leurs métadonnées associées.

## User Story
**En tant que** responsable DevSecOps ONCF  
**Je veux** extraire automatiquement les informations des utilisateurs GitLab  
**Afin de** constituer un référentiel centralisé des développeurs et analyser les patterns d'activité

## Critères d'acceptation

### ✅ Fonctionnalités principales
- [ ] Extraction complète des utilisateurs GitLab via API REST
- [ ] Récupération des métadonnées : id, username, name, state, created_at, last_activity_on, is_admin
- [ ] Support de la pagination pour gérer de grandes listes d'utilisateurs (300 max ONCF)
- [ ] Gestion des erreurs et retry automatique (3 tentatives : 1-4-9s selon SPC-GEN-05)
- [ ] Filtrage utilisateurs humains uniquement (pas de bots/comptes service)
- [ ] Transformation des données selon pipeline FORGE-KENOBI (Extract → Transform → Load)
- [ ] Export Excel conforme architecture FORGE-KENOBI Phase 1

### ✅ Critères techniques
- [ ] Respecter les limites de taux API GitLab (rate limiting)
- [ ] Authentification sécurisée par token
- [ ] Timeout 15 secondes par appel API
- [ ] Logs détaillés des opérations d'extraction (structlog JSON)
- [ ] Tests unitaires avec couverture ≥ 90% (standard FORGE-KENOBI)
- [ ] Documentation technique complète
- [ ] Intégration CLI dans etl/cli.py existant

### ✅ Critères qualité
- [ ] Code conforme aux standards Kenobi (Black, Flake8, isort, MyPy)
- [ ] Performance conforme standard FORGE-KENOBI : extraction utilisateurs ≤ 2 min (dérivé de ≤ 5 min / 100 projets)
- [ ] Gestion mémoire optimisée pour éviter les fuites
- [ ] Validation des données extraites (format email, dates JJ-MM-YYYY)
- [ ] Colonnes français format `gitlab_<metrique>_<unite>` selon SPC-GEN-01

## Spécifications techniques

### API GitLab utilisée
```bash
GET /api/v4/users?without_project_bots=true&per_page=100&page=1
GET /api/v4/users/:id (pour détails is_admin si nécessaire)
```

### Format de sortie Excel (conforme FORGE-KENOBI Phase 1)
```
Fichier: extracts/exports_28-07-2025/gitlab_utilisateurs_28-07-2025.xlsx

Feuille "Utilisateurs":
Colonnes (format <source>_<metric>_<unit>):
- gitlab_id_utilisateur
- gitlab_nom_utilisateur  
- gitlab_nom_complet
- gitlab_statut
- gitlab_date_creation (format JJ-MM-YYYY)
- gitlab_derniere_activite (format JJ-MM-YYYY)  
- gitlab_administrateur

Feuille "Metadonnees":
- horodatage_extraction: 28-07-2025 18:30:00
- gitlab_total_utilisateurs: 156
- gitlab_duree_extraction: 12.4
- gitlab_appels_api: 4
```

### Commande CLI (intégration etl/cli.py)
```bash
# Extraction basique vers Excel
python -m etl.cli extract-users --url https://gitlab.oncf.ma --token $GITLAB_TOKEN

# Avec options avancées
python -m etl.cli extract-users --url https://gitlab.oncf.ma --token $GITLAB_TOKEN \
  --output-dir extracts/custom --include-inactive --verbose
```

## Livrables
- [ ] Module `etl/extractors/gitlab/users_extractor.py` avec interface standard `fetch()` et `schema()`
- [ ] Module `etl/transformers/users_transformer.py` pour normalisation données selon SPC-GEN-01/02
- [ ] Tests unitaires `tests/unit/test_users_extractor.py` et `tests/unit/test_users_transformer.py`  
- [ ] Documentation technique dans README
- [ ] Intégration CLI mise à jour dans etl/cli.py
- [ ] Validation qualité complète (ruff, black, mypy, coverage ≥90%)

## Définition of Done
- [ ] Code pushé sur branche `feature/US-002-extraction-users-gitlab`
- [ ] Tous les tests passent (unitaires + intégration)  
- [ ] Pipeline CI/CD validé
- [ ] Code review effectué
- [ ] Documentation mise à jour
- [ ] Demo fonctionnelle réalisée

---
**Priorité:** Haute  
**Estimation:** 2 jours  
**Assigné:** DevSecOps Team  
**Sprint:** Sprint 2 - Juillet 2025
