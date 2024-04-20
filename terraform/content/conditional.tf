variable  "name" {
    type = string
}
variable "ami" {
    type = string
    default = "ami-09331245601cf"
}
variable "small" {
    type = string
    default = "t2.nano"
}
variable "large" {
    type = string
    default = "t2.2xlarge"
}

resource "aws_instance" "mario_servers" {
    ami = var.ami
    instance_type = var.name == "tiny" ? var.small : var.large
    tags = {
        Name = var.name
    }
}

# terraform apply -var name=tiny