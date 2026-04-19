#!/usr/bin/bash

exec > /var/log/artifact.log 2>&1
set -x

echo "cd to /root directory..."
cd /root

# Setting up Docker
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

# Setting up the GitLab Runner

echo "Downloading repo configuration script"
sudo curl -L "https://packages.gitlab.com/install/repositories/runner/gitlab-runner/script.deb.sh" -o script.deb.sh

echo "Running the script"
sudo bash script.deb.sh

echo "Installing the GitLab Runner"
sudo apt install gitlab-runner -y

echo "Registering the runner"
sudo sudo gitlab-runner register \
--non-interactive \
--url https://git.cardiff.ac.uk \
--token glrt-CjUVcbS0SuhbPn2ahSrDn286MQpwOmtsOQp0OjMKdToybXYT.01.1c1uwq4o5 \
--executor docker \
--docker-image docker:29.4.0-cli \
--docker-volumes "/cache" \
--docker-volumes "/builds:/builds" \
--docker-volumes "/var/run/docker.sock:/var/run/docker.sock"

echo "Adding the gitlab-runner to the docker group, so that that it doesn't need sudo to run commands"
sudo usermod -aG docker gitlab-runner
