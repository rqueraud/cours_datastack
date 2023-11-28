# TP - Outils pour la Data

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
1. Télécharger le fichier `service-account.json` dans le dossier `airflow/config`
2. Télécharger le fichier `Posts.json` dans le dossier `airflow/data/movies-stackexchange`
3. Lancer la commande `docker compose up -d --build`
4. Attendre que les containers soient lancés (compter environ 5 minutes)
5. Le DAG `DAG_stackexchange_posts` se lance, le fichier `Posts.json` est lu et un post est sélectionné aléatoirement pour être envoyé sur les files RabbitMQ "posts_to_minio" et "posts_to_mongodb".
6. Le container `rabbit_to_minio` récupère le post et le stocke dans le bucket `posts` de MinIO (visible via l'interface web)
7. Le container `rabbit_to_mongodb` récupère le post et le stocke dans la collection `posts` de la base de données `movies-stackexchange` de MongoDB (visible via Compass)
8. Le DAG `DAG_mongo_to_bigquery` se lance, va effectuer une aggrégation du nombre de posts par utilisateur et va stocker le résultat dans la table `posts_count` du dataset `posts` de BigQuery (visible via l'interface web)