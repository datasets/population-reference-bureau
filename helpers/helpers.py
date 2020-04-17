"""
Helper functions to go with collect.py
"""
# Standard library imports
from pathlib import Path
import csv
import os
import shutil
import sys

# Third-party library imports
import click
import requests

# Local imports
from .settings import (
    DATA_INTER,
    DATA_US,
    FOLDERS_TO_CLEAN,
    FOLDERS_TO_CREATE,
    LOCATIONS,
    SETTINGS,
)


def delete_empty_rows(filename: str, location: str):
    """Delete empty lines in file located at `filepath`."""
    _, processing_directory = set_location_dirs(location)
    filepath = f"{processing_directory}/{filename}.csv"
    temp_file = f"{SETTINGS['temp_dir']}/{filename}.csv"
    try:
        with open(filepath) as in_file, open(temp_file, "w") as out_file:
            writer = csv.writer(out_file)
            for row in csv.reader(in_file):
                if row:
                    writer.writerow(row)
        os.replace(temp_file, filepath)
    except FileNotFoundError:
        print(f"[Deleting empty lines] '{filepath}' not found. Next.")


def _start_from_scratch() -> None:
    """Delete all data and start from a clean slate."""
    if click.confirm(
        "Do you want to delete all data and start from scratch?",
        default=False,
        abort=True,
        prompt_suffix=": ",
        show_default=True,
        err=False,
    ):
        for directory in FOLDERS_TO_CLEAN:
            shutil.rmtree(directory, ignore_errors=True)
        click.secho("Everything is clean now.", fg="green", bold="True")
    sys.exit(0)


def do_maintenance(func, *args, **kwargs):
    """Decorator to run the script while performing some cleanup operations."""

    def cleaner_wrapper(*args, **kwargs):
        """Take care of creation and deletion of directories."""
        shutil.rmtree(
            SETTINGS["temp_dir"], ignore_errors=True
        )  # remove, there or not

        for directory in FOLDERS_TO_CREATE:
            # we don't want to touch anything already there
            if not os.path.isdir(directory):
                os.mkdir(directory)

        func(*args, **kwargs)  # main script happening here

        shutil.rmtree(SETTINGS["temp_dir"], ignore_errors=True)

    return cleaner_wrapper


def download_data(filename: str, url_bit: str) -> None:
    """Download given file from `url_bit` based on the required `filename`."""
    url = f"https://datacenter.prb.org/download/{url_bit}/indicator/{filename}/csv/"
    save_file = f"{filename}.csv"
    if url_bit == DATA_US["url_bit"]:
        save_dir = f"{SETTINGS['original_data_us']}/"
    else:
        save_dir = f"{SETTINGS['original_data_inter']}/"
    save_path = f"{save_dir}{save_file}"

    click.echo(
        click.style(save_dir, fg="blue") + click.style(save_file, fg="cyan")
    )

    if os.path.isfile(save_path):
        click.secho("Data already downloaded.\n", fg="blue", bold=True)
    else:
        request = requests.get(url, allow_redirects=True)
        with open(save_path, "wb") as data_file:
            data_file.write(request.content)

        # delete the file if the retrieved dataset doesn't exist
        # (file size < 1000 bytes)
        if Path(save_path).stat().st_size < 1000:
            # printed on the same line containing the dataset name
            click.secho("DATA NOT FOUND.\n", fg="yellow", bold=True)
            os.remove(save_path)


@do_maintenance
def execute_on_all(location: str, func) -> None:
    """Take a `location` and do `func` on all items in that location."""
    func_arg = location
    if func is download_data:
        if location_is_US(location):
            func_arg = DATA_US["url_bit"]
        else:
            func_arg = DATA_INTER["url_bit"]
        click.secho("Downloading data", fg="green", bold=True)

    if func is trim_file_header:
        if location_is_US(location):
            if folder_is_empty("original_data_us"):
                print("[Removing US header] No dataset found. Exiting.")
                sys.exit(0)
        else:
            if folder_is_empty("original_data_inter"):
                print(
                    "[Removing international header] No dataset found. Exiting."
                )
                sys.exit(0)

    if func is delete_empty_rows:
        if location_is_US(location):
            if folder_is_empty("processed_data_us"):
                print(
                    "[Deleting empty lines for US] No dataset found. Exiting."
                )
                sys.exit(0)
        else:
            if folder_is_empty("processed_data_inter"):
                print(
                    "[Deleting empty lines for international] No dataset found. Exiting."
                )
                sys.exit(0)

    for item in LOCATIONS[location]:
        func(item, func_arg)


def set_location_dirs(location: str) -> tuple:
    if location_is_US(location):
        original_directory = SETTINGS["original_data_us"]
        processing_directory = SETTINGS["processed_data_us"]
    else:
        original_directory = SETTINGS["original_data_inter"]
        processing_directory = SETTINGS["processed_data_inter"]
    return (original_directory, processing_directory)


def trim_file_header(filename: str, location: str, lines: int = 4) -> None:
    """Remove the first `lines` in `filename` for `location`."""
    original_directory, processing_directory = set_location_dirs(location)
    try:
        trimmed = False
        with open(f"{original_directory}/{filename}.csv") as input_file, open(
            f"{SETTINGS['temp_dir']}/{filename}.csv", "w"
        ) as output_file:
            first_line = input_file.readline()
            print(f"[Removing header] '{filename}'...", end=" ")
            if not first_line.startswith("FIPS"):  # file needs to be trimmed
                input_file.seek(0)  # reset position to first line
                for _ in range(lines):
                    next(input_file)  # discard header lines
                for line in input_file:  # save remaining lines
                    output_file.write(line)
                trimmed = True
        if trimmed:  # only replace if the file has been trimmed
            os.replace(
                f"{SETTINGS['temp_dir']}/{filename}.csv",
                f"{processing_directory}/{filename}.csv",
            )
            print("Done.")
        else:
            print("No header found.")
    except FileNotFoundError:
        print(f"[Removing header] '{filename}.csv' not found. Next.")


def location_is_US(source_name: str) -> bool:
    return source_name == "us"


def folder_is_empty(folder_name: str) -> bool:
    return os.listdir(SETTINGS[folder_name]) == []
