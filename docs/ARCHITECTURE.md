# Architecture Monorepo ETL DevSecOps

## Vue d'ensemble

Ce repository utilise une architecture **monorepo** pour héberger à la fois les composants ETL et Kenobi-Forge, permettant une gestion unifiée des dépendances, des versions et des déploiements.

## Structure recommandée

```
ETL_DevSecOps/
├── README.md                           # Documentation principale
├── .gitignore                         # Ignores globaux
├── .github/                           # GitHub workflows et templates
│   ├── workflows/                     # CI/CD pipelines
│   │   ├── etl-ci.yml                # Pipeline ETL
│   │   ├── kenobi-ci.yml             # Pipeline Kenobi-Forge
│   │   └── integration-tests.yml      # Tests d'intégration
│   └── ISSUE_TEMPLATE/               # Templates d'issues
├── docs/                             # Documentation globale
│   ├── ARCHITECTURE.md               # Ce fichier
│   ├── CONTRIBUTING.md               # Guide de contribution
│   └── DEPLOYMENT.md                 # Guide de déploiement
├── scripts/                          # Scripts globaux
│   ├── setup.sh                     # Setup environnement complet
│   ├── build-all.sh                 # Build tous les modules
│   └── deploy.sh                    # Déploiement global
├── config/                           # Configuration globale
│   ├── .env.example                 # Variables d'environnement
│   └── docker-compose.yml           # Orchestration locale
├── packages/                         # Modules principaux
│   ├── etl-core/                    # Module ETL principal
│   │   ├── etl/                     # Code source ETL (structure FORGE-KENOBI.md)
│   │   │   ├── core/               # Domain Layer (config, logging, errors, models)
│   │   │   ├── extractors/         # Infrastructure Layer (gitlab, sonar, dtrack, dojo)
│   │   │   ├── transformers/       # Application Layer (dates, agrégation, colonnes)
│   │   │   ├── loaders/           # Infrastructure Layer (excel_loader)
│   │   │   └── cli.py             # Interface Layer - Entry point
│   │   ├── tests/                  # Tests ETL
│   │   │   ├── unit/              # Tests unitaires (< 1s, pas I/O)
│   │   │   ├── integration/       # Tests d'intégration (mocks HTTP)
│   │   │   └── e2e/               # Tests end-to-end (nightly)
│   │   ├── pyproject.toml         # Configuration Poetry ≥1.8
│   │   └── README.md              # Documentation module
│   ├── kenobi-forge/              # Module Kenobi-Forge
│   │   ├── src/                   # Code source Kenobi
│   │   ├── docs/                  # Documentation Kenobi
│   │   │   ├── specs/             # Spécifications (SPC-GEN-XX)
│   │   │   └── user_stories/      # User stories
│   │   ├── olds/                  # Anciennes versions
│   │   ├── requirements.txt       # Dépendances Kenobi-Forge
│   │   └── FORGE-KENOBI.md       # Spécifications principales
│   └── shared/                    # Utilitaires partagés
│       ├── src/shared/            # Code source partagé
│       │   ├── models/            # Modèles de données communs
│       │   ├── utils/             # Fonctions utilitaires
│       │   ├── config/            # Configuration partagée
│       │   └── exceptions/        # Exceptions personnalisées
│       ├── requirements.txt       # Dépendances Shared
│       └── README.md              # Documentation module
├── tools/                          # Outils de développement
│   ├── linting/                   # Configuration linting
│   ├── testing/                   # Outils de test
│   └── monitoring/                # Outils de monitoring
└── examples/                       # Exemples d'utilisation
    ├── basic-etl/                 # Exemple ETL simple
    └── kenobi-integration/        # Exemple intégration
```

## Avantages de cette architecture

### 1. **Séparation claire des responsabilités**
- **ETL Core** : Logique métier ETL
- **Kenobi-Forge** : Génération de code et templates
- **Shared** : Code réutilisable entre modules

### 2. **Gestion unifiée**
- Un seul repository à maintenir
- Versions synchronisées
- CI/CD centralisé
- Documentation cohérente

### 3. **Développement efficace**
- Hot-reload entre modules
- Tests d'intégration simples
- Déploiement atomique

## Workflows recommandés

### Développement
1. Feature branch depuis `develop`
2. Développement dans le module concerné
3. Tests unitaires + intégration
4. PR vers `develop`
5. Merge vers `main` pour release

### CI/CD
- **Push sur feature branch** : Tests unitaires
- **PR vers develop** : Tests d'intégration
- **Merge vers main** : Déploiement automatique

## Technologies suggérées

### ETL Core
- **Python** : Logique ETL
- **Apache Airflow** : Orchestration
- **Pandas/Polars** : Traitement données
- **SQLAlchemy** : ORM base de données

### Kenobi-Forge
- **Python** : Générateur de templates
- **Jinja2** : Moteur de templates
- **Click** : CLI interface
- **YAML/JSON** : Configuration

### Outils DevSecOps
- **GitHub Actions** : CI/CD
- **SonarQube** : Qualité code
- **Snyk** : Sécurité
- **Docker** : Containerisation

## Scripts de gestion

Chaque module aura ses propres scripts mais des scripts globaux permettront :
- `make setup` : Installation complète
- `make test` : Tests tous modules
- `make build` : Build complet
- `make deploy` : Déploiement
