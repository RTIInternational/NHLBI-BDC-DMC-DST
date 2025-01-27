# Stop and remove only the dst app container

#docker rm -f bdc-dashboard-app

# Force Stop, Remove, and Delete Image
docker stop bdc-dashboard-app && docker rm <bdc-dashboard-app && docker rmi $(docker inspect bdc-dashboard-app --format '{{.Image}}')



