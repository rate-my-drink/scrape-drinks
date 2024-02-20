from typing import List

import requests
from helpers.DrinkObject import Drink
from scrapers.helpers import export_drinks

PRODUCER_ID = 20
PRODUCER_NAME = "starbucks"
BASE_URL = r"https://www.starbucks.com/"


all_catagories = []
category_hrefs = [
    BASE_URL + "/menu/drinks/oleato",
    BASE_URL + "/menu/drinks/hot",
    BASE_URL + "/menu/drinks/frappuccino",
    BASE_URL + "/menu/drinks/cold",
    BASE_URL + "/menu/drinks/iced",
]

category_href = r"https://www.starbucks.com/bff/ordering/menu"
# Get all drinks from overview
response = requests.get(category_href)
last_response = response.status_code

if response.status_code != 200:
    raise ConnectionError(
        f"Got {response.status_code} status from {category_href}. {response.content}"
    )

full_response = response.json()
categories = full_response["menus"]
for category in categories:
    if category["name"] == "Drinks":
        break


def get_products(children) -> List:
    if len(children["children"]) == 0:
        return children["products"]

    result = []
    for c in children["children"]:
        result += get_products(c)
    return result


products = get_products(category)
all_drinks: List[Drink] = []
for product in products:
    if product["productType"] != "Beverage":
        continue
    new_drink = Drink(
        href=f"{BASE_URL}menu{product['uri']}",
        name=product["name"],
        producer=PRODUCER_ID,
        image_url=product["assets"]["masterImage"]["uri"],
    )
    all_drinks.append(new_drink)
print(len(all_drinks))

export_drinks(PRODUCER_NAME, all_drinks)
