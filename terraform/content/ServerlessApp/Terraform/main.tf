provider "aws" {
  access_key                  = "test"
  secret_key                  = "test"
  region                      = "us-east-1"
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true

# Delete resources that are not going to be used for code cleanup
  endpoints {
    apigateway     = "http://localhost:4566"
    apigatewayv2   = "http://localhost:4566"
    cloudformation = "http://localhost:4566"
    cloudwatch     = "http://localhost:4566"
    dynamodb       = "http://localhost:4566"
    ec2            = "http://localhost:4566"
    es             = "http://localhost:4566"
    elasticache    = "http://localhost:4566"
    firehose       = "http://localhost:4566"
    iam            = "http://localhost:4566"
    kinesis        = "http://localhost:4566"
    lambda         = "http://localhost:4566"
    rds            = "http://localhost:4566"
    redshift       = "http://localhost:4566"
    route53        = "http://localhost:4566"
    s3             = "http://localhost:4566"
    secretsmanager = "http://localhost:4566"
    ses            = "http://localhost:4566"
    sns            = "http://localhost:4566"
    sqs            = "http://localhost:4566"
    ssm            = "http://localhost:4566"
    stepfunctions  = "http://localhost:4566"
    sts            = "http://localhost:4566"
  }
}

# Add here all the infraestructure logic
resource "aws_dynamodb_table" "events" {
  name = "EVENTS"
  billing_mode = "PAY_PER_REQUEST"
  hash_key = "eventId"
  attribute {
      name = "eventId"
      type = "N"
  }
}

# lambda definition
resource "aws_lambda_function" "CreateEventHandler" {
  filename      = var.lambda_file_path
  function_name = "CreateEventHandler"
  role          = aws_iam_role.lambda_role.arn
  handler       = "createevent.handler"
  runtime       = "python3.8"
}

resource "aws_iam_role" "lambda_role" {
  name = "lambda_role"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

resource "aws_iam_role_policy" "lambda_policy" {
  name = "lambda_policy"
  role = aws_iam_role.lambda_role.id
  policy = file(var.policy_file_path)
}

# api definition
resource "aws_api_gateway_rest_api" "product_nuwe" {
  name = var.api_name
}

resource "aws_api_gateway_resource" "events" {
  rest_api_id = aws_api_gateway_rest_api.product_nuwe.id
  parent_id = aws_api_gateway_rest_api.product_nuwe.root_resource_id
  path_part = "events"
}

resource "aws_api_gateway_method" "post_events" {
  rest_api_id = aws_api_gateway_rest_api.product_nuwe.id
  resource_id = aws_api_gateway_resource.events.id
  http_method = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "lambda_integration" {
  rest_api_id = aws_api_gateway_rest_api.product_nuwe.id
  resource_id = aws_api_gateway_resource.events.id
  http_method = aws_api_gateway_method.post_events.http_method
  integration_http_method = "POST"
  type = "AWS_PROXY"
  uri = aws_lambda_function.CreateEventHandler.invoke_arn
}

resource "aws_api_gateway_deployment" "production" {
  depends_on = [
    aws_api_gateway_integration.lambda_integration
  ]
  rest_api_id = aws_api_gateway_rest_api.product_nuwe.id
  stage_name = var.stage_name
}

resource "aws_lambda_permission" "api_gateway_permission" {
  statement_id = "AllowExecutionFromAPIGateway"
  action = "lambda:InvokeFunction"
  function_name = aws_lambda_function.CreateEventHandler.function_name
  principal = "apigateway.amazonaws.com"
  source_arn = "${aws_api_gateway_rest_api.product_nuwe.execution_arn}/events/*"
}