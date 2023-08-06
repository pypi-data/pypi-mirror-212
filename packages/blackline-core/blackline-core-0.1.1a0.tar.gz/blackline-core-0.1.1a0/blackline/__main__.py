"""Main entry point for Databricks"""

from blackline.cli import cli


def main() -> None:
    """Calls blackline CLI."""
    cli.cli(auto_envvar_prefix="BLACKLINE")
