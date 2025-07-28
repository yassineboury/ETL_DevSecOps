"""
Exceptions métier DDD selon FORGE-KENOBI.md
Module centralisé pour toutes les exceptions ETL DevSecOps.
"""


class ETLError(Exception):
    """Exception racine pour tous les erreurs ETL."""

    pass


class ConfigurationError(ETLError):
    """Erreur de configuration ETL."""

    pass


class ExtractorError(ETLError):
    """Erreur lors de l'extraction de données."""

    pass


class TransformerError(ETLError):
    """Erreur lors de la transformation de données."""

    pass


class LoaderError(ETLError):
    """Erreur lors du chargement de données."""

    pass
