"""
Retrieve and process data from PRB — https://www.prb.org/
"""

# Standard library imports
from pathlib import Path
import csv
import fileinput
import os
import shutil
import subprocess
import sys

# Third-party library imports
import pandas as pd
import requests

# Local imports
from scripts.settings import (
    DATA_INTER,
    DATA_US,
    DIRS,
    LOCATIONS,
)


def clean_data(filename: str, location: str) -> None:
    """Use Pandas to clean data. Replace NA values, sort, combine columns,
    reset index to new combined column."""
    clean_directory, _, processing_directory = set_location_dirs(location)
    na_vals = ["n/a"]
    df = pd.read_csv(
        f"{processing_directory}/{filename}.csv", na_values=na_vals,
    )
    df.sort_values(by=["Name", "TimeFrame"], inplace=True)

    # Remove leading zeros in column FIPS to convert to valid integers
    df["NameFIPS"] = df["Name"] + " - " + df["FIPS"]
    df.set_index("NameFIPS", inplace=True)
    df.drop(columns=["FIPS", "Name"], inplace=True)

    exported_file = f"{clean_directory}/{filename}.csv"
    df.to_csv(exported_file)
    print(f"Exported {exported_file}")


def delete_empty_rows(filename: str, location: str) -> None:
    """Delete empty lines in file located at `filepath`."""
    _, _, processing_directory = set_location_dirs(location)
    filepath = f"{processing_directory}/{filename}.csv"
    temp_file = f"{DIRS['temp_dir']}/{filename}.csv"
    try:
        with open(filepath) as in_file, open(temp_file, "w") as out_file:
            writer = csv.writer(out_file)
            for row in csv.reader(in_file):
                if row:
                    writer.writerow(row)
        os.replace(temp_file, filepath)
    except FileNotFoundError:
        print(f"[Deleting empty lines] '{filepath}' not found. Next.")


def run() -> None:
    """Retrieve and clean everything in one go."""
    for location in LOCATIONS:
        print(f"\n\nWorking with {location.upper()} data...\n")
        execute_on_all(location, download_data)
        execute_on_all(location, trim_file_header)
        execute_on_all(location, delete_empty_rows)
        execute_on_all(location, clean_data)
        truncate_csvs(location)

    package_data()


def download_data(filename: str, url_bit: str) -> None:
    """Download given file from `url_bit` based on the required `filename`."""
    url = f"https://datacenter.prb.org/download/{url_bit}/indicator/{filename}/csv/"
    save_file = f"{filename}.csv"
    if url_bit == DATA_US["url_bit"]:
        save_dir = f"{DIRS['original_data_us']}/"
    else:
        save_dir = f"{DIRS['original_data_inter']}/"
    save_path = f"{save_dir}{save_file}"

    print(f"{save_dir}{save_file}")

    if os.path.isfile(save_path):
        print("Data already downloaded.\n")
    else:
        request = requests.get(url, allow_redirects=True)
        with open(save_path, "wb") as data_file:
            data_file.write(request.content)

        # delete the file if the retrieved dataset doesn't exist
        # (file size < 1000 bytes)
        if Path(save_path).stat().st_size < 1000:
            # printed on the same line containing the dataset name
            print("DATA NOT FOUND.\n")
            os.remove(save_path)


def execute_on_all(location: str, func) -> None:
    """Take a `location` and do `func` on all items in that location."""
    func_arg = location
    if func is download_data:
        if location_is_US(location):
            func_arg = DATA_US["url_bit"]
        else:
            func_arg = DATA_INTER["url_bit"]
        print("Downloading data")

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


def folder_is_empty(folder_name: str) -> bool:
    """Return bool as to whether `folder_name` is empty."""
    return os.listdir(DIRS[folder_name]) == []


def location_is_US(source_name: str) -> bool:
    """Return bool as to whether `source_name` equals "us" or not."""
    return source_name == "us"


def package_data() -> None:
    """Create datapackage.json in data/ folder."""
    # Run `data init``in truncate_data dir
    subprocess.run(["data", "init", DIRS["truncate_data"]], check=True)

    datapackage = f"{DIRS['truncate_data']}/datapackage.json"
    dst_package = f"{DIRS['clean_data']}/datapackage.json"

    # Make quick passes through datapackage.json for easy substitution
    with fileinput.FileInput(datapackage, inplace=True) as filename:
        for line in filename:
            print(
                line.replace("truncate_data", "population_reference_bureau"),
                end="",
            )
    with fileinput.FileInput(datapackage, inplace=True) as filename:
        for line in filename:
            print(
                line.replace("Truncate_data", "Population-Reference-Bureau"),
                end="",
            )
    with fileinput.FileInput(datapackage, inplace=True) as filename:
        for line in filename:
            print(line.replace("scripts/population_reference_bureau/", ""), end="")

    os.replace(datapackage, dst_package)

    # Validate datapackage
    subprocess.run(["data", "validate", DIRS["clean_data"]], check=True)


def set_location_dirs(location: str) -> tuple:
    """Return a tuple containing directory settings for a given `location`."""
    if location_is_US(location):
        clean_directory = DIRS["clean_data_us"]
        original_directory = DIRS["original_data_us"]
        processing_directory = DIRS["processed_data_us"]
    else:
        clean_directory = DIRS["clean_data_inter"]
        original_directory = DIRS["original_data_inter"]
        processing_directory = DIRS["processed_data_inter"]
    return (clean_directory, original_directory, processing_directory)


def trim_file_header(filename: str, location: str, lines: int = 4) -> None:
    """Remove the first `lines` in `filename` for `location`."""
    (_, original_directory, processing_directory,) = set_location_dirs(
        location
    )
    try:
        trimmed = False
        with open(f"{original_directory}/{filename}.csv") as input_file, open(
            f"{DIRS['temp_dir']}/{filename}.csv", "w"
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
                f"{DIRS['temp_dir']}/{filename}.csv",
                f"{processing_directory}/{filename}.csv",
            )
            print("Done.")
        else:
            print("No header found.")
    except FileNotFoundError:
        print(f"[Removing header] '{filename}.csv' not found. Next.")


def truncate_csvs(location: str, lines: int = 20) -> None:
    """Truncate a CSV file to retain only the first `lines` of each file.
    Return a str of affected directory for further processing."""
    if location_is_US(location):
        clean_directory = "clean_data_us"
        truncate_dir = "truncate_data_us"
        save_dir = DIRS[truncate_dir]
    else:
        clean_directory = "clean_data_inter"
        truncate_dir = "truncate_data_inter"
        save_dir = DIRS[truncate_dir]

    if folder_is_empty(clean_directory):
        print(f"[Truncating {location}] No clean data found.")
        sys.exit(0)

    for file in os.listdir(DIRS[clean_directory]):
        filename = os.fsdecode(file)
        if filename.endswith(".csv"):
            filepath = f"{DIRS[clean_directory]}/{filename}"
            save_file = f"{save_dir}/{filename}"
            try:
                os.mkdir(DIRS["truncate_data"])
            except FileExistsError:
                pass
            try:
                os.mkdir(save_dir)
            except FileExistsError:
                pass
            with open(filepath) as in_file, open(save_file, "w") as out_file:
                writer = csv.writer(out_file)
                for index, row in enumerate(csv.reader(in_file)):
                    if row and index < lines:
                        writer.writerow(row)


if __name__ == "__main__":
    run()
