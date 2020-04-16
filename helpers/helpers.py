"""
Helper functions to go with collect.py
"""
# Standard library imports
from pathlib import Path
import os
import shutil
import sys

# Third-party library imports
import requests


def _start_from_scratch() -> None:
    """Delete all data and start from a clean slate."""
    to_clean = [
        "__pycache__",
        "data",
        "helpers/__pycache__",
        "original_data",
        "temp",
    ]
    if user_input_confirmation():
        for directory in to_clean:
            shutil.rmtree(directory, ignore_errors=True)
        print("Everything is clean now.")
    else:
        print("Nothing happened.")
    sys.exit(0)


def do_maintenance(func) -> None:
    """Decorator to run the script while performing some cleanup operations."""

    def cleaner_wrapper():
        """Take care of creation and deletion of directories."""
        to_create = [
            "data",
            "original_data",
            "temp",
        ]
        shutil.rmtree("temp", ignore_errors=True)  # remove, there or not

        for directory in to_create:
            # we don't want to replace anything already there
            if not os.path.isdir(directory):
                os.mkdir(directory)

        func()  # main script happening here
        shutil.rmtree("temp", ignore_errors=True)

    return cleaner_wrapper


def download_dataset(dataset: str) -> None:
    """Download given file by URL based on the required `dataset`."""
    url = f"https://datacenter.prb.org/download/international/indicator/{dataset}/csv"
    save_path = f"original_data/{dataset}.csv"
    print(f"Downloading '{dataset}'...", end=" ")
    if os.path.isfile(save_path):
        print("Dataset already downloaded.")
    else:
        r = requests.get(url, allow_redirects=True)
        with open(save_path, "wb") as data_file:
            data_file.write(r.content)

        # delete the file if the retrieved dataset doesn't exist
        # (file size < 100 bytes)
        if Path(save_path).stat().st_size < 100:
            # printed on the same line containing the dataset name
            print("Dataset not found.")
            os.remove(save_path)
        else:
            print()  # when dataset is found, start a new line


def execute_on_all(iterable: list, func, setting=None) -> None:
    """Take an `iterable` and do `func` on all items in `iterable`."""
    if func is download_dataset and not setting["download"]:
        print("Skip downloading datasets.")
        return
    if func is trim_file_header:
        if not os.listdir("original_data"):
            print("[Removing header] No dataset found. Exiting.")
            sys.exit(0)
    for item in iterable:
        func(item)


def trim_file_header(filename: str, lines: int = 4) -> None:
    """Remove the first `lines` in `filename`."""
    try:
        trimmed = False
        with open(f"original_data/{filename}.csv") as input_file, open(
            f"temp/{filename}.csv", "w"
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
            print("Done.")
            os.replace(f"temp/{filename}.csv", f"original_data/{filename}.csv")
        else:
            print("No header found.")
    except FileNotFoundError:
        print(f"[Removing header] '{filename}.csv' not found. Next.")


def user_input_confirmation(
    message: str = "\nDo you want to delete all data and start from scratch? (y/n) ",
):
    """Asks the user to enter either "y" or "n" to confirm. Return boolean."""
    choice = None
    while choice is None:
        user_input = input(message)
        if user_input.lower() == "y":
            choice = True
        elif user_input.lower() == "n":
            choice = False
        else:
            print('Please enter either "y" or "n".')
    return choice
