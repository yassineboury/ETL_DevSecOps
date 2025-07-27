# SPC‑001 – Nommage global (active)
**Version** : 1.0 **Owner** : devops@domaine.com

## Contexte
Garantir une homogénéité sur tous les artefacts (fichiers, colonnes, exports, etc.).

## Règles
1. Fichiers : snake_case ASCII, sans espace.
2. Colonnes : `<source>_<metric>_<unit>` (ex : `gitlab_pipeline_duration_sec`).
3. Identifiant semaine ISO : `YYYY‑WW` (ex : 2025‑30).

## Critères d’acceptation
- Générer un export le 25‑07‑2025 doit produire un fichier `gitlab_projects_25‑07‑2025.xlsx`.
