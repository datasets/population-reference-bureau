"""
Retrieve and process data from PRB — https://www.prb.org/
"""
# Third-party library imports
# pylint: disable=no-value-for-parameter
import click

# Local imports
from helpers.helpers import (
    _start_from_scratch,
    delete_empty_rows,
    do_maintenance,
    download_data,
    execute_on_all,
    location_is_US,
    trim_file_header,
)

# Main entry point on top of which other commands are created
@click.group()
def ccli():
    "Retrieve and process data from PRB — https://www.prb.org/"
    pass


@click.command()
def run():
    """Retrieve and process data from PRB — https://www.prb.org/"""
    click.secho(
        "You are about to download and process your data.",
        fg="blue",
        bold=True,
    )
    if click.confirm(
        "Are you sure you want to continue?",
        default=False,
        abort=True,
        prompt_suffix=": ",
        show_default=True,
        err=False,
    ):
        pass

@ccli.command()
@click.argument("location", type=click.Choice(["us", "international"]))
def delempty(location):
    """Delete empty rows in CSV files."""
    execute_on_all(location, delete_empty_rows)

@ccli.command()
@click.argument("location", type=click.Choice(["us", "international"]))
def download(location):
    """Retrieve data from source."""
    execute_on_all(location, download_data)


@ccli.command()
def reset():
    """Delete all data and start from a clean slate."""
    _start_from_scratch()


@ccli.command()
@click.argument("location", type=click.Choice(["us", "international"]))
def trimheaders(location):
    """Remove superfluous header lines in CSV files."""
    execute_on_all(location, trim_file_header)
    pass


if __name__ == "__main__":
    ccli()
