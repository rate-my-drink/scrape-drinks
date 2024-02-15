from typing import List

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from helpers.DrinkObject import Drink
from scrapers.helpers import export_drinks

PRODUCER_ID = 16
PRODUCER_NAME = "Local Tea"
BASE_URL = r"https://www.localtea.com/"


first_drink_url = r"https://www.localtea.com/localtea-chai/"
drink_url = first_drink_url

all_drinks: List[Drink] = []
while True:
    print(f"Now scraping: {drink_url}")
    # Get drink
    response = requests.get(drink_url)

    if response.status_code != 200:
        print(f"Got {response.status_code} status from {drink_url}. {response.content}")
        break

    drink_soup = BeautifulSoup(response.content, "html.parser")

    title_div = drink_soup.find("h1")
    title = title_div.text.strip()
    image_url = drink_soup.find("div", class_="image image-1").find(
        "img", class_="attachment-square-image size-square-image"
    )["data-lazy-src"]
    content = drink_soup.find("div", class_="column medium-1-2 content")
    description_ps = content.find_all("p")
    description = ""
    for p in description_ps:
        text = p.text.strip()
        if text:
            description += f"{text}\n"

    new_drink = Drink(
        href=drink_url,
        name=title,
        image_url=image_url,
        producer=PRODUCER_ID,
        description=description,
    )
    all_drinks.append(new_drink)

    # Get next url
    drink_url = content.find("h4").find("a")["href"]

    if drink_url == first_drink_url:
        break

export_drinks(PRODUCER_NAME, all_drinks)
