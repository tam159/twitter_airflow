import csv
from pathlib import Path
import json
from collections import defaultdict
import pandas as pd

with open(
    str(Path().resolve().parent) + "/master_data/kols/IDTwitterBuzzer.csv", "r"
) as buzzers:
    for kol in csv.DictReader(buzzers):
        # print(json.loads(json.dumps(row)))
        print(dict(kol))
