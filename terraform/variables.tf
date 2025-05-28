variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "ami_id" {
  description = "AMI ID for EC2"
  type        = string
  default     = "ami-0f9de6e2d2f067fca"
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t2.large"
}

variable "key_name" {
  description = "Key pair for SSH access"
  type        = string
  default     = "jenkins"
}

variable "subnet_id" {
  description = "Subnet ID to launch the instance"
  type        = string
  default     = "subnet-0c0b6a50e10b0ba94"
}

variable "vpc_id" {
  description = "VPC ID for the security group"
  type        = string
  default     = "vpc-072e855dcbcb49cea"
}

variable "instance_name" {
  description = "Name tag for the instance"
  type        = string
  default     = "jenkins-server"
}

variable "volume_size" {
  description = "Root volume size in GB"
  type        = number
  default     = 40
}
