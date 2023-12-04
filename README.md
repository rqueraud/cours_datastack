# TP - Outils pour la Data
## Trinôme : Boin Alexandre, Veillat Lisa & Vovard Marine

```bash
echo -e "AIRFLOW_UID=$(id -u)" > .env
chown -R $(whoami) ./airflow/*

docker compose pull
docker compose up -d --build
```

Plusieurs urls : 
* Airflow : http://localhost:8080 avec identifiants airflow/airflow
* MinIO : http://localhost:9000 avec identifiants minioadmin/minioadmin
* RabbitMQ : http://localhost:15672 avec identifiants guest/guest


## Instructions de démonstration
0. Créer un fichier .env et donner les bons droits sur le répertoire `airflow`:
```bash
echo -e "AIRFLOW_UID=$(id -u)" > .env
chown -R $(whoami) ./airflow/*
```
1. Télécharger le fichier `service-account.json` dans le dossier `airflow/config`
2. Télécharger le fichier `Posts.json` dans le dossier `airflow/data/movies-stackexchange`
3. Lancer `build.sh`
4. Lancer la commande `docker compose up -d --build`
5. Attendre que les containers soient lancés (compter environ 5 minutes)
6. Le DAG `DAG_install_dependencies` se lance (soit automatiquement la première fois, soit à lancer manuellement ensuite), les dépendances Python pour les DAGs suivants sont installées
7. À la fin de l'installation, le DAG `DAG_ingest_users` se lance, le fichier `Users.json` est lu et l'ensemble des utilisateurs sont stockés dans la collection `users` de la base de données `movies-stackexchange` de MongoDB (visible via Compass)
8. À intervalle réguliser, le DAG `DAG_stackexchange_posts` se lance, le fichier `Posts.json` est lu et un post est sélectionné aléatoirement pour être envoyé sur les files RabbitMQ "posts_to_minio" et "posts_to_mongodb".
9. Le script tournant dans le container `rabbit_to_minio` récupère le post et le stocke dans le bucket `posts` de MinIO (visible via l'interface web)
10. Le script tournant dans le container `rabbit_to_mongodb` récupère le post et le stocke dans la collection `posts` de la base de données `movies-stackexchange` de MongoDB (visible via Compass)
11. À intervalle réguliser, le DAG `DAG_mongo_to_bigquery` se lance, va effectuer une aggrégation du nombre de posts par utilisateur et va stocker le résultat dans la table `posts_count` du dataset `posts` de BigQuery (visible via l'interface web)
12. À intervalle réguliser, le DAG `DAG_mongo_to_bigquery_user` se lance, va effectuer une aggrégation des utilisateurs pour obtenir la date de leur denier post et va stocker le résultat dans la table `users_last_post` du dataset `users` de BigQuery (visible via l'interface web)