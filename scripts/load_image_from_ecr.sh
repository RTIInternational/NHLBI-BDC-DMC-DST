#!/bin/bash
set -e

AWS_REGION="us-east-1"  # Change if needed
ECR_REPO="099963124704.dkr.ecr.us-east-1.amazonaws.com/dst/nhlbi-bdc-dmc-dst_bdc-dashboard-app"  # Replace with your ECR repo URL
IMAGE_TAG="latest"  # Change tag if necessary

echo "Logging into Amazon ECR..."
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 099963124704.dkr.ecr.us-east-1.amazonaws.com

echo "Pulling latest Docker image from ECR..."
#docker pull $ECR_REPO:$IMAGE_TAG


docker pull 099963124704.dkr.ecr.us-east-1.amazonaws.com/dst/nhlbi-bdc-dmc-dst_bdc-dashboard-app:latest