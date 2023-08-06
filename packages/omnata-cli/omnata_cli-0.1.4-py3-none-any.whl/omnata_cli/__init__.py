from pathlib import Path
import typer
from snowcli import config
from snowcli.config import AppConfig


app = typer.Typer(context_settings={"help_option_names": ["-h", "--help"]})

@app.command()
def docs():
    """Open the Omnata CLI documentation in your browser."""
    typer.launch("https://docs.omnata.com")
try:
    from omnata_plugin_devkit import cli # 

    # If the import is successful, we can add its commands to our application
    # Assume `external_command` is the command you want to include from the external package
    app.add_typer(cli.app, name="plugin_dev")

except ImportError:
    @app.command()
    def plugin_dev():
        "To use the plugin-dev subcommand, run `pip install omnata_plugin_devkit`."
        print("To use the plugin-dev subcommand, run `pip install omnata_plugin_devkit`.")
        raise typer.Abort()


def check_env_conf(env_conf,environment):
    if env_conf is None:
        print(
            f"The {environment} environment is not configured in app.toml "
            f"yet, please run `snow configure {environment}` first before continuing.",
        )
        raise typer.Abort()