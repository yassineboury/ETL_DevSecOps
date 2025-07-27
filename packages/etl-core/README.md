# ETL Core Module

Module principal pour les opérations ETL (Extract, Transform, Load).

## Structure

```
etl-core/
├── src/
│   └── etl_core/
│       ├── __init__.py
│       ├── extractors/     # Extracteurs de données
│       ├── transformers/   # Transformateurs
│       ├── loaders/        # Chargeurs de données
│       └── pipelines/      # Pipelines ETL
├── tests/
├── docs/
├── requirements.txt
└── setup.py
```

## Installation en mode développement

```bash
# Depuis la racine du monorepo
make dev-etl

# Ou manuellement
cd packages/etl-core
pip install -e .
```

## Utilisation

```python
from etl_core.pipelines import DataPipeline

pipeline = DataPipeline()
pipeline.extract("source").transform("rules").load("destination")
```
