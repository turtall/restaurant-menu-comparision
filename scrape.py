import requests
import urllib.parse
from bs4 import BeautifulSoup
from datetime import datetime, timezone
from db_table import db_table
import json

import requests
from bs4 import BeautifulSoup


def get_bagaan_data():
    # Headers for the HTTP request
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.6',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Referer': 'https://bagaanthakali.com/',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Sec-GPC': '1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Brave";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    # Sending the request to the website
    response = requests.get('https://bagaanthakali.com/menu/', headers=headers)

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Create an empty list to store the data
    products = []

    # Find all the divs that contain the product information
    product_divs = soup.find_all('div', class_='featured-restaurant-box')

    for div in product_divs:
        # Extract the product name
        name = div.find('h4', itemprop='headline').get_text(strip=True)

        # Extract the price and clean it
        price = div.find('span', class_='price').get_text(strip=True)

        image = ""
        try:
            image = div.find('img', class_='brd-rd50')['src']
        except:
            print("Could not get image")

        # Remove the currency symbol and any extra text
        price = price.replace('Rs', '').strip()

        # Add the product to the list
        products.append({
            'name': name,
            'price': price,
            'image': image
        })

    return products


def get_jimbu_data():
    cookies = {
        'cart_id': 'eyJpdiI6InYrRWRJUk5mQXlYNzlhQndnMVlZQ2c9PSIsInZhbHVlIjoiVkR3ek5STndud0xZM3Jyd2ZTQTlSNGpDWFZWTGZ6Rk1xdkNxVFdjeFNXTDZDVU1FMS9TV0k2MTJjTm5ZbU9pdGMyd2NPdWhVaGZPTG1yQnY4aVFIYnc9PSIsIm1hYyI6ImU1YTk5NmVkN2JjYzA0NjNkZmM3ODBlY2U2MTQyNTBiZTE3MDU5OGRhNjBjZjZlODQzMTdhNmI5MzZhZjI0NTEiLCJ0YWciOiIifQ%3D%3D',
        'XSRF-TOKEN': 'eyJpdiI6ImVYQS81NFZOYVl3VmNpL2NKUnczRHc9PSIsInZhbHVlIjoiSlYrejU1WjVhZmluZW1sOGt4eXZQcjRabVozeTJyNCtuRmE2VE1UTTVZRlg0Y1Y1Z2UrTHR3NUR4enBHVStVR0k1dUJacEsrWUcramVnQTdqaDhpYzVkTkxoaEJvK2F0OUt0MHB3YmxaenVPNTh1RGVJZWNqUXBsNzU3VDR6RnQiLCJtYWMiOiJiZmI0MWMyN2UyZDk4OThmMzg0YmMwYTUwYTc2YjZhNWMzM2EzYmEyMzMyYjBiMDA3ZDZjYzVmYjI5NzdkYjIyIiwidGFnIjoiIn0%3D',
        'jimbu_thakali_session': 'eyJpdiI6IlBvek5qaFpVTVpVSVJpb1VydjE1UFE9PSIsInZhbHVlIjoiRHY4eDIvMWRhT0VEd0p6MjF1RDRkUnJxcVB2eEtXbWs2T3VZSVNsSmFwd0RTMGxTVitoL1dZTmdjaDVodXdXcGlnM0dweFNsclVERmdWcEUzWGRXTlhKZWJJSlkzMDVCSDVIckNEVk5wNlpzMkdRN2tjcHRya1h0K3JWeTMzVjIiLCJtYWMiOiJhZmE2OTcxZGY2YzE4OWEwNTMwZWZjM2I3OTViN2YwMWRkY2UyY2VmMTA0MjM4YTJhNmZjYzEyZTJkZjY2MTk5IiwidGFnIjoiIn0%3D',
        '5A9QjemXYmEKNEfIXuRz6l79xIRuIYVJIBoAaPTA': 'eyJpdiI6IkNXUVhvenhxdkVua3A1NTltVnd4YkE9PSIsInZhbHVlIjoiYXkvK2M0NlJUaDVyY2F6cGg4azFaQnRSeGY1VkxtRHlQazBJb0lSMnk4YUE1aVNIbEd1bEhvWnQ5QTJWUXBGRy9aWFB6NkQvZ3RpL0dQWHliMWo4SUU1V0RBKzJTNEp3NGE4Tlo0SlFtUVo0R2xuYjdTZ2N3MjBoZ212YzNJWkFUTlVWZG5NcnlWVjNxelM2YjBsaVJZKzJPYVhySVhpNEJ3dythUzZSWTBsU1dic2VsMkk4SFBCUGlwRXhhSHp2Tzhhbm4zMDJhTXJ1emo4aDdSU2owZEVtZHV3TXZia1dXQ0tOcmFGMFBva1R6bndTcGtqRFRkaVdlMm9na0VNS1dYb1ZlNi9rZ0tlbytpdU1QRVYwbmlMTGF2c3MzSHpQRHJLRXNjMHdENTVteDhUbGN6SDI0SW0yU3ZqUmhvOEppRjVhRHZiNUhFekpzZm9LTjZmaGYrR3B4RUxOVnZQNVdCRHAyaDBZUkkzdzE2K2cwTitxS2xIWkdMbWQxUTNvIiwibWFjIjoiNzIxNTlmNzQwMDllZDI3OThhZWMzYjIwM2ZhMGY3ZjgzYzdhNWI1NDgxOWIwYmEzNGUwNjAxNDkwYWYzYzJiZCIsInRhZyI6IiJ9',
    }

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'dnt': '1',
        'priority': 'u=0, i',
        'referer': 'https://jimbuthakali.com/',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Brave";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'sec-gpc': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    }

    response = requests.get('https://jimbuthakali.com/menu',
                            cookies=cookies, headers=headers)

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Create an empty list to store the data
    products = []

    # Find all the divs that contain the product information
    product_divs = soup.find_all('div', class_='item')

    for div in product_divs:
        try:
            # Extract the product name
            name = div.find('a', class_='food-name').get_text(strip=True)

            # Extract the price and clean it
            price = div.find('div', class_='food-price').get_text(strip=True)

            image = ""
            try:
                image = div.find('img', class_='lazy')['src']
            except:
                print("Could not get image")

            # Remove the currency symbol and any extra text
            price = price.replace('Rs.', '').strip()

            # Add the product to the list
            products.append({
                'name': name,
                'price': price,
                'image': image
            })
        except:
            print("Could not scrape item")

    return products


bagaan_data = []
jimbu_data = []

got_data = False
try:
    print("bagaan")
    bagaan_data = get_bagaan_data()
    print("jimbu")
    jimbu_data = get_jimbu_data()
    got_data = True
except Exception as e:
    print(e)
    print("Cound not get data")

if got_data:
    try:
        # Iniit the database connection
        db_schema = {
            "sn": "INT PRIMARY KEY",
            "name": "string",
            "price": "float",
            "image": "string"
        }

        bagaan_db = db_table("BAGAAN", db_schema)
        for index, item in enumerate(bagaan_data):
            try:
                item["sn"] = index + 1
                bagaan_db.insert(item)
            except:
                print("Could not insert item in database")
                print(item)

        jimbu_db = db_table("JIMBU", db_schema)
        for index, item in enumerate(jimbu_data):
            try:
                item["sn"] = index + 1
                jimbu_db.insert(item)
            except:
                print("Could not insert item in database")
                print(item)
        print("Done updating database")
    except:
        print("Cound not load data in database")
else:
    print("Data could not be fetched")
