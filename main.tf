# Cloud Deployment Design (AWS)
# Infrastructure as Code with Terraform

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

# VPC Configuration
resource "aws_vpc" "app_vpc" {
  cidr_block = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support = true
  
  tags = {
    Name = "Production-VPC"
  }
}

# Postgres RDS (Database Infrastructure)
resource "aws_db_instance" "app_db" {
  identifier           = "app-production-db"
  engine               = "postgres"
  engine_version       = "15.3"
  instance_class       = "db.t3.medium"
  allocated_storage    = 50
  
  db_name              = "app_db"
  username             = "admin_user"
  password             = "secure_password_replace_me"
  
  multi_az             = true 
  publicly_accessible  = false
  skip_final_snapshot  = false
  
  tags = {
    Environment = "Production"
  }
}

# ElastiCache Redis Cluster (Caching Setup)
resource "aws_elasticache_cluster" "app_redis" {
  cluster_id           = "app-production-redis"
  engine               = "redis"
  node_type            = "cache.t3.micro"
  num_cache_nodes      = 1
  parameter_group_name = "default.redis7"
  engine_version       = "7.0"
  port                 = 6379
}

# ECS Cluster for App Deployment (Production Containers)
resource "aws_ecs_cluster" "app_cluster" {
  name = "app-production-cluster"
  
  setting {
    name  = "containerInsights"
    value = "enabled"  
  }
}
