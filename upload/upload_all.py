from helpers import load_img_from_url, SupabaseCC
import pandas as pd
from tqdm import tqdm

client = SupabaseCC()

csv_loc = r"/home/tom/Documents/git/scrape-drinks/upload/filtered_data/Lipton.csv"


df = pd.read_csv(csv_loc)

for index, row in tqdm(df.iterrows()):
    image = load_img_from_url(row["image_url"])
    client.upload_drink(
        row["name"],
        row["producer"],
        row["href"],
        description=row["description"],
        image_bytes=image,
    )
# took 2 minutes and 19 seconds
