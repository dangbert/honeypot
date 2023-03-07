output "public_ip" {
  value = aws_instance.this.public_ip
}

output "private_ip" {
  value = aws_instance.this.private_ip
}

output "instance_id" {
  value = aws_instance.this.id
}

output "ami_id" {
  value = data.aws_ami.amazon-linux-2.id 
  description = "ID of Amazon Machine Image that was used for this EC2 instance."
}