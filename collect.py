"""
Retrieve and process data from PRB — https://www.prb.org/
"""
# Third-party library imports
# pylint: disable=no-value-for-parameter
import click

# Local imports
from helpers.helpers import (
    _start_from_scratch,
    clean_data,
    delete_empty_rows,
    do_everything,
    download_data,
    execute_on_all,
    package_data,
    trim_file_header,
    truncate_csvs,
)

# Main entry point on top of which other commands are created
@click.group()
def ccli():
    """Retrieve and process data from PRB — https://www.prb.org/

    To perform all actions at once, use the `everything` command (recommended
    option)."""
    pass


@ccli.command()
@click.argument("location", type=click.Choice(["us", "international"]))
def clean(location):
    """Clean data with Pandas (sort and output to data/ folder)."""
    execute_on_all(location, clean_data)
    pass


@ccli.command()
@click.argument("location", type=click.Choice(["us", "international"]))
def delempty(location):
    """Delete empty rows in CSV files."""
    execute_on_all(location, delete_empty_rows)


@ccli.command()
@click.argument("reset", type=click.Choice(["reset", "noreset"]))
def everything(reset):
    """reset + retrieve + process + clean in one go.

    Specify if old data should be removed first with `reset`/`noreset`."""
    do_everything(reset)


@ccli.command()
def package():
    """Create datapackage.json in population_reference_bureau/."""
    package_data()


@ccli.command()
def reset():
    """Delete all data and start from a clean slate."""
    _start_from_scratch()


@ccli.command()
@click.argument("location", type=click.Choice(["us", "international"]))
def retrieve(location):
    """Retrieve data from source."""
    execute_on_all(location, download_data)


@ccli.command()
@click.argument("location", type=click.Choice(["us", "international"]))
def trimheaders(location):
    """Remove superfluous header lines in CSV files."""
    execute_on_all(location, trim_file_header)


@ccli.command()
@click.argument("location", type=click.Choice(["us", "international"]))
def truncate(location):
    """Keep first 20 lines of clean CSV files."""
    truncate_csvs(location)


if __name__ == "__main__":
    ccli()
