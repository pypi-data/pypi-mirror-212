import click

from firmitas import __vers__, readconf
from firmitas.base.maintool import gonotify, probedir


@click.command(name="firmitas")
@click.option(
    "-c",
    "--conffile",
    "conffile",
    type=click.Path(exists=True),
    help="Read configuration from the specified Python file",
    default=None,
)
@click.version_option(version=__vers__, prog_name="firmitas")
def main(conffile=None):
    if conffile:
        confdict = {}
        with open(conffile, "r") as confobjc:
            exec(compile(confobjc.read(), conffile, "exec"), confdict)
        readconf(confdict)
    probedir()
    gonotify()
