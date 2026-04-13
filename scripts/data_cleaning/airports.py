"""

"""
import os.path

import pandas as pd
from pathlib import Path

import config

def clean_airport_data() -> pd.DataFrame:
    """

    :return:
    """
    in_file_path = f"{config.PROJECT_DIR}/raw_data/airports.csv"
    df = pd.read_csv(in_file_path)

    # Drops irrelevant columns
    df = df.drop(
        columns=[
            "id",
            "ident",
            "elevation_ft",
            "gps_code",
            "local_code",
            "home_link",
            "wikipedia_link",
            "keywords",
        ]
    )

    # Filters ou non commercial airports
    df = df[
        (df["scheduled_service"] == "yes") &
        (df["type"] != "closed_airport") &
        (df["type"] != "balloonport") &
        (df["type"] != "heliport") &
        (df["type"] != "seaplane_base") &
        (df["type"] != "small_airport") &
        (df["icao_code"].notna())
        ]

    df.set_index("icao_code", inplace=True, drop=False)

    # Drops column no longer needed
    df = df.drop(columns=["scheduled_service"])

    # Removes the country code from the region code
    regions: list[str] = []

    for i in range(len(df["iso_region"])):
        stripped = df["iso_region"].iloc[i].split("-")
        if len(stripped) == 2:
            regions.append(stripped[1])


        elif len(stripped) == 3:
            regions.append("-".join(stripped[1:]))

    df["iso_region"] = regions

    out_file_path = os.path.dirname(__file__) / "cleaned_data" / "airports.csv"

    print(config.PROJECT_DIR)

if __name__ == '__main__':
    clean_airport_data()
