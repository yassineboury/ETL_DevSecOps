# ETL Core

ETL Core module conforme aux spécifications FORGE-KENOBI.md

## Structure

Respecte l'architecture Clean Architecture + DDD selon FORGE-KENOBI.md :

```
etl/
├── core/             # Domain Layer (config, logging, errors, models)
├── extractors/       # Infrastructure Layer (GitLab, SonarQube, Dependency-Track, DefectDojo)
├── transformers/     # Application Layer (dates, agrégation, colonnes)
├── loaders/          # Infrastructure Layer (Excel Phase 1)
└── cli.py            # Interface Layer - Entry point
```

## Spécifications conformes

- **SPC-GEN-01**: Nommage snake_case
- **SPC-GEN-02**: Dates ISO/Epoch → JJ-MM-YYYY  
- **SPC-GEN-03**: Agrégation hebdomadaire ISO
- **SPC-GEN-04**: Seuils CI ≥90%
- **SPC-GEN-05**: Retry HTTP 1-4-9s

## Installation

```bash
# Mode développement depuis racine monorepo
make dev-etl
```
