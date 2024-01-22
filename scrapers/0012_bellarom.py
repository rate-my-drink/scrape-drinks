from pathlib import Path
from typing import List

from bs4 import BeautifulSoup
from tqdm import tqdm
from helpers.DrinkObject import Drink
from scrapers.helpers import export_drinks

PRODUCER_ID = 12
PRODUCER_NAME = "Bellarom"
BASE_URL = r"https://www.lidl.nl"
headers = {
    "Host": BASE_URL,
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
}


drinks_soup = BeautifulSoup(
    Path("downloaded_sites/0012_lidl_coffee.html").read_text(), "html.parser"
)

all_drink_items = []
drink_items = drinks_soup.find_all("li", class_="ACampaignGrid__item--product")
all_drink_items += drink_items

all_drinks: List[Drink] = []
for drink_item in tqdm(all_drink_items):
    title = drink_item.find("h2").text.strip()
    href = drink_item.find("a", class_="grid-box__pdp-link")["href"]
    image_url = drink_item.find("img", class_="product-grid-box__image")["src"]
    new_drink = Drink(
        href=f"{BASE_URL}{href}", name=title, producer=PRODUCER_ID, image_url=image_url
    )
    all_drinks.append(new_drink)

export_drinks(PRODUCER_NAME, all_drinks)
