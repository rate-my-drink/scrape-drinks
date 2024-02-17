from pathlib import Path
from helpers import load_img_from_url, SupabaseCC
import pandas as pd
from tqdm import tqdm

client = SupabaseCC()

csv_loc = Path("upload") / "filtered_data" / "Twinings.csv"


df = pd.read_csv(csv_loc)
df = df.fillna(" ")

for index, row in tqdm(df.iterrows()):
    try:
        image = load_img_from_url(row["image_url"])
    except:
        print(
            f"Error: Image of {row['name']} could not be downloaded. {row['image_url']}"
        )
        image = None
    client.upload_drink(
        row["name"],
        row["producer"],
        row["href"],
        description=row.get("description", " "),
        image_bytes=image,
    )
# took 2 minutes and 19 seconds
