[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/rqueraud/cours_datastack/main)

Test the container with : 
```bash
docker build -t cours_datastack .
docker run -it --rm -p 8888:8888 cours_datastack jupyter notebook --NotebookApp.default_url=/lab/ --ip=0.0.0.0 --port=8888
```

Commandes à lancer pour démarrer les différents services : 
```bash
redis-server --daemonize yes  # Redis
MINIO_ROOT_USER=admin MINIO_ROOT_PASSWORD=password minio server /mnt/data --console-address ":9001" &  # MinIO
sudo mongod & # MongoDB
sudo rabbitmq-server & # RabbitMQ

# Localhost.run
ssh -R 80:localhost:9001 nokey@localhost.run  # minio ==> admin/password
ssh -R 80:localhost:15672 nokey@localhost.run  # rabbitmq ==> guest/guest

# Alternative en utilisant ngrok si besoin
export NGROK_TOKEN=<your_ngrok_token>
./ngrok config add-authtoken $NGROK_TOKEN
./ngrok http 9001  # En utilisant ngrok si besin

# Alternative en utilisant pyjamas si besoin
curl https://tunnel.pyjam.as/8080 > tunnel.conf && wg-quick up ./tunnel.conf
```

Commandes à lancer pour les scripts python : 
```bash
python3.9 ./src/rabbit_to_minio.py
python3.9 ./src/rabbit_to_redis.py
python3.9 ./src/clics.py
```

Pour se créer un utilisateur MinIO : 
* Aller dans Identity --> User --> Create User