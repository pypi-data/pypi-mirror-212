import click
from click import ClickException

from .config import config
from .users import UserServiceV1


@click.group()
def cli():
    pass


@click.command()
@click.option("--username")
@click.option("--password")
def login(username, password):
    if not (username and password):
        raise ClickException("You must provide both --username and --password options.")
    login_response = UserServiceV1().login(username, password)

    with open(config.credentials_path, 'w') as f:
        f.write(f'COMPUTEX_ACCESS_TOKEN={login_response.access_token}\n')
        f.write(f'COMPUTEX_REFRESH_TOKEN={login_response.refresh_token}\n')

    click.echo("Successfully logged in. Welcome to ComputeX.")


cli.add_command(login)


if __name__ == "__main__":
    cli()
