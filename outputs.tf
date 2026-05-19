output "cluster_name" {
  description = "EKS Cluster Name"
  value       = module.eks.cluster_name
}

output "cluster_arn" {
  description = "EKS Cluster ARN"
  value       = module.eks.cluster_arn
}

output "vpc_id" {
  description = "VPC ID"
  value       = module.vpc.vpc_id
}

output "public_subnet_ids" {
  description = "Public Subnet IDs"
  value       = module.vpc.public_subnet_ids
}

output "private_subnet_ids" {
  description = "Private Subnet IDs"
  value       = module.vpc.private_subnet_ids
}

output "node_group_details" {
  description = "Node group configuration"
  value = {
    instance_type = var.instance_type
    desired_size  = 2
    min_size      = 1
    max_size      = 3
  }
}