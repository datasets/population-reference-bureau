"""
Quick settings to modify, if needed.
"""
SETTINGS = {
    "clean_data": "clean_data",
    "clean_data_inter": "clean_data/inter",
    "clean_data_us": "clean_data/us",
    "original_data": "original_data",
    "original_data_inter": "original_data/inter",
    "original_data_us": "original_data/us",
    "processed_data": "processed_data",
    "processed_data_inter": "processed_data/inter",
    "processed_data_us": "processed_data/us",
    "truncate_data": "truncate_data",
    "truncate_data_inter": "truncate_data/inter",
    "truncate_data_us": "truncate_data/us",
    "temp_dir": "temp",
}

FOLDERS_TO_CLEAN = [
    "__pycache__",
    "helpers/__pycache__",
    "temp",
    SETTINGS["clean_data"],
    SETTINGS["clean_data_inter"],
    SETTINGS["clean_data_us"],
    SETTINGS["original_data"],
    SETTINGS["original_data_inter"],
    SETTINGS["original_data_us"],
    SETTINGS["processed_data"],
    SETTINGS["processed_data_inter"],
    SETTINGS["processed_data_us"],
    SETTINGS["truncate_data"],
    SETTINGS["truncate_data_inter"],
    SETTINGS["truncate_data_us"],
]

# Needed for script to work fully
FOLDERS_TO_CREATE = [
    "temp",
    SETTINGS["clean_data"],
    SETTINGS["clean_data_inter"],
    SETTINGS["clean_data_us"],
    SETTINGS["original_data"],
    SETTINGS["original_data_inter"],
    SETTINGS["original_data_us"],
    SETTINGS["processed_data"],
    SETTINGS["processed_data_inter"],
    SETTINGS["processed_data_us"],
    SETTINGS["truncate_data"],
    SETTINGS["truncate_data_inter"],
    SETTINGS["truncate_data_us"],
]

# Data extracted from HTML source at https://www.prb.org/international/
DATA_INTER = {
    "name": "inter",
    "sources": [
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
    ],
    "url_bit": "international",  # variable part of URL
}

# Data extracted from HTML source at https://www.prb.org/usdata/
DATA_US = {
    "name": "us",
    "sources": [
        "population",
        "population-change",
        "births",
        "deaths",
        "fertility",
        "migration",
        "race-ethnicity",
        "age65",
        "age18",
        "elderly-support-ratio",
        "foreign-born",
        "bachelors-degree",
        "income",
        "poverty",
        "marriage-age-men",
        "marriage-age-women",
        "gini",
        "living-alone",
    ],
    "url_bit": "usdata",  # variable part of URL
}

LOCATIONS = {
    "international": DATA_INTER["sources"],
    "us": DATA_US["sources"],
}
