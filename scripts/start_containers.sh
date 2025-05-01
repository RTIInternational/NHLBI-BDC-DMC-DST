#The command never executed in the Install phase for some reason
docker load < /home/ubuntu/dst-pipeline/nhlbi-bdc-dmc-dst_bdc-dashboard-app-prod.tar


#!/bin/bash
cd /home/ubuntu/dst-pipeline/scripts

# Build and start the containers
docker-compose up -d bdc-dashboard-app
