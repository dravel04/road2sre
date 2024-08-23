from setuptools import setup

setup(
    name='clickDemo',
    version='1.0.0',
    py_modules=['clickDemo'],
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'clickDemo = clickDemo:cli',
        ],
    },
)

# name: Especifica el nombre del paquete. En este caso, el paquete se llama clickDemo.
# version: Define la versión del paquete. Aquí, el paquete tiene la versión 1.0.0.
# py_modules: Una lista de módulos de Python que están incluidos en el paquete. En este caso, solo hay un módulo llamado clickDemo.
# install_requires: Enumera las dependencias que debe instalar pip cuando se instala el paquete. En este ejemplo, el paquete requiere la biblioteca Click.
# entry_points: Define puntos de entrada para el paquete. En este caso, está utilizando la sección 'console_scripts', que es específica de la creación de scripts de consola.
# 'console_scripts': Indica que estás creando scripts de consola ejecutables.
# 'clickDemo = clickDemo:cli': Define el nombre del script de consola (clickDemo) y el punto de entrada al que apunta (clickDemo:cli). Esto significa que cuando ejecutas el script de consola clickDemo, se llamará a la función cli en el módulo clickDemo.