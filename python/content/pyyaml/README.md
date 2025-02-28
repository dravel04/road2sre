# PyYAML

Es una librería de Python que nos permite trabajar con archivos YAML, un formato de datos muy usado en DevOps, Kubernetes, configuración de aplicaciones, etc.

## Dumper y Representer: ¿Para qué sirven?
Cuando conviertes un objeto de Python a YAML (`yaml.dump()`), PyYAML usa dos conceptos clave:
- **Dumper**: Se encarga de generar la salida YAML.
- **Representer**: Define cómo se representan los objetos de Python en YAML.

## Dumper personalizado para tabular arrays
Cuando **PyYAML** genera listas (`- elemento`), por defecto no las alinea con espacios. Un **Dumper personalizado** puede solucionar esto.

```python
import yaml

class CustomDumper(yaml.Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super().increase_indent(flow, False)

data = {
    "nombre": "Juan",
    "habilidades": ["Python", "Kubernetes", "DevOps"]
}

yaml_output = yaml.dump(data, Dumper=CustomDumper, default_flow_style=False)
print(yaml_output)
```
```yaml
nombre: Juan
habilidades:
  - Python
  - Kubernetes
  - DevOps
```
El `increase_indent` del `CustomDumper` asegura que los guiones (`-`) de las listas estén correctamente tabulado

### ¿Qué hace `increase_indent` en CustomDumper?
El método `increase_indent` de Dumper controla cómo se tabulan los elementos anidados. Cuando lo sobrescribimos:
```python
class CustomDumper(yaml.Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super().increase_indent(flow, False)
```
Estamos diciendo:
1. `flow=False`
    - `flow=True` haría que el YAML use estilo compacto (`{}` y `[]` en una línea).
    - `False` mantiene el formato multilínea.
2. `indentless=False`
    - `True` haría que las listas (`- item`) se escriban sin una sangría extra.
    - `False` asegura que los guiones estén correctamente alineados dentro de bloques.

#### Ejemplo sin este cambio:
```yaml
nombre: Juan
habilidades:
- Python
- Kubernetes
- DevOps
```
Aquí la lista (`-`) no está tabulada dentro de habilidades.

#### Ejemplo con `increase_indent` corregido:
```yaml
nombre: Juan
habilidades:
  - Python
  - Kubernetes
  - DevOps
```
Ahora los guiones (`-`) están bien alineados.


## Representer con una clase personalizada
Si intentamos convertir un objeto de una clase propia fallará:
```python
class Persona:
    def __init__(self, nombre, edad):
        self.nombre = nombre
        self.edad = edad

p = Persona("Juan", 30)
print(yaml.dump(p))
```
```yaml
!!python/object:__main__.Persona {}
```

Por lo que tenemos que crear un un **Representer** personalizado para la clase
```python
def persona_representer(dumper, obj):
    return dumper.represent_mapping("!Persona", {"nombre": obj.nombre, "edad": obj.edad})

yaml.add_representer(Persona, persona_representer)

p = Persona("Juan", 30)
yaml_output = yaml.dump(p)
print(yaml_output)
```
```yaml
!Persona
  nombre: Juan
  edad: 30
```
mediante `represent_mapping("!Persona", {"nombre": obj.nombre, "edad": obj.edad})` le decimos como tiene que interpretar la clase

##  Representer para mantener el orden de los diccionarios
Por defecto, PyYAML ordena las claves de los diccionarios. Si queremos mantener el orden en que fueron definidos, usamos `OrderedDict`.

```python
from collections import OrderedDict

def ordered_dict_representer(dumper, data):
    return dumper.represent_dict(data.items())

yaml.add_representer(OrderedDict, ordered_dict_representer)

data = OrderedDict([
    ("nombre", "Juan"),
    ("edad", 30),
    ("habilidades", ["Python", "DevOps"])
])

yaml_output = yaml.dump(data, Dumper=CustomDumper, default_flow_style=False)
print(yaml_output)
```
```yaml
nombre: Juan
edad: 30
habilidades:
  - Python
  - DevOps
```
Ahora **PyYAML** respeta el orden de las claves en lugar de ordenarlas alfabéticamente.

## Diferencia entre `represent_mapping` y `represent_dict`
Cuando creamos un Representer, tenemos que decirle a PyYAML cómo representar un tipo de objeto en YAML.

1. Para **clases personalizadas** (`Persona` en nuestro ejemplo), usamos `represent_mapping`:
```python
return dumper.represent_mapping("!Persona", {"nombre": obj.nombre, "edad": obj.edad})
```
- Aquí `!Persona` es una etiqueta que se agrega en YAML para indicar que es un objeto especial.
- `represent_mapping` convierte la estructura en un diccionario YAML.

2. Para `OrderedDict`, usamos `represent_dict`:
```python
return dumper.represent_dict(data.items())
```
- No necesitamos una etiqueta especial como `!Persona` porque `OrderedDict` ya es un diccionario.
- `represent_dict(data.items())` lo convierte en un YAML con el mismo orden en que fue definido.

### ¿Por qué `represent_dict` y no `represent_mapping`?
`represent_dict` es más directo para diccionarios normales. `represent_mapping` se usa cuando queremos un mapeo con una etiqueta especial.

## 🎯 Resumen
`represent_dict(data.items())` → Para `OrderedDict`, mantiene el orden de las claves.
`represent_mapping("!Clase", {...})` → Para clases personalizadas, agrega etiquetas YAML.
`increase_indent(flow, False)` → Asegura que las listas (`- item`) tengan la tabulación correcta.