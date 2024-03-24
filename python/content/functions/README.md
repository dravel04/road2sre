# Funciones

## Definiciones
Cuando definimos funciones tenemos algunas opciones para declarar los argumentos:

[Ejemplo 00](00-example.py)
### `default-value arguments`
Estos son argumentos que tienen un valor predeterminado y que pueden ser omitidos al llamar a la función. Si no se proporciona un valor para estos argumentos, se utiliza el valor por defecto.
``` Python
def funcion(opcional="defecto"):
    print('Default value arguments:', opcional)

funcion()  # Salida: defecto
funcion("otro_valor")  # Salida: otro_valor
```

### `keyword-only arguments`
Estos son argumentos que sólo pueden ser especificados mediante su **nombre** (`keyword`) al llamar a la función, y no pueden ser pasados como argumentos posicionales. `*` permite especificar que los argumentos después de él deben ser de palabra clave, lo que ayuda a evitar errores al llamar a la función con argumentos mal colocados.
``` Python
def funcion(*args, clave):
    print(args)
    print(clave)

funcion(1, 2, clave="valor")
```

### `positional arguments`
Estos son argumentos que sólo pueden ser pasados como argumentos posicionales y no pueden ser especificados mediante su nombre (`keyword`) al llamar a la función.
``` Python
def funcion(posicional, *, obligatorio):
    print(posicional)
    print(obligatorio)

funcion(1, obligatorio=2)
```

### `*args` y `**kwargs`
**`*args`** recoge argumentos posicionales en una tupla. Esto significa que puedes pasar un número variable de argumentos posicionales a una función, y estos serán recogidos en una tupla dentro de la función.

**`**kwargs`** recoge argumentos de palabra clave en un diccionario. Esto permite pasar un número variable de argumentos de palabra clave a una función, y estos serán recogidos en un diccionario dentro de la función.

``` Python
def funcion(*args, **kwargs):
    print("Argumentos posicionales:", args)
    # Pueden ser recorridos
    # for arg in args:
    #     print(arg)
    print("Argumentos de palabra clave:", kwargs)
    # for key, value in kwargs.items():
    #     print(f"{key}: {value}")

funcion(1, 2, 3, nombre="Juan", edad=30)
```

## Decorators
Los decoradores en Python permiten modificar o extender el comportamiento de funciones o clases de manera transparente y elegante. Un decorador es una función que toma otra función como argumento y devuelve una función nueva. Los decoradores se utilizan comúnmente para añadir funcionalidades adicionales a funciones o métodos sin modificar su código interno.

[Ejemplo 01](01-example.py)
``` Python
def registrar(func):
    def wrapper(*args, **kwargs):
        resultado = func(*args, **kwargs)
        print(f"La función {func.__name__} fue llamada con los argumentos {args} y devuelve {resultado}")
        return resultado
    return wrapper

@registrar
def suma(a, b):
    return a + b

resultado = suma(3, 5)
# Salida:
# La función suma fue llamada con los argumentos (3, 5) y devuelve 8
print(resultado)  # Salida: 8
```
