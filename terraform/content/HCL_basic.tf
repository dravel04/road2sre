# https://registry.terraform.io/providers/hashicorp/local/latest/docs/resources/file
resource "local_file" "games" {
    filename = "/root/favorite-games"
    content  = "FIFA 21"
}