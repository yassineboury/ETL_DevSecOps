# ETL DevSecOps

## Description

Monorepo ETL (Extract, Transform, Load) avec approche DevSecOps incluant Kenobi-Forge pour l'automatisation et la gestion des pipelines de données.

## Architecture Monorepo

Ce projet utilise une architecture **monorepo** pour une gestion unifiée des composants ETL et Kenobi-Forge.

```
ETL_DevSecOps/
├── 📁 packages/                    # Modules principaux
│   ├── 🔧 etl-core/               # Module ETL principal
│   ├── ⚡ kenobi-forge/           # Générateur de code et templates
│   └── 🔗 shared/                 # Utilitaires partagés
├── 📚 docs/                       # Documentation globale
├── ⚙️ scripts/                    # Scripts d'automatisation
├── 🔧 config/                     # Configuration globale
├── 🐳 .github/                    # CI/CD et workflows
└── 📄 Makefile                    # Commandes de gestion
```

## 🚀 Démarrage rapide

### Installation complète
```bash
# Configuration automatique de l'environnement
make setup

# Ou voir toutes les commandes disponibles
make help
```

### Commandes principales
```bash
make setup          # Installation complète
make test           # Tests tous modules
make lint           # Vérification qualité code
make build          # Build tous les modules
make clean          # Nettoyage
```

### Développement par module
```bash
make dev-etl        # Mode dev ETL Core
make dev-kenobi     # Mode dev Kenobi-Forge
make status         # Statut du monorepo
```

## 📖 Documentation

- [**Architecture**](docs/ARCHITECTURE.md) - Architecture détaillée du monorepo
- [**ETL Core**](packages/etl-core/README.md) - Module de traitement des données
- [**Kenobi-Forge**](packages/kenobi-forge/README.md) - Générateur de code
- [**Shared**](packages/shared/README.md) - Utilitaires communs

## 🛠️ Technologies

- **ETL Core** : Python, Pandas, SQLAlchemy, Apache Airflow
- **Kenobi-Forge** : Jinja2, Click, YAML, Templates
- **DevSecOps** : GitHub Actions, SonarQube, Docker
- **Qualité** : Black, Flake8, Pytest, MyPy

## 🔄 Workflow de développement

1. **Feature branch** depuis `develop`
2. **Développement** dans le module concerné
3. **Tests** : `make test`
4. **Quality check** : `make lint`
5. **PR** vers `develop`
6. **Merge** vers `main` pour release

## 🤝 Contribution

1. Consultez [ARCHITECTURE.md](docs/ARCHITECTURE.md) pour comprendre la structure
2. Utilisez `make setup` pour configurer votre environnement
3. Suivez les conventions de code (formatage automatique avec `make format`)
4. Ajoutez des tests pour toute nouvelle fonctionnalité

## 📜 License

À définir
