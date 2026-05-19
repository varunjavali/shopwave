module "vpc" {
  source = "./modules/vpc"

  vpc_cidr        = var.vpc_cidr
  public_subnets  = var.public_subnets
  private_subnets = var.private_subnets

  azs = ["ap-south-1a", "ap-south-1b"]

  project_name = "shopwave"
}

module "eks" {
  source = "./modules/eks"

  cluster_name  = var.cluster_name
  subnet_ids    = module.vpc.private_subnet_ids
  instance_type = var.instance_type

  desired_size = 2
  max_size     = 3
  min_size     = 1

  cluster_role = var.cluster_role
  node_role    = var.node_role
}