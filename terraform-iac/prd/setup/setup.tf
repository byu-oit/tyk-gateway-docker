terraform {
  backend "s3" {
    bucket         = "terraform-state-storage-915516739071"
    dynamodb_table = "terraform-state-lock-915516739071"
    key            = "tyk-gateway-docker-prd/setup.tfstate"
    region         = "us-west-2"
  }
}

provider "aws" {
  region = "us-west-2"
}

module "setup" {
  source        = "../../modules/setup/"
  env           = "prd"
  portal_url    = "living-permit-dev.aws-usw2.cloud-ara.tyk.io"
  dashboard_url = "living-permit-adm.aws-usw2.cloud-ara.tyk.io"
  west_gw_url   = "low-cymbals-gw.aws-usw2.cloud-ara.tyk.io"
  east_gw_url   = "low-cymbals-gw.aws-usw2.cloud-ara.tyk.io"
  provo_gw_url  = "low-cymbals-gw.aws-usw2.cloud-ara.tyk.io"
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
