import logging
from datetime import datetime
from pathlib import Path

import click
from blackline.constants import DEFAULT_PROFILE, SAMPLE_PROJECT_NAME
from blackline.exceptions import InvalidDatsetError
from blackline.execution.debug import Debug
from blackline.execution.deidentify import deidentify
from blackline.execution.demo import Demo, create_demo
from blackline.execution.report import create_report
from blackline.execution.validate import Validate
from blackline.project.init import InitProject
from blackline.version import __version__

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def default_project_dir() -> Path:
    """Return the default project directory."""
    return Path.cwd()


debug_flag = click.option("--debug/--no-debug", default=False, help="Debug mode")

version = click.option("--version", "-v", is_flag=True, help="Show blackline version")

project_dir = click.option(
    "--project-dir",
    "-p",
    type=Path,
    default=default_project_dir(),
    show_default=True,
    help="Project directory, where blackline_project.yml is located",
)
sample_project_dir = click.option(
    "--project-dir",
    "-p",
    type=Path,
    default=Path(default_project_dir(), "blackline_sample"),
    show_default=True,
    help="Project directory, where blackline_project.yml is located",
)
name = click.option(
    "--name",
    "-n",
    type=str,
    default="blackline",
    show_default=True,
    help="Project name",
)
name_sample = click.option(
    "--name",
    "-n",
    type=str,
    default=SAMPLE_PROJECT_NAME,
    show_default=True,
    help="Project name",
)

profile = click.option(
    "--profile", type=str, required=True, help="Data stores profile to use"
)

start_date = click.option(
    "--start-date",
    type=click.DateTime(),
    default=datetime.now().strftime("%Y-%m-%d"),
    show_default=True,
    help="Start date for deidentification",
)

default_profile = click.option(
    "--default-profile",
    type=str,
    default=DEFAULT_PROFILE,
    show_default=True,
    help="Default profile to use",
)
catalogue_path = click.option(
    "--catalogue-path",
    type=Path,
    default="catalogue",
    show_default=True,
    help="Path to the catalogue folder",
)
adapters_path = click.option(
    "--adapters-path",
    type=Path,
    default="adapters",
    show_default=True,
    help="Path to the adapters folder",
)

overwrite = click.option(
    "--overwrite/--no-overwrite",
    default=False,
    show_default=True,
    help="Overwrite existing project",
)

data_only = click.option(
    "--data-only/--no-data-only",
    default=False,
    show_default=True,
    help="Only create a sample sqlite database",
)


def echo_validation(exceptions) -> None:
    click.secho(f"Validating dataset definitions for profile: {profile}", bold=False)
    for key, validation in exceptions.items():
        click.secho(f"Dataset: {key}:", bold=False)
        _excs = []
        for collection_key, collection_validation in validation.collections.items():
            click.secho(f"  Collection: {collection_key}:", bold=False)
            click.secho(
                "    Collection found: True"
                if collection_validation.not_found is None
                else "    Collection found: False => {collection_validation.not_found}",  # noqa
                fg="green" if collection_validation.not_found is None else "red",
            )
            if collection_validation.not_found is not None:
                _excs.append(collection_validation.not_found)
            for field_key, field_validation in collection_validation.fields.items():
                click.secho(f"    Field: {field_key}:", bold=False)
                click.secho(
                    "       Field found: True"
                    if field_validation.not_found is None
                    else f"      Field found: False => {field_validation.not_found}",  # noqa
                    fg="green" if field_validation.not_found is None else "red",
                )
                click.secho(
                    "       Invalid field constraint: False"
                    if field_validation.invalid_constraint is None
                    else f"      Invalid field constraint: True => {field_validation.invalid_constraint}",  # noqa
                    fg="green"
                    if field_validation.invalid_constraint is None
                    else "red",
                )
                if field_validation.not_found is not None:
                    _excs.append(field_validation.not_found)
                if field_validation.invalid_constraint is not None:
                    _excs.append(field_validation.invalid_constraint)
        if _excs:
            click.secho("  Exceptions:", bold=False)
            for exc in _excs:
                click.secho(f"    {exc}", fg="red")
            raise InvalidDatsetError(
                f"Invalid dataset definition, experiences {len(_excs)} exceptions."
            )
        else:
            click.secho("  Exceptions:", bold=False)
            click.secho("      None!", fg="green")


@click.version_option(package_name="blackline-core", prog_name="blackline-core")
@click.group(
    invoke_without_command=True,
    help=f"Blackline CLI version {__version__}",
    no_args_is_help=True,
)
@click.pass_context
@debug_flag
def cli(ctx, debug):
    if ctx.invoked_subcommand is None:
        if debug:
            click.echo("Debug mode is %s" % ("on" if debug else "off"))


@cli.command(help="Initialize a project.", no_args_is_help=False)
@project_dir
@name
@default_profile
@catalogue_path
@adapters_path
def init(project_dir, name, default_profile, catalogue_path, adapters_path):
    project = InitProject(
        path=project_dir,
        name=name,
        default_profile=default_profile,
        catalogue=catalogue_path,
        adapters=adapters_path,
    )
    project.init_project()
    click.echo(f"Initialized blackline project at: {project_dir}")


@cli.command(help="Run project.", no_args_is_help=True)
@profile
@project_dir
@start_date
def run(profile, project_dir, start_date):
    click.echo(f"Running project: {project_dir}")
    click.echo(f"Running profile: {profile}")
    click.echo(f"Running start date: {start_date}")
    excs = deidentify(path=project_dir, profile=profile, start_date=start_date)
    if excs:
        excs = Validate(path=project_dir, profile=profile).validate_catalogue_dataset()
        echo_validation(exceptions=excs)
    click.echo(f"Finished project: {project_dir}")


@cli.command(help="Test data store connections.", no_args_is_help=True)
@profile
@project_dir
def debug(profile, project_dir):
    debug = Debug(path=project_dir, profile=profile)
    result = debug.debug()
    click.secho(f"Testing connections for profile: {profile}", bold=False)
    for name, status in result.items():
        click.secho(
            f"  {name}: good" if status else f"  {name}: no connection",
            fg="green" if status else "red",
        )
    excs = Validate(path=project_dir, profile=profile).validate_catalogue_dataset()
    echo_validation(exceptions=excs)


@cli.command(help="Create a sample project.", no_args_is_help=False)
@sample_project_dir
@name_sample
@overwrite
@default_profile
@data_only
def sample(project_dir, name, overwrite, default_profile, data_only):
    if data_only:
        project_dir.mkdir(parents=True, exist_ok=True)
        Demo(path=project_dir, overwrite=overwrite).create_database()
        click.echo(f"Created sample data at: {project_dir}")
        return
    create_demo(
        path=project_dir,
        name=name,
        overwrite=overwrite,
        default_profile=default_profile,
    )
    click.echo(f"Created sample project at: {project_dir}")


@cli.command(help="Report the defined project.", no_args_is_help=False)
@project_dir
def report(project_dir):
    project, stores, catalogue = create_report(path=project_dir)

    click.secho("=" * 80, fg="magenta")
    click.secho("Project Settings:", fg="magenta")
    click.echo(f"Project name: {project.name}")
    click.echo(f"Project Root: {project.project_root}")
    click.echo(f"Adapters path: {project.adapters_path}")
    click.echo(f"Catalogue path: {project.catalogue_path}")
    click.echo(f"Default profile: {project.default_profile}")
    click.echo("")
    click.secho("Data Stores:", fg="magenta")
    for store in stores:
        click.echo("Data Store: " + click.style(f"{store.name}", fg="blue"))
        click.echo("Profiles:")
        for profile, value in store.profiles.items():
            click.echo(f"  {profile}")
            click.echo(f"    Type: {value.type}")
            click.echo(f"    Adapter: {value.adapter}")
            click.echo("    Config:")
            click.echo("      Connection:")
            for conn_key, conn_value in value.config.connection.dict().items():
                click.echo(f"        {conn_key}: {conn_value}")
    click.echo("")
    click.secho("Catalogue:", fg="magenta")
    click.secho("...")


if __name__ == "__main__":
    cli(auto_envvar_prefix="BLACKLINE")
