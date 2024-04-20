# Terraform
resource "local_file" "test":
- "local" -> provider
- "file" -> resource
- "test" -> resource name

## Basic Command
- `terraform init` -> Inicia todas las dependencias asociados a nuestro espacio de trabajo y descarga los providers en caso de ser necesario
- `terraform validate` -> Revisa la sintaxis de nuestros ficheros .tf
- `terraform plan` -> Nos muestra las acciones a realizar
- `terraform apply` -> Aplica las acciones
- `terraform destroy` -> Elimina los recursos generados
- `terraform fmt` -> Nos reescribe nuestro ficheros de configuración al formato "oficial"
- `terraform output` -> Nos muestra el valor de las variables definidas
- `terraform show` -> Muestra el estado actual de nuestro proyecto
- `terraform providers` -> Muestra los providers usados en nuestro proyecto
- `terraform graph` -> Nos muestra un diagrama de dependencias de los recursos creados en nuestro proyecto
- `terraform taint` -> Marca un recurso como dañado o degrado. Será reemplazado


## [Variables](https://developer.hashicorp.com/terraform/cloud-docs/workspaces/variables)
- Archivos .tf (Archivos de Configuración de Terraform): Para definir metadata (tipo, etc)
- Archivos .tfvars (Archivos de Variables de Terraform): Para definir el contenido de la variable

### [Types](https://developer.hashicorp.com/terraform/language/expressions/types)
The Terraform language uses the following types for its values:
- **string:** a sequence of Unicode characters representing some text, like "hello".
- **number:** a numeric value. The number type can represent both whole numbers like 15 and fractional values like 6.283185.
- **bool:** a boolean value, either true or false. bool values can be used in conditional logic.
- **list (or tuple):** a sequence of values, like ["us-west-1a", "us-west-1c"]. Identify elements in a list with consecutive whole numbers, starting with zero.
- **set:** a collection of unique values that do not have any secondary identifiers or ordering.
- **map (or object):** a group of values identified by named labels, like {name = "Mabel", age = 52}.

### count vs for_each
- **count:** trata con listas, normalmente asignada a `length(var.name)`. La salida generada es `list`
- **for_each:** trata con `set`. La salida generada es `map`
```terraform
resource "local_file" "games" {
    filename = each.value
    for_each = toset(var.name)
}
```

## [Debugging](https://developer.hashicorp.com/terraform/internals/debugging)
Definiendo la variable de entorno `TF_LOG` con los valores `TRACE`,`DEBUG`,`INFO`,`WARN` o `ERROR`, podemos tener diferente grado de debug:
```shell
export TF_LOG=TRACE
```
Adicionalmente, podemos definir la variable `TF_LOG_PATH` para tener persistencia de estos logs
```shell
export TF_LOG_PATH=/path/to/log/file
```

## [Modules](https://developer.hashicorp.com/terraform/language/modules)
Encapsula recursos, variables, salidas y otros elementos relacionados. Permite crear abstracciones y componentes reutilizables.


## [Funciones](https://developer.hashicorp.com/terraform/language/functions) y [Condicionales](https://developer.hashicorp.com/terraform/language/expressions/conditionals)
- Existen funciones para manejar los recursos. Pueden ser usadas en `terraform console`
- Los condicionales usan la siguiente sintaxis `condition ? {true_val} : {false_val}`


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
- [private_key](https://registry.terraform.io/providers/hashicorp/tls/latest/docs/resources/private_key)
- [`depends_on`](https://developer.hashicorp.com/terraform/language/meta-arguments/depends_on): meta-argumento que nos garantiza que un recurso se generará después de ese del cuál de depende
- [Life Cicle](https://developer.hashicorp.com/terraform/language/meta-arguments/lifecycle)
- [Provisioners](https://developer.hashicorp.com/terraform/language/resources/provisioners/syntax)
- [Workspaces](https://developer.hashicorp.com/terraform/language/state/workspaces)

### [Curso](https://kodekloud.com/certificate-verification/2DEF3DB21713-2DEF37BC379D-2DEF377F06C5/)