# from click.testing import CliRunner


# from lancet.commands.configuration import setup


# def test_setup_command():
#     data = {
#         "gitlab_user": "cli_user",
#         "timer_id": "12345",
#         "timer_user": "67890",
#     }
#     with runner.isolated_filesystem():
#         runner = CliRunner()
#         result = runner.invoke(setup, [], input=data)
    # assert result.exit_code == 0


import click

@click.command()
@click.argument('name')
def hello(name):
   click.echo('Hello %s!' % name)

from click.testing import CliRunner

def test_hello_world():
  runner = CliRunner()
  result = runner.invoke(hello, ['Peter'])
  assert result.exit_code == 0
  assert result.output == 'Hello Peter!\n'
