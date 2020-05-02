"""
Quick settings to modify, if needed.
"""
DIRS = {
    "clean_data": "data",
    "clean_data_inter": "data/inter",
    "clean_data_us": "data/us",
    "original_data": "scripts/original_data",
    "original_data_inter": "scripts/original_data/inter",
    "original_data_us": "scripts/original_data/us",
    "processed_data": "scripts/processed_data",
    "processed_data_inter": "scripts/processed_data/inter",
    "processed_data_us": "scripts/processed_data/us",
    "temp_dir": "scripts/temp",
}

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
