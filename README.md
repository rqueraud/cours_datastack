[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/rqueraud/cours_redis/main)

Test the container with : 
```bash
docker build -t cours_datastack .
docker run -it --rm -p 8888:8888 cours_datastack jupyter notebook --NotebookApp.default_url=/lab/ --ip=0.0.0.0 --port=8888
```

Commandes à lancer pour démarrer les différents services : 
```bash
redis-server --daemonize yes  # Redis
MINIO_ROOT_USER=admin MINIO_ROOT_PASSWORD=password minio server /mnt/data --console-address ":9001" &  # MinIO
systemctl start mongod & # MongoDB
sudo rabbitmq-server & # RabbitMQ
airflow db init
airflow users  create --role Admin --username root --email admin --firstname admin --lastname admin --password root
airflow standalone & # Airflow

# Localhost.run
ssh -R 80:localhost:9001 nokey@localhost.run  # minio ==> admin/password
ssh -R 80:localhost:15672 nokey@localhost.run  # rabbitmq ==> guest/guest

./ngrok config add-authtoken 2GLhjIIyFMiR0l7JStddRsHT56N_827XER1AXDhxZ1R9XkLo5
./ngrok http --region=eu 8080  # airflow ==> root/root

curl https://tunnel.pyjam.as/8080 > tunnel.conf && wg-quick up ./tunnel.conf
```

Commandes à lancer pour les scripts python : 
```bash
python3.9 rabbit_to_minio.py
python3.9 rabbit_to_redis.py
python3.9 clic.py
```

Pour se créer un utilisateur MinIO : 
* Aller dans Identity --> User --> Create User  # rqueraud/Catie515_