import requests
from bs4 import BeautifulSoup
import json
import time
from dotenv import load_dotenv
from datetime import datetime
import os


# Load environment variables from .env file
load_dotenv()

zillow_url = os.getenv("ZILLOW_URL")
redfin_url = os.getenv("REDFIN_URL")

# Check if URLs are present
if zillow_url is None or redfin_url is None:
    raise ValueError("One or both URLs are missing. Please check the .env file.")


# Send a GET request to Redfin webpage with headers to mimic a browser
redfin_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}
redfin_response = requests.get(redfin_url, headers=redfin_headers)
redfin_soup = BeautifulSoup(redfin_response.content, 'html.parser')
redfin_div_element = redfin_soup.find('div', class_='value')
redfin_value = redfin_div_element.text.strip()

# Introduce a delay to mimic human-like behavior
time.sleep(2)

# Send a GET request to Zillow webpage with headers to mimic a browser
zillow_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}
zillow_response = requests.get(zillow_url, headers=zillow_headers)
zillow_soup = BeautifulSoup(zillow_response.content, 'html.parser')
zestimate_element = zillow_soup.find('span', class_='Text-c11n-8-89-0__sc-aiai24-0 cfmKEe')
zestimate_value = zestimate_element.find('span').text.strip() if zestimate_element else 'N/A'


# Create a timestamp for the last updated time
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Store values and timestamp in a dictionary
values = {
    'redfin': redfin_value,
    'zillow': zestimate_value,
    'last_updated': timestamp
}

# Save values to a JSON file
filename = 'data/property_values.json'
with open(filename, 'w') as file:
    json.dump(values, file)

print("Property values saved to", filename)
