// Create aws_ami filter to pick up the ami available in your region
data "aws_ami" "amazon-linux-2" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm*"]
  }
}

# ec2 instance
# TODO: check/control its disk space size?
resource "aws_instance" "this" {
  ami                         = data.aws_ami.amazon-linux-2.id
  associate_public_ip_address = true
  instance_type               = "t2.micro"
  key_name                    = var.key_name
  #subnet_id                   = var.vpc.public_subnets[0]
  vpc_security_group_ids      = [aws_security_group.ec2.id]


  tags = {
    "Name" = "${var.prefix}-PUBLIC"
  }

  # copy setup.sh to EC2
  provisioner "file" {
    source      = "${path.module}/setup.sh"
    destination = "/home/ec2-user/setup.sh"
    connection {
      type        = "ssh"
      user        = "ec2-user"
      private_key = file("${var.key_name}.pem")
      host        = self.public_ip
    }
  }

  # provisioner "remote-exec" {
  #   inline = ["chmod 755 ~/setup.sh"]
  #   connection {
  #     type        = "ssh"
  #     user        = "ec2-user"
  #     private_key = file("${var.key_name}.pem")
  #     host        = self.public_ip
  #   }
  # }
  
  # run setup script for installing desired software on EC2
  provisioner "remote-exec" {
    script = "${path.module}/setup.sh"
    connection {
      type        = "ssh"
      user        = "ec2-user"
      private_key = file("${var.key_name}.pem")
      host        = self.public_ip
    }
  }
}

# https://www.middlewareinventory.com/blog/terraform-aws-example-ec2/
resource "aws_security_group" "ec2" {
  name = "${var.prefix}-ec2-sg"
  #vpc_id = lookup(var.awsprops, "vpc")

  # allow SSH Transport
  ingress {
    from_port = 22
    protocol = "tcp"
    to_port = 22
    cidr_blocks = ["0.0.0.0/0"]
  }

  # allow Port 80 Transport
  ingress {
    from_port = 80
    protocol = "tcp"
    to_port = 80
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port       = 0
    to_port         = 0
    protocol        = "-1"
    cidr_blocks     = ["0.0.0.0/0"]
  }

  lifecycle {
    create_before_destroy = true
  }
}
