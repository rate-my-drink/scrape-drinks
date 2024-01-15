from typing import List

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from helpers.DrinkObject import Drink
from scrapers.helpers import export_drinks

PRODUCER_ID = 8
PRODUCER_NAME = "Albert Heijn"
headers = {
    "Host": "www.ah.nl",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,nl;q=0.7,en;q=0.3",
    "Accept-Encoding": "gzip, deflate, br",
    "DNT": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "TE": "trailers",
}
all_drinks: List[Drink] = []


all_drink_items = []
for base_url in [
    r"https://www.ah.nl/producten/frisdrank-sappen-koffie-thee/thee?merk=AH",
    r"https://www.ah.nl/producten/frisdrank-sappen-koffie-thee/thee?merk=AH%20Biologisch",
]:
    # Get all drinks from overview
    response = requests.get(base_url, headers=headers)
    last_response = response.status_code

    if last_response != 200:
        raise ConnectionError(f"Did not get a 200 status from {base_url}")

    drinks_soup = BeautifulSoup(response.content, "html.parser")

    drink_items = drinks_soup.find_all(
        "article",
        class_="product-card-portrait_root__ZiRpZ product-grid-lane_gridItems__BBa4h",
    )
    all_drink_items += drink_items

for drink_item in tqdm(all_drink_items):
    title = drink_item.find("strong").text.strip()
    href = drink_item.find("a")["href"]
    new_drink = Drink(
        href=f"https://www.ah.nl{href}",
        name=title,
        producer=PRODUCER_ID,
    )
    all_drinks.append(new_drink)

for drink in tqdm(all_drinks):
    response = requests.get(drink.href, headers=headers)
    if response.status_code != 200:
        raise ConnectionError(f"Did not get a 200 status from {drink.href}")
    drink_soup = BeautifulSoup(response.content, "html.parser")
    image_url = drink_soup.find("div", class_="swiper-wrapper").find("img")["src"]
    drink.image_url = image_url

    description = drink_soup.select('div[data-testhook="product-info-description"]')[
        0
    ].text.strip()
    drink.description = description
export_drinks(PRODUCER_NAME, all_drinks)
