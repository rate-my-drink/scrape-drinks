from typing import List

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from helpers.DrinkObject import Drink
from scrapers.helpers import export_drinks

PRODUCER_ID = 7
PRODUCER_NAME = "Clipper"
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0",
    "Referer": "https://www.clipper-teas.nl/",
}
all_drinks: List[Drink] = []


all_drink_items = []
for base_url in [
    r"https://www.clipper-teas.nl/onze-theeen/zwarte-thee/",
    # TODO breaks when going there directly r"https://www.clipper-teas.nl/onze-theeen/groene-thee/",
    r"https://www.clipper-teas.nl/onze-theeen/infusies/",
]:
    # Get all drinks from overview
    response = requests.get(base_url)
    last_response = response.status_code

    if last_response != 200:
        raise ConnectionError(f"Did not get a 200 status from {base_url}")

    drinks_soup = BeautifulSoup(response.content, "html.parser")

    drink_items = drinks_soup.find_all("div", class_="card")
    all_drink_items += drink_items

for drink_item in tqdm(all_drink_items):
    title = drink_item.find("h3", class_="faux-h5").text.strip()
    image_url = drink_item.find("img", class_="card__image")["src"]
    href = drink_item.find("a", class_="button")["href"]
    description = drink_item.find("div", class_="card__text mb-30").text.strip()
    new_drink = Drink(
        href=f"https://www.clipper-teas.nl{href}",
        name=title,
        producer=PRODUCER_ID,
        description=description,
        image_url=image_url,
    )
    all_drinks.append(new_drink)

export_drinks(PRODUCER_NAME, all_drinks)
