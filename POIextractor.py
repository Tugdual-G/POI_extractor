#!/usr/bin/env python3
#
""" Retrieves POI points saved via Garmin edge devices as
 .fit files and save them to the desired format. """

from datetime import timedelta, datetime, timezone
import os.path
import argparse
import pandas as pd
import geopandas as gpd
from garmin_fit_sdk import Decoder, Stream

parser = argparse.ArgumentParser(
    prog="POI extractor",
    description="Retrieves POI points from FIT file"
    " format and save them to the desired format.",
)
parser.add_argument("input_file", type=str)
parser.add_argument(
    "output_file",
    type=str,
    help="output file format can be '.json' '.gpkg' '.shp' for example",
)
args = parser.parse_args()

if not os.path.isfile(args.input_file):
    raise FileNotFoundError("the input file does not exist")

# Garmin seems to use UTC +0 as default
tz = timezone(timedelta(0))
# Garmin FIT epoch
FITepoch = datetime(1989, 12, 31, tzinfo=tz)

# Opening the file
stream = Stream.from_file(args.input_file)
decoder = Decoder(stream)
messages, errors = decoder.read()

for er in errors:
    print(er)

points = {
    "id": [],
    "name": [],
    "comment": [],
    "lon": [],
    "lat": [],
    "datetime": [],
    "symbol": [],
}

for k, v in messages.items():
    # The identification code corresponding to a
    # POI messages seems to be "29".
    if k == "29":
        for POI in messages[k]:
            points["id"] += [POI[254]]
            points["name"] += [POI[0]]
            points["comment"] += [POI.get(6)]

            # Converting from semicircles to degrees
            points["lat"] += [POI[1] * (180 / 2**31)]
            points["lon"] += [POI[2] * (180 / 2**31)]

            points["datetime"] += [FITepoch + timedelta(seconds=POI[253])]

            # The code corresponding to the symbol
            # representing the POI on the garmin device.
            points["symbol"] += [POI[3]]


df = pd.DataFrame(points)
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.lon, df.lat))

gdf.to_file(args.output_file)
print(gdf)
