terraform {
  backend "s3" {
    bucket         = "terraform-state-storage-915516739071"
    dynamodb_table = "terraform-state-lock-915516739071"
    key            = "tyk-gateway-docker-prd/setup.tfstate"
    region         = "us-west-2"
  }
}

provider "aws" {
  version = "~> 2.42"
  region  = "us-west-2"
}

module "setup" {
  source = "../../modules/setup/"
  env    = "prd"
  tyk_generated_name = "living-permit"
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
