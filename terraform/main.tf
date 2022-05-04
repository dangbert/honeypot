provider "aws" {
  #region = var.region
  region = "eu-central-1"
}

module "ssh-key" {
  source    = "./modules/ssh-key"
  prefix = "honey"
}

module "ec2" {
  source     = "./modules/ec2"
  prefix      = "honey"
  #vpc        = module.networking.vpc
  #sg_pub_id  = module.networking.sg_pub_id
  #sg_priv_id = module.networking.sg_priv_id
  key_name   = module.ssh-key.key_name
}

output "data" {
  value = module.ec2
}

output "ssh_cmd" {
  value = "ssh -i ${module.ssh-key.key_name}.pem ec2-user@${module.ec2.public_ip}"
}