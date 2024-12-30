# Stop and remove images and containers
docker ps -aq | xargs -r docker stop | xargs -r docker rm

docker images -q | xargs -r docker rmi


