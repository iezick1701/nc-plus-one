resource "aws_s3_bucket" "terraform_bucket" {
  bucket = "iezick-backend-state"
}

terraform {
  backend "s3" {
    bucket = "iezick-backend-state"
    key    = "nc-plus-one/terraform.tfstate"
    region = "eu-west-2"
  }
}