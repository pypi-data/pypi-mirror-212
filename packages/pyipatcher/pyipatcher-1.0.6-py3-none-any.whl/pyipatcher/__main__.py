import click
from .cli.ramdiskpatcher import ramdiskpatcher
from .cli.kernelpatcher import kernelpatcher

@click.group()
def cli():
    pass
   
cli.add_command(ramdiskpatcher)
cli.add_command(kernelpatcher)

cli.context_settings = dict(help_option_names=['-h', '--help'])