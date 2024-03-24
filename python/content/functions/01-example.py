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
