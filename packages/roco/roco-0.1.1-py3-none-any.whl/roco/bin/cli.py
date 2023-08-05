import sys
import click

from roco.main import generate_runtime_config
from roco.config import get_settings


@click.command()
@click.option(
    '-s',
    '--settings',
    is_flag=True,
    default=False,
    show_default=True,
    help="echo current settings"
)
def run(settings: bool):
    if settings:
        se = get_settings()
        click.echo(f"prefix = {se.Config.env_prefix}")
        click.echo(se.dict())
        sys.exit(0)

    output = generate_runtime_config()
    click.echo(output)


if __name__ == "__main__":
    run()
