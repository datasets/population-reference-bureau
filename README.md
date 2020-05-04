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
    │   ├── [PACKAGE-NAME]
    │   │   ├── data
    │   │   │   └── international-[PACKAGE-NAME].csv
    │   │   └── datapackage.json
    │   ├── ... other packages ...
    └── us
        ├── [PACKAGE-NAME]
        │   ├── data
        │   │   └── us-[PACKAGE-NAME].csv
        │   └── datapackage.json
        └── ... other packages ...
