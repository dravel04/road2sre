data "aws_iam_policy_document" "assume_role" {
  statement {
    effect = "Allow"
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
    actions = ["sts:AssumeRole"]
  }
}
data "archive_file" "lambda" {
  type        = "zip"
  source_file = "../lambda/lambdaname.py"
  output_path = var.lambda_file_path
}

variable "policy_file_path" {
  default = "./policy.json"
}

variable "lambda_file_path" {
  default = "../lambda/lambda.zip"
}

variable "api_name" {
  type = string
  default = "product-nuwe"
}

variable "stage_name" {
  type = string
  default = "production"
}
