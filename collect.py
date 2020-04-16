"""

"""
# Standard library imports
import argparse

# Local imports
from helpers.helpers import (
    _start_from_scratch,
    do_maintenance,
    download_dataset,
    execute_on_all,
    trim_file_header,
)

# Quick settings
SETTINGS = {"download": False}

# Extracted from HTML source at https://www.prb.org/international/ with Neovim
DATASETS = [
    "population",
    "population-2035",
    "population-2050",
    "births",
    "deaths",
    "rate-natural-increase",
    "infant-mortality",
    "fertility",
    "gross-national-income",
    "urban",
    "fp-all",
    "fp-total-modern",
    "hiv-rate-male",
    "hiv-rate-female",
    "life-expectancy-birth-male",
    "life-expectancy-birth-female",
    "age15",
    "age65",
    "hh-size-av",
    "hh-one-person",
    "fp-unmet-total",
    "fp-demand-satisfied-married",
    "fp-demand-satisfied-15-24",
]


@do_maintenance
def run() -> None:
    """Main function to run the script. The action happens here."""
    execute_on_all(DATASETS, download_dataset, SETTINGS)
    execute_on_all(DATASETS, trim_file_header)


if __name__ == "__main__":
    # initiate the parser
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument(
        "-d",
        "--download",
        help="Force download of datasets",
        action="store_true",
    )
    PARSER.add_argument(
        "-r",
        "--reset",
        help="Start from scratch: delete everything",
        action="store_true",
    )

    # read arguments from the command line
    ARGUMENTS = PARSER.parse_args()

    # check for --reset or -r, script ends here if condition is true
    if ARGUMENTS.reset:
        _start_from_scratch()  # script exits here

    if ARGUMENTS.download:
        SETTINGS["download"] = True

    run()
