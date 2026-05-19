region         = "ap-south-1"
cluster_name   = "shopwave-eks"
vpc_cidr       = "10.0.0.0/16"

public_subnets  = ["10.0.1.0/24", "10.0.2.0/24"]
private_subnets = ["10.0.3.0/24", "10.0.4.0/24"]

instance_type = "m7i-flex.large"
cluster_role = "arn:aws:iam::768571909004:role/EKSClusterRole"
node_role    = "arn:aws:iam::768571909004:role/EKSNodeRole"
azs = ["ap-south-1a", "ap-south-1b"]
