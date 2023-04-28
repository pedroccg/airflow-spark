#Uninstall old version
sudo apt-get remove docker docker-engine docker.io containerd runc

#Set up the repository
sudo apt-get update
sudo apt-get install \
    ca-certificates \
    curl \
    gnupg


#Add Dockeofficial GPG key:
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg


#Setup repository
echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null


#Install Docker Engine
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin



#Create docker group and add user to group
sudo groupadd docker
sudo usermod -aG docker adminuser
sudo usermod -aG docker adminuser

sudo chown "adminuser":"adminuser" /home/adminuser/.docker -R
sudo chmod g+rwx "home/adminuser/.docker" -R


#Configure Docker to start on
sudo systemctl enable docker.service
sudo systemctl enable containerd.service