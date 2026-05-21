provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "test_bucket" {
  bucket = "checkov-trigger-test-bucket-123456"
  acl    = "public-read"
}