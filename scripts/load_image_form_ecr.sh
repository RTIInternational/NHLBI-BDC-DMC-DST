#!/bin/bash
set -e

AWS_REGION="us-east-1"  # Change if needed
ECR_REPO="099963124704.dkr.ecr.us-east-1.amazonaws.com/dst/nhlbi-bdc-dmc-dst_bdc-dashboard-app"  # Replace with your ECR repo URL
IMAGE_TAG="latest"  # Change tag if necessary

echo "Logging into Amazon ECR..."
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_REPO

echo "Pulling latest Docker image from ECR..."
docker pull $ECR_REPO:$IMAGE_TAG

echo "Stopping and removing existing containers..."
docker-compose -f /home/ubuntu/dst-pipeline/scripts/docker-compose.yml down

echo "Removing old Docker images..."
docker image prune -f

echo "Starting new container..."
docker-compose -f /home/ubuntu/dst-pipeline/scripts/docker-compose.yml up -d

echo "Deployment completed!"
