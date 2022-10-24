FROM ubuntu:20.04

RUN apt-get update && apt-get upgrade -y

RUN apt-get install -y python3.9
RUN apt-get install -y python3-pip

# ##### Binder doc #####

RUN python3.9 -m pip install --no-cache-dir notebook jupyterlab

ARG NB_USER=jovyan
ARG NB_UID=1000
ENV USER ${NB_USER}
ENV NB_UID ${NB_UID}
ENV HOME /home/${NB_USER}

RUN adduser --disabled-password \
    --gecos "Default user" \
    --uid ${NB_UID} \
    ${NB_USER}

USER root

######################

# Install tools
RUN python3.9 -m pip install --no-cache-dir notebook pymongo pandas xmltodict elasticsearch
RUN apt-get install -y htop curl
RUN apt-get update
RUN apt-get install -y default-jre default-jdk

# Allow sudo commands
RUN apt-get install -y sudo
RUN echo "ALL            ALL = (ALL) NOPASSWD: ALL" >> /etc/sudoers
RUN apt-get install -y systemd

# Install n 
RUN curl -L https://raw.githubusercontent.com/tj/n/master/bin/n -o n
RUN bash n lts

# Install redis
RUN apt-get install -y lsb-release
RUN curl -fsSL https://packages.redis.io/gpg | gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg
RUN echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | tee /etc/apt/sources.list.d/redis.list
RUN apt-get update
RUN apt-get install -y redis
RUN python3.9 -m pip install redis

# Install MinIO
RUN apt-get install -y wget
RUN wget https://dl.min.io/server/minio/release/linux-amd64/minio_20221021223748.0.0_amd64.deb
RUN dpkg -i minio_20221021223748.0.0_amd64.deb
RUN mkdir /mnt/data
RUN chown -R jovyan /mnt/data && chmod u+rxw /mnt/data
# Install MinIO viewer
RUN wget https://github.com/minio/console/releases/latest/download/console-linux-amd64 -P /home/${NB_USER}
RUN chmod +x /home/${NB_USER}/console-linux-amd64
# Install minio python
RUN python3.9 -m pip install minio

# Install MongoDB
RUN wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | apt-key add -
RUN echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-6.0.list
RUN apt-get update
RUN apt-get install -y mongodb-org
# Install mongo-express
RUN npm install -g mongo-express
RUN python3.9 -m pip install pymongo
RUN mkdir -p /data/db

# Install RabbitMQ
RUN apt-get install -y rabbitmq-server
# Install python dependency for rabbitmq
RUN python3.9 -m pip install pika
# Enable rabbitmq_management
RUN rabbitmq-plugins enable rabbitmq_management

# Install dependencies for localhost.run
RUN apt-get install -y ssh
# Generate ssh key
RUN mkdir -p /home/${NB_USER}/.ssh
RUN ssh-keygen -t ed25519 -C "localhost.run" -N "" -f "/home/${NB_USER}/.ssh/id_ed25519"

# Download ngrok
RUN wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz
RUN tar -xvzf ngrok-v3-stable-linux-amd64.tgz
RUN mv ngrok /home/${NB_USER}/

# Install Airflow
ENV AIRFLOW_HOME=/home/${NB_USER}/airflow
ENV AIRFLOW_VERSION=2.4.1
ENV PYTHON_VERSION=3.9
ENV CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
RUN python3.9 -m pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
ENV AIRFLOW__CORE__LOAD_EXAMPLES=False

# Set directory
WORKDIR /home/${NB_USER}
COPY . ${HOME}

# Set user
RUN chown -R ${NB_UID} ${HOME}
USER ${NB_USER}
