# Default value arguments
def funcion(opcional="defecto"):
    print('')
    print('Default value arguments:', opcional)

funcion()  # Salida: defecto
funcion("otro_valor")  # Salida: otro_valor

# Keyword value arguments
def funcion(*args, clave):
    print('-------------------------------')
    print('Keyword value arguments:')
    print(args)
    print(clave)

funcion(1, 2, clave="valor")

# Positional arguments
def funcion(posicional, *, obligatorio):
    print('-------------------------------')
    print('Positional arguments:')
    print(posicional)
    print(obligatorio)

funcion(1, obligatorio='obligatorio')

# *args y **kwargs
def funcion(*args, **kwargs):
    print('-------------------------------')
    print("Argumentos posicionales:", args)
    # Pueden ser recorridos
    # for arg in args:
    #     print(arg)
    print("Argumentos de palabra clave:", kwargs)
    # for key, value in kwargs.items():
    #     print(f"{key}: {value}")

funcion(1, 2, 3, nombre="Juan", edad=30)
