#!/usr/bin/bash
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

# Add vagrant user to docker group - means that 'sudo' command isn't required each time!
usermod -aG docker vagrant

# Above was found from HashiCorp at: https://developer.hashicorp.com/vagrant/tutorials/get-started/provision
