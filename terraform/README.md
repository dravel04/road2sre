# Terraform
resource "local_file" "test":
- "local" -> provider
- "file" -> resource
- "test" -> resource name

## Basic Command
- `terraform init` -> Inicia todas las dependencias asociados a nuestro espacio de trabajo y descarga los providers en caso de ser necesario
- `terraform plan` -> Nos muestra las acciones a realizar
- `terraform apply` -> Aplica las acciones
- `terraform destroy` -> Elimina los recursos generados

## Links de interés
- [random_pet](https://registry.terraform.io/providers/hashicorp/random/latest/docs/resources/pet)
> La propiedad `keepers` se utiliza para definir los valores que determinarán la aleatoriedad en la generación del nombre. Cuando se proporcionan valores para `keepers`, Terraform garantiza que los nombres generados serán únicos para cada combinación de valores de `keepers`.
> Por ejemplo, si tienes un recurso `random_pet` definido de esta manera:
> ```terraform
> resource "random_pet" "my_pet" {
>   keepers = {
>     region = "us-west"
>     env    = "production"
>   }
> }
> ```
> Terraform generará un nombre de animal aleatorio, pero garantizará que el nombre generado sea único para cada combinación de valores de region y env. Esto significa que si creas otro recurso `random_pet` con diferentes valores para region y env, obtendrás un nombre diferente, pero si vuelves a crear un recurso con los mismos valores para region y env, obtendrás el mismo nombre generado anteriormente.