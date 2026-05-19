resource "aws_eks_cluster" "eks" {
  name     = var.cluster_name
  role_arn = var.cluster_role

  vpc_config {
    subnet_ids = var.subnet_ids
  }
}

resource "aws_eks_node_group" "nodes" {
  cluster_name    = aws_eks_cluster.eks.name
  node_group_name = "shopwave-nodes"
  node_role_arn   = var.node_role
  subnet_ids      = var.subnet_ids

  scaling_config {
    desired_size = 2
    max_size     = 3
    min_size     = 1
  }

  instance_types = [var.instance_type]
}