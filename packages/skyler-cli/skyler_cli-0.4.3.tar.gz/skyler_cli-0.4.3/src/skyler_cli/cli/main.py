import typer
from ..core.bootstrap.system import SystemBootstrapper, OS, MachineType

help_msg = "Skyler CLI: The multitool I always wanted to build myself"
app = typer.Typer(
    help=help_msg,
    no_args_is_help=True,
)


@app.command()
def main():
    print("Hello World!")


@app.command()
def setup_configs(
    os: OS = typer.Option(..., prompt="Select your OS"),
    machine_type: MachineType = typer.Option(
        ..., prompt="What type of machine is this?"
    ),
    personal_machine: bool = typer.Option(
        ..., prompt="Is this a personal machine (as opposed to one for work)"
    ),
    dryrun: bool = typer.Option(False, is_flag=True),
):
    bootstrapper = SystemBootstrapper(os, machine_type, is_personal=personal_machine)
    if dryrun:
        print(
            f"Dryrun! Would have set up the system with: {os=} {machine_type=} {personal_machine=}"
        )
        return

    bootstrapper.bootstrap_system()


if __name__ == "__main__":
    app()
