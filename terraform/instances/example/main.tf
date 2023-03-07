locals {
  # use name of this folder as prefix for resource names
  prefix = basename(abspath(path.module))

  # AWS params:
  region = "eu-central-1"
  profile = "default"
}

provider "aws" {
  #region = var.region
  region = local.region
  profile = local.profile
}


module "ssh-key" {
  source    = "../../modules/ssh-key"
  prefix = "honey"
}

module "ec2" {
  source     = "../../modules/ec2"
  prefix      = "honey"
  key_name   = module.ssh-key.key_name
}

# make output from ec2 module available:
output "data" {
  value = {
    ec2 = module.ec2
    ssh = {
      ssh = "ssh -i ${module.ssh-key.key_name}.pem ec2-user@${module.ec2.public_ip}"
      scp = "scp -i ${module.ssh-key.key_name}.pem file.txt ec2-user@${module.ec2.public_ip}:"
      remote = "ec2-user@${module.ec2.public_ip}"
      key = abspath("${module.ssh-key.key_name}.pem")
    }
    aws = {
      stop = "aws ec2 stop-instances --instance-ids ${module.ec2.instance_id} --region ${local.region} --profile ${local.profile}"
      start = "aws ec2 start-instances --instance-ids ${module.ec2.instance_id} --region ${local.region} --profile ${local.profile}"
    }
  }
}