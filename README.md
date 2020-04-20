# awesome-data-prb

Curate available data from the [Population Reference Bureau](https://www.prb.org/data/).

## Table of contents
<!-- vim-markdown-toc GFM -->

* [Installation](#installation)
    * [Dependencies](#dependencies)
        * [Python](#python)
        * [JavaScript](#javascript)
* [Execution](#execution)
    * [General help](#general-help)
    * [Quick start](#quick-start)

<!-- vim-markdown-toc -->

---

## Installation

### Dependencies

#### Python

    pip install -r requirements.txt

#### JavaScript

**The npm package `data-cli` is required** if producing a `datapackage.json` file is desirable. If it is not available, the script will need to be run with other appropriate options (other than `package`) described when launching the script with no arguments. Install with one of the following commands:

    # globally
    npm install --global data-cli

    # locally
    npm install data-cli

## Execution

### General help

    python collect.py

This will display all available commands and options.

### Quick start

_Note: This requires all dependencies to be installed._

    python collect.py everything reset

This will do the following, in order:

1. Remove all local data, if any (downloaded, processed and cleaned).
2. Download data.
3. Process CSV files (trim headers, delete empty rows, clean data).
4. Generate truncated files to use with `data init` command.
5. Generate a `datapackage.json` file and validate it.

There will be quite a bit of output to the terminal. The final statement should read:

    > Your Data Package is valid!

The clean data that's useful for distribution in the end is located under the `clean_data` directory like so:

    .
    ├── clean_data
    │   ├── datapackage.json
    │   ├── inter
    │   │   ├── ...
    │   └── us
    │       ├── ...
