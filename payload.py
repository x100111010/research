import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from store import *  # Assuming the custom 'store' module is available
import kbech32

# path to your datadir2
data_dir = "/datadir2"
store = Store(data_dir)

# load recent blocks (you can adjust the number of blocks if needed)
store.load_recent_blocks(7200_000)

# define fields to query
header_fields = [
    "timeInMilliseconds",
    "blueScore",
    "blueWork",
    "daaScore",
    "difficulty",
]
block_fields = ["pubkey_script", "spectred_version", "miner_version"]
count_fields = []  # Optional fields for count data

# load the data into frames
frames = store.load_data(
    header_fields=header_fields, block_fields=block_fields, count_fields=count_fields
)

# convert the frames into a DataFrame and set the 'hash' as the index
df = pd.DataFrame(frames).set_index("hash")

# fetch pruning point time and dataframe length
pp_time = store.get_header_data(store.pruning_point()).timeInMilliseconds
print(f"Pruning Point Time: {pp_time}, DataFrame Length: {len(df)}")

# Get spectred version counts
version_counts = df["spectred_version"].value_counts(normalize=True)
print("Spectred Version Distribution:")
print(version_counts)


# identify miner types based on miner_version
def miner_type(miner_version):
    if "spectre-miner" in miner_version:
        return "BinaryExpr"
    if "tnn-miner" in miner_version:
        return "TnnMiner"
    if "TT-miner" in miner_version:
        return "TT-miner"
    if "spectre-stratum-bridge" in miner_version:
        return "spectre-stratum-bridge"
    return miner_version


df["miner_type"] = df["miner_version"].apply(miner_type)

# version and miner type counts
version_and_miner_type = (df["spectred_version"] + "/" + df["miner_type"]).value_counts(
    normalize=True
)

# version and miner type breakdown
print("Version and Miner Type Distribution:")
for entry in version_and_miner_type.items():
    print(f"{entry[0].ljust(45)} {round(entry[1], 4)}")

store.close()
