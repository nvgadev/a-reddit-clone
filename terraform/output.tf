output "public_ip" {
  description = "Public IP of the EC2 instance"
  value       = aws_instance.jenkins.public_ip
}
