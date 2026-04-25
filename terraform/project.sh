#!/usr/bin/bash

exec > /var/log/artifact.log 2>&1
set -x

echo "cd to /root directory..."
cd /root

echo "whoami..."
whoami

echo "pwd..."
pwd

# This updates the package list
apt-get update

# These are the required packages
apt-get install -y ca-certificates curl gnupg

# Add Docker's official GPG key
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
chmod a+r /etc/apt/keyrings/docker.gpg

# Add Docker repo
echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker packages
apt-get update
apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Login to docker for access to personal registry
echo "dckr_pat_kMcmoi1oTECeoSm2qG7V0ESi_Eo" | sudo docker login -u dk04 --password-stdin

echo "Ensuring that docker network doesn't interfere with SSH"
cd /etc/docker
cat <<EOF | sudo tee /etc/docker/daemon.json
{
  "default-address-pools": [
    {
      "base": "172.20.0.0/16",
      "size": 24
    }
  ],
  "bip": "172.19.0.1/24",
  "mtu": 1400,
  "labels": ["vm_ip=$VM_IP"]
}
EOF
sudo systemctl restart docker

# Above was found from HashiCorp at: https://developer.hashicorp.com/vagrant/tutorials/get-started/provision
cd /
echo "Creating the app directory and adding the compose.yaml file"
mkdir app
cd app
touch compose.yaml
touch .env
cat << `EOF` >> compose.yaml
services:
  # Setting up redis for dev and prod environments
  redis:
    image: redis:8.6.2-alpine

  # Setting up the prod env -- TO BE PROPERLY CONFIGURED WHEN SETTING UP CLOUD DEPLOYMENT
  database-prod:
    image: mariadb:11.8-noble
    environment:
      - MARIADB_ROOT_PASSWORD=\${DB_PASSWORD}
      - MARIADB_DATABASE=\${DB_NAME}
    volumes:
      - dte-prod-db-volume:/var/lib/mysql
    healthcheck:
      test: ["CMD", "healthcheck.sh", "--connect", "--innodb_initialized"] # https://mariadb.com/docs/server/server-management/automated-mariadb-deployment-and-administration/docker-and-mariadb/using-healthcheck-sh
      start_period: 40s
      interval: 10s
      timeout: 5s
      retries: 5

  alembic_migrations-prod:
    image: dk04/data-trust-engine-registry:backend-latest
    environment:
      - DB_HOST=database-prod
      - DB_USERNAME=\${DB_USERNAME}
      - DB_PASSWORD=\${DB_PASSWORD}
      - DB_NAME=\${DB_NAME}
      - DB_TEST_NAME=\${DB_TEST_NAME}
    command: ["python", "-m", "alembic", "-c", "alembic.ini", "upgrade", "head"]
    depends_on:
      database-prod:
        condition: service_healthy

  backend-prod:
    image: dk04/data-trust-engine-registry:backend-latest
    pull_policy: never
    environment:
      - CLIENT_ID=\${CLIENT_ID}
      - CLIENT_SECRET=\${CLIENT_SECRET}
      - AUTHORITY=\${AUTHORITY}
      - SCOPES=\${SCOPES}
      - DB_HOST=database-prod
      - DB_USERNAME=\${DB_USERNAME}
      - DB_PASSWORD=\${DB_PASSWORD}
      - DB_NAME=\${DB_NAME}
      - DB_TEST_NAME=\${DB_TEST_NAME}
      - ACCESS_TOKEN_SECRET=\${ACCESS_TOKEN_SECRET}
      - ALGORITHM=\${ALGORITHM}
      - MAIL_PASSWORD=\${MAIL_PASSWORD}
      - ZEROBOUNCE_API_KEY=\${ZEROBOUNCE_API_KEY}
      - FERNET_KEY=\${FERNET_KEY}
      - FRONTEND_HOST=http://localhost #  THESE MUST ALWAYS BE TO WHATEVER THE USER'S CLIENT SHOULD BE! FOR DEV, THAT IS LOCALHOST
      - REDIRECT_URI=http://localhost/api
      - REDIS_HOST=redis
    depends_on:
      alembic_migrations-prod:
        condition: service_completed_successfully

  frontend-prod:
    image: dk04/data-trust-engine-registry:frontend-latest
    ports:
      - 80:80
    depends_on:
      - backend-prod

  # Setting up celery for prod env
  celery-prod:
    image: dk04/data-trust-engine-registry:backend-latest
    pull_policy: never
    environment:
      - CLIENT_ID=\${CLIENT_ID}
      - CLIENT_SECRET=\${CLIENT_SECRET}
      - AUTHORITY=\${AUTHORITY}
      - SCOPES=\${SCOPES}
      - DB_HOST=database-prod
      - DB_USERNAME=\${DB_USERNAME}
      - DB_PASSWORD=\${DB_PASSWORD}
      - DB_NAME=\${DB_NAME}
      - DB_TEST_NAME=\${DB_TEST_NAME}
      - ACCESS_TOKEN_SECRET=\${ACCESS_TOKEN_SECRET}
      - ALGORITHM=\${ALGORITHM}
      - MAIL_PASSWORD=\${MAIL_PASSWORD}
      - ZEROBOUNCE_API_KEY=\${ZEROBOUNCE_API_KEY}
      - FERNET_KEY=\${FERNET_KEY}
      - FRONTEND_HOST=http://localhost #  THESE MUST ALWAYS BE TO WHATEVER THE USER'S CLIENT SHOULD BE! FOR DEV, THAT IS LOCALHOST
      - REDIRECT_URI=http://localhost/api
      - REDIS_HOST=redis
    command: ["celery","-A","app.core.celery_worker.celery", "worker", "--loglevel=info", "--concurrency=1"]
    depends_on:
      - redis
      - backend-prod

  # Setting up WatchTower for monitoring changes in docker repository in docker hub
  watchtower:
    image: containrrr/watchtower:latest
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - /home/c23026535/.docker/config.json:/config.json
    command: --cleanup --api-version 1.54 --interval 3600

volumes:
  dte-prod-db-volume:
`EOF`

echo "Pulling all the images..."
sudo docker compose pull



