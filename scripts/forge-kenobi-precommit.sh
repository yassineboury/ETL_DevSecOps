#!/bin/bash
# Forge-Kenobi Pre-commit Hook
# Vérifie systématiquement la conformité aux spécifications avant chaque commit

set -e

echo "🤖 Forge-Kenobi Compliance Check..."

# Configuration
PROJECT_ROOT="$(git rev-parse --show-toplevel)"
KENOBI_ENGINE="$PROJECT_ROOT/packages/kenobi-forge/src/forge_kenobi_engine.py"

# Vérifier que Forge-Kenobi.md existe et est à jour
if [ ! -f "$PROJECT_ROOT/packages/kenobi-forge/FORGE-KENOBI.md" ]; then
    echo "❌ ERREUR: FORGE-KENOBI.md manquant !"
    echo "   Tous les développements doivent respecter les spécifications Forge-Kenobi"
    exit 1
fi

# Vérifier les spécifications de nommage (SPC-GEN-01)
echo "🔍 Vérification nommage des fichiers (SPC-GEN-01)..."
INVALID_FILES=$(find "$PROJECT_ROOT/packages" -name "*.py" -not -path "*/venv/*" -not -name "__init__.py" | while read file; do
    basename_file=$(basename "$file" .py)
    if ! echo "$basename_file" | grep -E '^[a-z][a-z0-9_]*[a-z0-9]$' > /dev/null; then
        echo "$file"
    fi
done)

if [ ! -z "$INVALID_FILES" ]; then
    echo "❌ Fichiers ne respectant pas snake_case (SPC-GEN-01):"
    echo "$INVALID_FILES"
    echo "   Renommez ces fichiers selon la convention snake_case"
    exit 1
fi

# Vérifier structure ETL obligatoire
echo "🏗️  Vérification architecture ETL..."
REQUIRED_DIRS=(
    "packages/etl-core/src/etl/core"
    "packages/etl-core/src/etl/extractors"
    "packages/etl-core/src/etl/transformers" 
    "packages/etl-core/src/etl/loaders"
)

for dir in "${REQUIRED_DIRS[@]}"; do
    if [ ! -d "$PROJECT_ROOT/$dir" ]; then
        echo "❌ Architecture ETL incomplète: $dir manquant"
        echo "   Créez la structure selon FORGE-KENOBI.md"
        exit 1
    fi
done

# Vérifier que les commits suivent Conventional Commits
COMMIT_MSG_FILE="$1"
if [ -f "$COMMIT_MSG_FILE" ]; then
    COMMIT_MSG=$(cat "$COMMIT_MSG_FILE")
    if ! echo "$COMMIT_MSG" | grep -E '^(feat|fix|docs|style|refactor|test|chore)(\(.+\))?: .+' > /dev/null; then
        echo "❌ Message de commit non conforme aux Conventional Commits"
        echo "   Format requis: type(scope): description"
        echo "   Exemple: feat(etl): add gitlab extractor"
        exit 1
    fi
fi

# Si le moteur de conformité existe, l'exécuter
if [ -f "$KENOBI_ENGINE" ]; then
    echo "🤖 Exécution du moteur de conformité complet..."
    cd "$PROJECT_ROOT"
    if command -v python3 > /dev/null; then
        python3 "$KENOBI_ENGINE" --check-only --project-root "$PROJECT_ROOT"
        COMPLIANCE_EXIT_CODE=$?
        if [ $COMPLIANCE_EXIT_CODE -ne 0 ]; then
            echo "❌ Échec de conformité Forge-Kenobi"
            echo "   Corrigez les erreurs avant de committer"
            exit 1
        fi
    fi
fi

echo "✅ Conformité Forge-Kenobi validée !"
echo "🚀 Commit autorisé"
