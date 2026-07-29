#!/bin/bash
# AWS Deployment Script using ECS Fargate

CLUSTER_NAME="cognitive-alarm-cluster"
SERVICE_NAME="frontend-service"
TASK_FAMILY="frontend-task"
REGION="us-east-1"

echo "Deploying Cognitive Alarm Frontend to AWS ECS..."

# Create cluster (if not exists)
aws ecs create-cluster --cluster-name $CLUSTER_NAME --region $REGION

# Register task definition using an existing JSON config
# aws ecs register-task-definition --cli-input-json file://aws-task-def.json --region $REGION

# Update or Create Service
aws ecs update-service --cluster $CLUSTER_NAME --service $SERVICE_NAME --force-new-deployment --region $REGION

echo "AWS ECS deployment triggered."
