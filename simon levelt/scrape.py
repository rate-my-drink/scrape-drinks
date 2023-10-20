import requests
from bs4 import BeautifulSoup

base_url = r"https://www.simonlevelt.nl/"
# Send a GET request to the coffee page

last_response = 200
coffee_list = []
p = 1
while last_response == 200:
    coffee_url = f"{base_url}/koffie?p={p}&o=2&n=17&f=10003"
    coffee_response = requests.get(coffee_url)
    last_response = coffee_response.status_code
    if last_response != 200:
        break
    # Parse the HTML content of the coffee page
    coffee_soup = BeautifulSoup(coffee_response.content, "html.parser")

    # Find the HTML elements that contain the coffee information
    coffee_items = coffee_soup.find_all("div", class_="product--box")

    # Extract the coffee information and store it in a list or dictionary

    for item in coffee_items:
        try:
            a_tittle = item.find("a", class_="product--title")
            name = a_tittle.text.strip()
            href = a_tittle["href"]
            coffee_list.append({"name": name, "producer": 1, "href": href})
        except:
            pass
    p += 1

for coffee in coffee_list:
    try:
        coffee_response = requests.get(coffee["href"])
        last_response = coffee_response.status_code
        if last_response != 200:
            continue
        # Parse the HTML content of the coffee page
        coffee_page_soup = BeautifulSoup(coffee_response.content, "html.parser")
        description = (
            coffee_page_soup.find("div", class_="product--description")
            .find("p")
            .text.strip()
        )
        coffee["description"] = description
    except:
        pass

# Send a GET request to the tea page
tea_url = "https://www.simonlevelt.com/en/tea-coffee/tea"
tea_response = requests.get(tea_url)

# Parse the HTML content of the tea page
tea_soup = BeautifulSoup(tea_response.content, "html.parser")

# Find the HTML elements that contain the tea information
tea_items = tea_soup.find_all("div", class_="product-item")

# Extract the tea information and store it in a list or dictionary
tea_list = []
for item in tea_items:
    name = item.find("h3", class_="product-item__title").text.strip()
    description = item.find("div", class_="product-item__description").text.strip()
    price = item.find("span", class_="product-item__price").text.strip()
    tea_list.append({"name": name, "description": description, "price": price})

# Combine the coffee and tea information into a single list or dictionary
drinks_list = coffee_list + tea_list

# Output the final list or dictionary
print(drinks_list)
