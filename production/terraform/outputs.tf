# terraform/outputs.tf
# Outputs for the Infinite AI Security Platform Terraform configuration

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

output "public_subnets" {
  description = "Public subnets"
  value       = module.vpc.public_subnets
}

output "cluster_name" {
  description = "Name of the EKS cluster"
  value       = module.eks.cluster_name
}

output "cluster_version" {
  description = "Version of the EKS cluster"
  value       = module.eks.cluster_version
}

output "node_group_arn" {
  description = "ARN of the EKS node group"
  value       = module.eks.eks_managed_node_groups["workers"].node_group_arn
}

output "efs_id" {
  description = "ID of the EFS file system"
  value       = aws_efs_file_system.persistence.id
}

output "alb_controller_policy_arn" {
  description = "ARN of the ALB Controller IAM policy"
  value       = aws_iam_policy.alb_controller.arn
}