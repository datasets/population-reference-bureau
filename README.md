# Population Reference Bureau

Curated data available from the [Population Reference Bureau](https://www.prb.org/data/).

## Requirements

The requirements can be installed with the following command:

    pip install -r requirements.txt

## Execution

    python collect.py


The clean data that's useful for distribution is located under the
`data` directory like so:

    data
    ├── international
    │   ├── [PACKAGE_NAME]
    │   │   ├── data
    │   │   │   └── international_[PACKAGE_NAME].csv
    │   │   └── datapackage.json
    │   ├── ... other packages ...
    └── us
        ├── [PACKAGE_NAME]
        │   ├── data
        │   │   └── us_[PACKAGE_NAME].csv
        │   └── datapackage.json
        └── ... other packages ...
