sudo snap install docker
sudo groupadd docker
sudo gpasswd -a $USER docker 
newgrp docker

docker build -t test .
docker run --net=host -v /home/free/CV_projects/camera_grabber:/home/project -it test




docker rm $(docker ps -a -q)
docker rmi $(docker images -q)
docker rmi $(docker images -q) --force


pip install -r requirements.txt

## NVIDIA DOCKER

# Add the package repositories
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update && sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker

docker run --gpus all nvidia/cuda:10.0-base nvidia-smi