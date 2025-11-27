# terraform/main.tf
# Main Terraform configuration for Infinite AI Security Platform

terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.0"
    }
    helm = {
      source  = "hashicorp/helm"
      version = "~> 2.0"
    }
  }
}

# Provider configuration
provider "aws" {
  region = var.aws_region
  
  default_tags {
    tags = {
      Project     = "infinite-ai-security"
      Environment = var.environment
      ManagedBy   = "terraform"
    }
  }
}

provider "kubernetes" {
  host                   = module.eks.cluster_endpoint
  cluster_ca_certificate = base64decode(module.eks.cluster_certificate_authority_data)
  
  token = data.aws_eks_cluster_auth.this.token
}

provider "helm" {
  kubernetes {
    host                   = module.eks.cluster_endpoint
    cluster_ca_certificate = base64decode(module.eks.cluster_certificate_authority_data)
    
    token = data.aws_eks_cluster_auth.this.token
  }
}

# VPC Module
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.0.0"

  name = "${var.project_name}-${var.environment}-vpc"
  cidr = var.vpc_cidr_block

  azs             = var.availability_zones
  private_subnets = var.private_subnet_cidrs
  public_subnets  = var.public_subnet_cidrs

  enable_nat_gateway = true
  single_nat_gateway = true
  enable_dns_hostnames = true
  enable_dns_support   = true

  private_subnet_tags = {
    "kubernetes.io/role/internal-elb" = "1"
  }

  public_subnet_tags = {
    "kubernetes.io/role/elb" = "1"
  }
}

# EKS Cluster
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "19.0.0"

  cluster_name    = "${var.project_name}-${var.environment}"
  cluster_version = "1.28"

  vpc_id     = module.vpc.vpc_id
  subnet_ids = concat(module.vpc.private_subnets, module.vpc.public_subnets)

  # EKS Control Plane
  cluster_endpoint_private_access = true
  cluster_endpoint_public_access  = true

  # Node groups
  eks_managed_node_groups = {
    workers = {
      name = "${var.project_name}-worker-node-group"

      instance_types = var.worker_node_instance_types
      capacity_type  = "SPOT"

      min_size     = var.node_group_min_size
      max_size     = var.node_group_max_size
      desired_size = var.node_group_desired_size

      labels = {
        role = "worker"
      }

      tags = {
        Name = "${var.project_name}-worker-nodes"
      }
    }
  }

  # EFS for shared storage
  create_efs = true
  efs_name   = "${var.project_name}-${var.environment}-efs"

  tags = {
    Environment = var.environment
  }
}

# Data source for EKS cluster auth
data "aws_eks_cluster_auth" "this" {
  name = module.eks.cluster_name
}

# ALB Controller IAM Policy
resource "aws_iam_policy" "alb_controller" {
  name = "${var.project_name}-${var.environment}-alb-controller-policy"
  path = "/"
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "acm:Describe*",
          "acm:List*",
          "acm:Get*",
          "ec2:Authorize*",
          "ec2:Create*",
          "ec2:Delete*",
          "ec2:Describe*",
          "ec2:Revoke*",
          "elasticloadbalancing:*"
        ]
        Resource = "*"
      }
    ]
  })
}

# EFS for persistent storage
resource "aws_efs_file_system" "persistence" {
  creation_token = "${var.project_name}-${var.environment}-persistence"
  
  tags = {
    Name = "${var.project_name}-${var.environment}-efs"
  }
}

resource "aws_efs_mount_target" "private_a" {
  count = length(var.availability_zones)
  
  file_system_id  = aws_efs_file_system.persistence.id
  subnet_id       = element(module.vpc.private_subnets, count.index)
  security_groups = [aws_security_group.efs.id]
}

resource "aws_security_group" "efs" {
  name_prefix = "${var.project_name}-${var.environment}-efs-"
  vpc_id      = module.vpc.vpc_id

  ingress {
    from_port = 2049
    to_port   = 2049
    protocol  = "tcp"
    security_groups = [module.eks.node_security_group_id]
  }

  tags = {
    Name = "${var.project_name}-${var.environment}-efs-sg"
  }
}

# RDS PostgreSQL Instance for production
resource "aws_db_subnet_group" "main" {
  name       = "${var.project_name}-${var.environment}-db-subnet-group"
  subnet_ids = module.vpc.private_subnets

  tags = {
    Name = "${var.project_name}-${var.environment}-db-subnet-group"
  }
}

resource "aws_security_group" "rds" {
  name_prefix = "${var.project_name}-${var.environment}-rds-"
  vpc_id      = module.vpc.vpc_id

  ingress {
    from_port = 5432
    to_port   = 5432
    protocol  = "tcp"
    security_groups = [module.eks.node_security_group_id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.project_name}-${var.environment}-rds-sg"
  }
}

resource "aws_db_instance" "main" {
  identifier = "${var.project_name}-${var.environment}"

  allocated_storage    = 100
  max_allocated_storage = 500
  storage_type         = "gp3"
  storage_encrypted    = true

  engine         = "postgres"
  engine_version = "15.4"
  instance_class = var.db_instance_class

  db_name  = var.db_name
  username = var.db_username
  password = var.db_password

  db_subnet_group_name   = aws_db_subnet_group.main.id
  vpc_security_group_ids = [aws_security_group.rds.id]

  backup_retention_period = 7
  backup_window          = "03:00-04:00"
  maintenance_window     = "sun:04:00-sun:05:00"

  skip_final_snapshot = false
  final_snapshot_identifier = "${var.project_name}-${var.environment}-final-snapshot"

  tags = {
    Name = "${var.project_name}-${var.environment}-db"
  }
}

# Redis ElastiCache Cluster
resource "aws_elasticache_subnet_group" "redis" {
  name       = "${var.project_name}-${var.environment}-redis-subnet-group"
  subnet_ids = module.vpc.private_subnets

  tags = {
    Name = "${var.project_name}-${var.environment}-redis-subnet-group"
  }
}

resource "aws_elasticache_cluster" "redis" {
  cluster_id         = "${var.project_name}-${var.environment}-redis"
  engine             = "redis"
  node_type          = var.redis_node_type
  port               = 6379
  parameter_group_name = "default.redis7"
  
  num_cache_nodes    = 1
  engine_version     = "7.0"
  
  subnet_group_name  = aws_elasticache_subnet_group.redis.id
  security_group_ids = [aws_security_group.redis.id]
  
  apply_immediately = true

  tags = {
    Name = "${var.project_name}-${var.environment}-redis"
  }
}

resource "aws_security_group" "redis" {
  name_prefix = "${var.project_name}-${var.environment}-redis-"
  vpc_id      = module.vpc.vpc_id

  ingress {
    from_port = 6379
    to_port   = 6379
    protocol  = "tcp"
    security_groups = [module.eks.node_security_group_id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.project_name}-${var.environment}-redis-sg"
  }
}

# Outputs
output "cluster_endpoint" {
  description = "Endpoint for EKS control plane"
  value       = module.eks.cluster_endpoint
}

output "cluster_security_group_id" {
  description = "Security group ids attached to the cluster control plane"
  value       = module.eks.cluster_additional_security_group_ids
}

output "node_security_group_id" {
  description = "Security group for all nodes in the cluster"
  value       = module.eks.node_security_group_id
}

output "rds_endpoint" {
  description = "RDS instance endpoint"
  value       = aws_db_instance.main.endpoint
}

output "redis_endpoint" {
  description = "Redis cluster endpoint"
  value       = aws_elasticache_cluster.redis.cache_nodes[0].address
}

output "vpc_id" {
  description = "VPC ID"
  value       = module.vpc.vpc_id
}

output "private_subnets" {
  description = "Private subnets"
  value       = module.vpc.private_subnets
}