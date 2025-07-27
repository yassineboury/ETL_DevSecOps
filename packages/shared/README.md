# Shared Utilities

Utilitaires et modèles partagés entre ETL Core et Kenobi-Forge.

## Structure

```
shared/
├── src/
│   └── shared/
│       ├── __init__.py
│       ├── models/         # Modèles de données communs
│       ├── utils/          # Fonctions utilitaires
│       ├── config/         # Configuration partagée
│       └── exceptions/     # Exceptions personnalisées
├── tests/
└── requirements.txt
```

## Contenu

- **Models** : Modèles Pydantic réutilisables
- **Utils** : Fonctions utilitaires (logging, validation, etc.)
- **Config** : Configuration centralisée
- **Exceptions** : Exceptions métier communes
