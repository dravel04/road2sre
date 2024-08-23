import click

@click.group()
def cli():
    # La cadena de texto "Este es un grupo de comandos principal." se 
    # utiliza como descripción o documentación del comando. Cuando
    # ejecutas el script y consultas la ayuda del comando desde la línea
    # de comandos, esta cadena se mostrará como la descripción del comando.
    """Este es un grupo de comandos principal."""
    pass

@cli.command()
@click.option('--nombre', default='Mundo', help='Especifica un nombre para saludar.')
def saludar(nombre):
    """Saluda a alguien."""
    click.echo(f'Hola, {nombre}!')

@cli.command()
def despedir():
    """Se despide."""
    click.echo('Adiós!')

if __name__ == '__main__':
    cli()