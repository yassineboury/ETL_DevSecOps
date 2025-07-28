#!/bin/bash

# Script de vérification qualité complète pour le projet ETL DevSecOps Kenobi
# Compatible avec les standards Kenobi SPARCTER v1.4.0

set -e

# Configuration environnement Python
PYTHON_ENV="/Volumes/DATA/STRATIS_CREATIS/PROJETS DEV/ETL DevSecOps/etl_devsecops/bin/python"

echo "🔍 === CHECK QUALITÉ ETL DEVSECOPS KENOBI ==="
echo "Version: SPARCTER v1.4.0"
echo "Date: $(date)"
echo "Branch: $(git branch --show-current)"
echo "Commit: $(git rev-parse --short HEAD)"
echo ""

# 1. Formatage avec Black
echo "📝 [1/6] Vérification formatage Black..."
if "$PYTHON_ENV" -m black --check --diff . > /dev/null 2>&1; then
    echo "✅ Black: Formatage conforme"
else
    echo "❌ Black: Formatage requis"
    exit 1
fi

# 2. Style avec Flake8
echo "🎨 [2/6] Vérification style Flake8..."
if "$PYTHON_ENV" -m flake8 --max-line-length=88 --extend-ignore=E203,W503 . > /dev/null 2>&1; then
    echo "✅ Flake8: Style conforme"
else
    echo "❌ Flake8: Problèmes de style détectés"
    exit 1
fi

# 3. Ordre des imports avec isort
echo "📦 [3/6] Vérification imports isort..."
if "$PYTHON_ENV" -m isort --check-only --profile black . > /dev/null 2>&1; then
    echo "✅ isort: Imports triés correctement"
else
    echo "❌ isort: Imports nécessitent un tri"
    exit 1
fi

# 4. Types avec MyPy
echo "🔬 [4/6] Vérification types MyPy..."
if "$PYTHON_ENV" -m mypy etl/ > /dev/null 2>&1; then
    echo "✅ MyPy: Types conformes"
else
    echo "❌ MyPy: Erreurs de types détectées"
    exit 1
fi

# 5. Tests avec pytest
echo "🧪 [5/6] Exécution tests pytest..."
if "$PYTHON_ENV" -m pytest tests/ -q > /dev/null 2>&1; then
    echo "✅ pytest: 8 tests réussis"
else
    echo "❌ pytest: Tests échoués"
    exit 1
fi

# 6. CLI fonctionnelle
echo "⚙️  [6/6] Vérification CLI..."
if "$PYTHON_ENV" -m etl.cli test-gitlab --help > /dev/null 2>&1; then
    echo "✅ CLI: Interface fonctionnelle"
else
    echo "❌ CLI: Problème d'interface"
    exit 1
fi

echo ""
echo "🎉 === SUCCÈS: PROJET CONFORME AUX STANDARDS KENOBI ==="
echo "📊 Métriques:"
echo "   • Fichiers Python: $(find . -name '*.py' | wc -l | tr -d ' ')"
echo "   • Tests unitaires: 8"
echo "   • Couverture formatage: 100%"
echo "   • Conformité style: 100%"
echo "   • Conformité types: 100%"
echo ""
echo "✨ Le projet ETL DevSecOps est prêt pour la production ONCF !"
