terraform {
  backend "s3" {
    bucket         = "terraform-state-storage-598052082689"
    dynamodb_table = "terraform-state-lock-598052082689"
    key            = "tyk-gateway-docker-dev/app.tfstate"
    region         = "us-west-2"
  }
}

provider "aws" {
  region = "us-west-2"
}

module "app" {
  source = "../../modules/app/"
  env    = "dev"
}

