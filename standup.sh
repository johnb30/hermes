#Install docker
wget -qO- https://get.docker.com/ | sh
#Install docker compose
sudo touch /usr/local/bin/docker-compose
sudo chmod 777 /usr/local/bin/docker-compose
curl -L https://github.com/docker/compose/releases/download/1.1.0/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
#Install unzip
sudo apt-get install unzip
#Install htop because I like it
sudo apt-get install htop
