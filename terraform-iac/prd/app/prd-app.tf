terraform {
  backend "s3" {
    bucket         = "terraform-state-storage-915516739071"
    dynamodb_table = "terraform-state-lock-915516739071"
    key            = "tyk-gateway-docker-prd/app.tfstate"
    region         = "us-west-2"
  }
}

provider "aws" {
  region = "us-west-2"
}

module "app" {
  source = "../../modules/app/"
  env    = "prd"
}

