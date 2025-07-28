# Configuration ETL DevSecOps ONCF

Ce dossier contient les fichiers de configuration pour le projet ETL DevSecOps ONCF.

## 📋 Fichiers

- `settings.toml.example` : Fichier d'exemple avec toutes les options de configuration
- `settings.toml` : Configuration réelle (non versionnée, créée localement)

## 🚀 Usage

### 1. Configuration initiale

```bash
# Copier le fichier d'exemple
cp config/settings.toml.example config/settings.toml

# Adapter les valeurs selon votre environnement
vim config/settings.toml
```

### 2. Variables d'environnement prioritaires

Les variables d'environnement ont la priorité sur le fichier de configuration :

```bash
export GITLAB_URL="https://gitlab.oncf.net"
export GITLAB_TOKEN="your_personal_access_token"
```

### 3. US-001 - Test connexion GitLab

Pour US-001, seules ces variables sont nécessaires :
- `GITLAB_URL` : URL de l'instance GitLab ONCF
- `GITLAB_TOKEN` : Token d'accès personnel GitLab

## 🔒 Sécurité

⚠️ **IMPORTANT** : 
- Ne jamais committer `settings.toml` avec des tokens/passwords
- Utiliser les variables d'environnement pour les secrets
- Le fichier `settings.toml` est dans `.gitignore`

## 🏗️ Architecture

```
config/
├── settings.toml.example  # Template de configuration (versionné)
├── settings.toml         # Configuration locale (non versionné)
└── README.md            # Cette documentation
```

## 🌍 Environnements

Le fichier supporte plusieurs environnements :
- `development` : Configuration de développement
- `testing` : Configuration pour les tests
- `production` : Configuration production ONCF
