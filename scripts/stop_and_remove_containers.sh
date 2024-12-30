# Stop and remove images and containers
docker stop $(docker ps -aq) && docker rm $(docker ps -aq)
docker rmi $(docker images -q)

