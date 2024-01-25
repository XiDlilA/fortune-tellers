from model.DateInfo import *
import click 


@click.command()
@click.option('--today/--no-today', default=False, help='Show today info')
def info(today):
    if today:
        API().today()


info()
