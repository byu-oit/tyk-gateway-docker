terraform {
  required_version = "0.12.26"
  backend "s3" {
    bucket         = "terraform-state-storage-598052082689"
    dynamodb_table = "terraform-state-lock-598052082689"
    key            = "tyk-gateway-docker-dev/setup.tfstate"
    region         = "us-west-2"
  }
}

provider "aws" {
  version = "~> 3.0"
  region  = "us-west-2"
}

module "setup" {
  source = "../../modules/setup/"
  env    = "dev"
  tyk_generated_name = "respectable-parchment"
}

output "hosted_zone_id" {
  value = module.setup.hosted_zone.zone_id
}

output "hosted_zone_name" {
  value = module.setup.hosted_zone.name
}

output "hosted_zone_name_servers" {
  value = module.setup.hosted_zone.name_servers
}

output "note" {
  value = "These NS records need to be manually added QIP."
}
