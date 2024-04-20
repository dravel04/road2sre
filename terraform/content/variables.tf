# Recursos sacados del curso de KodeKloud
# https://developer.hashicorp.com/terraform/language/expressions/types
variable "name" {
     type = string
     default = "Mark"
  
}
variable "number" {
     type = bool
     default = true
  
}
variable "distance" {
     type = number
     default = 5
  
}
variable "jedi" {
     type = map
     default = {
     filename = "/root/first-jedi"
     content = "phanius"
     }
  
}
variable "gender" {
     type = list(string)
     default = ["Male", "Female"]
}
variable "hard_drive" {
     type = map
     default = {
          slow = "HHD"
          fast = "SSD"
     }
}
variable "users" {
     type = set(string)
     default = ["tom", "jerry", "pluto", "daffy", "donald", "jerry", "chip", "dale"]
}

  
# -----------
# -----------

variable "cloud_users" {
    type = string
    default = "andrew:ken:faraz:mutsumi:peter:steve:braja"
}
resource "aws_iam_user" "cloud" {
    name = split(":",var.cloud_users)[count.index]
    count = length(split(":",var.cloud_users))
}


