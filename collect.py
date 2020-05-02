"""
Retrieve and process data from PRB — https://www.prb.org/
"""

# Standard library imports
from pathlib import Path
import csv
import os
import sys

# Third-party library imports
import requests
from dataflows import (
    Flow,
    PackageWrapper,
    ResourceWrapper,
    add_field,
    delete_fields,
    dump_to_path,
    load,
    set_type,
    validate,
)

# Local imports
from scripts import settings

# Hack to send data to change_path function without using additional parameters
FILE_NAME = None

def change_path(package: PackageWrapper):
    """Change the path to nest data in the subdirectory data/."""
    package.pkg.descriptor["resources"][0]["path"] = f"data/{FILE_NAME}.csv"
    yield package.pkg
    res_iter = iter(package)
    try:
        first: ResourceWrapper = next(res_iter)
    except StopIteration:
        pass
    yield first.it
    yield from package


def clean_data(filename: str, location: str) -> None:
    """Clean and validate data with `dataflows`, creating data packages in the
    process, one for each file."""
    global FILE_NAME
    FILE_NAME = f"{location}_{filename}"
    clean_directory, _, processing_directory = set_location_dirs(location)
    exported_file = f"{clean_directory}/{filename}"
    _ = Flow(
        load(
            f"{processing_directory}/{filename}.csv",
            name=f"{location}_{filename}",
        ),
        change_path,
        add_field("NameFIPS", "string"),
        concat_name_columns,
        delete_fields(["Name", "FIPS"]),
        set_type("Data", type="any"),
        validate(),
        dump_to_path(exported_file),
    ).process()[1]


def concat_name_columns(row: dict) -> None:
    """Merge content of columns 'FIPS' and 'Name' into new column 'NameFIPS'."""
    row["NameFIPS"] = f"{row['Name']} {row['FIPS']}"


def delete_empty_rows(filename: str, location: str) -> None:
    """Delete empty lines in file located at `filepath`."""
    _, _, processing_directory = set_location_dirs(location)
    filepath = f"{processing_directory}/{filename}.csv"
    temp_file = f"{settings.DIRS['temp_dir']}/{filename}.csv"
    try:
        with open(filepath) as in_file, open(temp_file, "w") as out_file:
            writer = csv.writer(out_file)
            for row in csv.reader(in_file):
                if row:
                    writer.writerow(row)
        os.replace(temp_file, filepath)
    except FileNotFoundError:
        print(f"[Deleting empty lines] '{filepath}' not found. Next.")


def download_data(filename: str, url_bit: str) -> None:
    """Download given file from `url_bit` based on the required `filename`."""
    url = f"https://datacenter.prb.org/download/{url_bit}/indicator/{filename}/csv/"
    save_file = f"{filename}.csv"
    if url_bit == settings.DATA_US["url_bit"]:
        save_dir = f"{settings.DIRS['original_data_us']}/"
    else:
        save_dir = f"{settings.DIRS['original_data_inter']}/"
    save_path = f"{save_dir}{save_file}"

    if not os.path.isfile(save_path):
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
        if location_is_us(location):
            func_arg = settings.DATA_US["url_bit"]
        else:
            func_arg = settings.DATA_INTER["url_bit"]

    if func is trim_file_header:
        if location_is_us(location):
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
        if location_is_us(location):
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

    for item in settings.LOCATIONS[location]:
        func(item, func_arg)


def folder_is_empty(folder_name: str) -> bool:
    """Return bool as to whether `folder_name` is empty."""
    return os.listdir(settings.DIRS[folder_name]) == []


def location_is_us(source_name: str) -> bool:
    """Return bool as to whether `source_name` equals "us" or not."""
    return source_name == "us"


def set_location_dirs(location: str) -> tuple:
    """Return a tuple containing directory settings for a given `location`."""
    if location_is_us(location):
        clean_directory = settings.DIRS["clean_data_us"]
        original_directory = settings.DIRS["original_data_us"]
        processing_directory = settings.DIRS["processed_data_us"]
    else:
        clean_directory = settings.DIRS["clean_data_inter"]
        original_directory = settings.DIRS["original_data_inter"]
        processing_directory = settings.DIRS["processed_data_inter"]
    return (clean_directory, original_directory, processing_directory)


def trim_file_header(filename: str, location: str, lines: int = 4) -> None:
    """Remove the first `lines` in `filename` for `location`."""
    (_, original_directory, processing_directory,) = set_location_dirs(
        location
    )
    try:
        trimmed = False
        with open(f"{original_directory}/{filename}.csv") as input_file, open(
                f"{settings.DIRS['temp_dir']}/{filename}.csv", "w"
        ) as output_file:
            first_line = input_file.readline()
            if not first_line.startswith("FIPS"):  # file needs to be trimmed
                input_file.seek(0)  # reset position to first line
                for _ in range(lines):
                    next(input_file)  # discard header lines
                for line in input_file:  # save remaining lines
                    output_file.write(line)
                trimmed = True
        if trimmed:  # only replace if the file has been trimmed
            os.replace(
                f"{settings.DIRS['temp_dir']}/{filename}.csv",
                f"{processing_directory}/{filename}.csv",
            )
        else:
            print(f"No header found in {filename}.csv.")
    except FileNotFoundError:
        print(f"[Removing header] '{filename}.csv' not found. Next.")


def run() -> None:
    """Retrieve and clean everything in one go."""
    for location in settings.LOCATIONS:
        execute_on_all(location, download_data)
        execute_on_all(location, trim_file_header)
        execute_on_all(location, delete_empty_rows)
        execute_on_all(location, clean_data)


if __name__ == "__main__":
    run()
