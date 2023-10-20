import requests
from bs4 import BeautifulSoup

# Send a GET request to the coffee page
coffee_url = "https://www.simonlevelt.com/en/tea-coffee/coffee"
coffee_response = requests.get(coffee_url)

# Parse the HTML content of the coffee page
coffee_soup = BeautifulSoup(coffee_response.content, "html.parser")

# Find the HTML elements that contain the coffee information
coffee_items = coffee_soup.find_all("div", class_="product-item")

# Extract the coffee information and store it in a list or dictionary
coffee_list = []
for item in coffee_items:
    name = item.find("h3", class_="product-item__title").text.strip()
    description = item.find("div", class_="product-item__description").text.strip()
    price = item.find("span", class_="product-item__price").text.strip()
    coffee_list.append({"name": name, "description": description, "price": price})

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
