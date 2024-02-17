from pathlib import Path
from typing import List

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from helpers.DrinkObject import Drink
from scrapers.helpers import export_drinks

PRODUCER_ID = 17
PRODUCER_NAME = "Twinings"
BASE_URL = r"https://twinings.co.uk"
headers = {
    "Host": BASE_URL,
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
}


drinks_soup = BeautifulSoup(
    Path("downloaded_sites/0017_twinings.html").read_text(), "html.parser"
)

all_drink_items = drinks_soup.find_all(
    "div",
    class_="c-card",
)

all_drinks: List[Drink] = []
for drink_item in tqdm(all_drink_items):
    title_el = drink_item.find("h2", class_="c-card__title")
    title = title_el.text.strip()
    href = BASE_URL + title_el.find("a")["href"]

    image_url = drink_item.find("a", class_="c-card__image").find("img")["src"]

    response = requests.get(href)
    if response.status_code != 200:
        raise ConnectionError(
            f"Did not get a 200 status from {href}. \n {response.content}"
        )
    drink_soup = BeautifulSoup(response.content, "html.parser")
    description = drink_soup.find("div", class_="c-pdp-info__description").text.strip()

    new_drink = Drink(
        href=href,
        name=title,
        producer=PRODUCER_ID,
        image_url=image_url,
        description=description,
    )
    all_drinks.append(new_drink)

export_drinks(PRODUCER_NAME, all_drinks)
