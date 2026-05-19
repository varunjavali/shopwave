variable "cluster_name" {
  description = "varun-cluster"
  type        = string
}

variable "subnet_ids" {
  description = "Subnets for EKS cluster"
  type        = list(string)
}

variable "instance_type" {
  description = "EC2 instance type for nodes"
  type        = string
}

variable "desired_size" {
  description = "Desired number of worker nodes"
  type        = number
}

variable "max_size" {
  description = "Maximum number of worker nodes"
  type        = number
}

variable "min_size" {
  description = "Minimum number of worker nodes"
  type        = number
}

variable "cluster_role" {
  description = "IAM role ARN for EKS cluster"
  type        = string
}

variable "node_role" {
  description = "IAM role ARN for worker nodes"
  type        = string
}