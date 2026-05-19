output "cluster_name" {
  description = "EKS Cluster Name"
  value       = aws_eks_cluster.eks.name
}

output "cluster_arn" {
  description = "EKS Cluster ARN"
  value       = aws_eks_cluster.eks.arn
}