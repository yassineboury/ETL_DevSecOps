# US-001 – Extraction des projets GitLab

## En tant que
Chef de projet DevSecOps

## Je veux
Que l’application ETL récupère la liste complète des projets actifs depuis l’API GitLab (hors espaces personnels et projets archivés).

## Pour
Centraliser le pilotage et l’audit de l’activité de développement.

## Critères d’acceptation
- [ ] Tous les projets actifs (hors persos/archivés) sont extraits en moins de 30 s pour 200 projets.
- [ ] L’export Excel suit la convention de nommage du projet.
- [ ] En cas d’erreur d’API, l’échec est loggé et remonte dans la CI.
