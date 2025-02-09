#The command never executed in the Install phase for some reason
#docker load < /home/ubuntu/dst-pipeline/nhlbi-bdc-dmc-dst_bdc-dashboard-app.tar

echo "Logging into Amazon ECR..."
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 099963124704.dkr.ecr.us-east-1.amazonaws.com

#!/bin/bash
cd /home/ubuntu/dst-pipeline/scripts

# Build and start the containers
docker-compose up -d bdc-dashboard-app
