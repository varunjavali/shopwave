variable "region" {}
variable "cluster_name" {}
variable "vpc_cidr" {}
variable "public_subnets" {
  type = list(string)
}
variable "private_subnets" {
  type = list(string)
}
variable "instance_type" {}
variable "cluster_role" {
  description = "IAM role for EKS cluster"
  type        = string
}

variable "node_role" {
  description = "IAM role for EKS nodes"
  type        = string
}
variable "azs" {
  description = "Availability Zones"
  type        = list(string)
}