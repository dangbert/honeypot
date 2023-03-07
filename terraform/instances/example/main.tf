locals {
  # use name of this folder as namespace / prefix for resource names
  prefix = "honey-${basename(abspath(path.module))}"

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
  source = "../../modules/ssh-key"
  prefix = local.prefix
}

module "ec2" {
  source     = "../../modules/ec2"
  prefix     = local.prefix
  key_name   = module.ssh-key.key_name
}

# make output from ec2 module available:
output "data" {
  value = {
    ec2 = module.ec2
    site = {
      url = "http://${module.ec2.public_ip}/"
    }
    ssh = {
      ssh = "ssh -i ${module.ssh-key.key_name}.pem ec2-user@${module.ec2.public_ip}"
      # example scp command:
      scp = "scp -i ${module.ssh-key.key_name}.pem '${abspath("../../modules/ec2/setup.sh")}' ec2-user@${module.ec2.public_ip}:"
      remote = "ec2-user@${module.ec2.public_ip}"
      key = abspath("${module.ssh-key.key_name}.pem")
    }
    aws = {
      stop = "aws ec2 stop-instances --instance-ids ${module.ec2.instance_id} --region ${local.region} --profile ${local.profile}"
      start = "aws ec2 start-instances --instance-ids ${module.ec2.instance_id} --region ${local.region} --profile ${local.profile}"
    }
  }
}