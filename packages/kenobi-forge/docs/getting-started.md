# Getting Started - Kenobi‑Forge ETL

Ce guide vous accompagne dans la prise en main du projet **Kenobi‑Forge**, l'ETL DevSecOps qui centralise les métriques GitLab, SonarQube, Dependency‑Track et DefectDojo.

## 🎯 Prérequis

### Environnement technique
- **Python 3.12.x** (obligatoire pour la compatibilité)
- **Poetry ≥ 1.8** pour la gestion des dépendances
- **Windows 11 64‑bit** + SSD NVMe (environnement cible)
- **≥ 4 vCPU / 16 Go RAM** pour les performances
- **Git** configuré avec accès au dépôt

### Accès & tokens
- Token GitLab avec scope `read_api` 
- Token SonarQube (si applicable)
- Token Dependency‑Track (si applicable)
- Token DefectDojo (si applicable)

## 🚀 Installation rapide

### 1. Cloner et installer
```bash
git clone <repo-url> kenobi-forge
cd kenobi-forge
poetry install --no-root
```

### 2. Configuration
```bash
# Copier le template de configuration
cp config/settings.toml.example config/settings.toml

# Éditer avec vos tokens (JAMAIS dans le dépôt!)
code config/settings.toml
```

### 3. Vérification de l'installation
```bash
# Lancer la CI locale
make ci

# Test rapide
poetry run python -m etl.cli --help
```

## 📋 Structure du projet

```
kenobi-forge/
├── etl/                     # Code source principal
│   ├── core/                # Configuration, logging, erreurs
│   ├── extractors/          # GitLab, SonarQube, DTrack, DefectDojo
│   ├── transformers/        # Normalisation dates, agrégations
│   ├── loaders/             # Export Excel (Phase 1)
│   └── cli.py               # Point d'entrée
├── tests/                   # Tests unitaires, intégration, e2e
├── docs/                    # Documentation & spécifications
├── config/                  # Fichiers de configuration
└── extracts/                # Dossier de sortie (auto-créé)
```

## 🏃‍♂️ Premier run

### 1. Configuration minimale
Éditez `config/settings.toml` :
```toml
[gitlab]
url = "https://gitlab.example.com"
token = "glpat-xxxxxxxxxxxxxxxxxxxx"

[export]
quota_gb = 10
base_path = "extracts"

[logging]
level = "INFO"
format = "json"
```

### 2. Lancer une extraction GitLab
```bash
# Mode debug pour commencer
LOG_LEVEL=DEBUG poetry run python -m etl.cli extract --source gitlab --limit 10

# Run complet (attention: peut prendre du temps!)
poetry run python -m etl.cli run
```

### 3. Vérifier les outputs
```bash
ls -la extracts/exports_$(date +%d-%m-%Y)/
```

## 🔧 Commandes essentielles

### Développement
```bash
make format          # Black + ruff formatting
make lint            # Vérifications qualité
make test            # Tests unitaires + couverture
make ci              # Pipeline complète locale
```

### ETL
```bash
# Extraction par source
poetry run python -m etl.cli extract --source gitlab
poetry run python -m etl.cli extract --source sonar

# Pipeline complet
poetry run python -m etl.cli run

# Nettoyage des anciens exports
poetry run python -m etl.cli purge --dry-run
```

### Monitoring
```bash
# Vérifier les logs
tail -f logs/etl.log

# Statut des derniers runs
poetry run python -m etl.cli status

# Vérifier les checksums
make verify_exports
```

## 📊 Comprendre les outputs

### Structure des exports
```
extracts/exports_DD-MM-YYYY/
├── gitlab_projects_DD-MM-YYYY.xlsx      # Projets GitLab
├── gitlab_pipelines_DD-MM-YYYY.xlsx     # Pipelines CI/CD
├── sonar_metrics_DD-MM-YYYY.xlsx        # Métriques qualité
└── .sha256                              # Checksums de vérification
```

### Format des colonnes
Convention : `<source>_<metric>_<unit>`
- `gitlab_pipeline_duration_sec` : Durée pipeline en secondes
- `sonar_critical_vuln_count` : Nombre vulnérabilités critiques
- `week_id` : Semaine ISO au format `YYYY-WW`

## 🐛 Debugging courant

### Problèmes d'API
```bash
# Tester la connectivité GitLab
curl -H "PRIVATE-TOKEN: <token>" https://gitlab.example.com/api/v4/projects

# Vérifier les rate limits
grep "429" logs/etl.log
```

### Problèmes de performance
```bash
# Activer le profiling
PROFILE=true poetry run python -m etl.cli run

# Réduire le scope pour debug
poetry run python -m etl.cli extract --source gitlab --limit 5 --since 2025-07-01
```

### Erreurs de CI
```bash
# Logs détaillés des échecs
ls -la failed_jobs/

# Re-run après correction
make ci && echo "✅ CI OK" || echo "❌ CI KO"
```

## 📚 Documentation avancée

### Pour approfondir
- [`FORGE-KENOBI.md`](../FORGE-KENOBI.md) : Spécification complète du projet
- [`docs/specs/`](specs/) : Spécifications techniques détaillées
- [`docs/user_stories/`](user_stories/) : User stories et critères d'acceptation

### Développement
- [`docs/adr/`](adr/) : Architecture Decision Records (à créer)
- Tests : Voir `tests/README.md` pour les conventions
- CI/CD : Pipeline définie dans `.gitlab-ci.yml`

## 🆘 Support & escalade

### Auto-diagnostic
1. `make ci` passe-t-elle ? 
2. Les tokens sont-ils valides ?
3. Y a-t-il assez d'espace disque (`df -h`) ?
4. Les APIs externes sont-elles accessibles ?

### Escalade
- **Issues rapides** : Créer une issue GitLab avec label `question`
- **Blocage technique** : Mentionner `@team-lead` dans l'issue
- **Urgence** : Protocole défini dans `FORGE-KENOBI.md` section `clarification_protocol`

---

## 🎉 Félicitations !

Vous êtes maintenant prêt à contribuer au projet Kenobi‑Forge. N'hésitez pas à consulter les user stories dans `docs/user_stories/` pour comprendre les besoins métier.

**Prochaines étapes suggérées :**
1. Lire [`US-001-extraction-gitlab.md`](user_stories/US-001-extraction-gitlab.md)
2. Examiner le code source dans `etl/extractors/gitlab/`
3. Lancer votre premier test d'extraction sur un petit scope

Bon développement ! 🚀
