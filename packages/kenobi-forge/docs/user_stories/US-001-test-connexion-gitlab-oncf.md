# US-001 – Test de connexion à GitLab ONCF

## En tant que
Développeur ETL DevSecOps

## Je veux
Pouvoir tester et valider la connexion à la plateforme GitLab ONCF avec authentification sécurisée

## Pour
M'assurer que l'infrastructure ETL peut communiquer avec GitLab ONCF avant d'implémenter les extracteurs de données

## Critères d'acceptation
- [ ] La connexion à l'API GitLab ONCF s'établit avec succès via token d'authentification
- [ ] Le test de connexion répond en moins de 5 secondes
- [ ] Les informations de base de l'utilisateur connecté sont récupérées (nom, email, permissions)
- [ ] En cas d'échec de connexion, un message d'erreur explicite est retourné
- [ ] Les logs de connexion respectent les standards de sécurité (pas de token en clair)
- [ ] Le test peut être exécuté depuis l'environnement de développement et CI/CD

## Spécifications techniques
- **API Endpoint**: GitLab ONCF instance URL + `/api/v4/user`
- **Authentification**: Token privé GitLab (variable d'environnement)
- **Timeout**: 5 secondes maximum
- **Logging**: Niveau INFO pour succès, ERROR pour échecs
- **Architecture**: Utiliser `packages/etl-core/etl/extractors/gitlab/`

## Définition de "Terminé"
- [ ] Fonction `test_gitlab_oncf_connection()` implémentée
- [ ] Tests unitaires couvrant succès et échecs
- [ ] Documentation des variables d'environnement requises
- [ ] Intégration dans le CLI ETL (`etl-cli test-gitlab`)
- [ ] Validation par l'équipe DevSecOps ONCF

## Estimation
**Story Points**: 3  
**Durée estimée**: 0.5 jour

## Dépendances
- Accès à l'instance GitLab ONCF
- Token d'authentification avec permissions appropriées
- Configuration des variables d'environnement

---
*Créé le 28/07/2025 selon spécifications SPARCTER v1.4.0*
