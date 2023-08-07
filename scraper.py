import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
import os
import mysql.connector
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

zillow_url = os.getenv("ZILLOW_URL")
redfin_url = os.getenv("REDFIN_URL")

# Check if URLs are present
if zillow_url is None or redfin_url is None:
    raise ValueError("One or both URLs are missing. Please check the .env file.")

# Establish a connection to the MySQL database
db_connection = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
    port=os.getenv("DB_PORT")
)
db_cursor = db_connection.cursor()

# Define the table creation query
create_table_query = """
CREATE TABLE IF NOT EXISTS property_values (
    id INT AUTO_INCREMENT PRIMARY KEY,
    property_name VARCHAR(255),
    redfin_value VARCHAR(255),
    zillow_value VARCHAR(255),
    last_updated DATETIME,
    UNIQUE (property_name)
)
"""

# Execute the table creation query
db_cursor.execute(create_table_query)
db_connection.commit()

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
zestimate_element = zillow_soup.find('span', class_='Text-c11n-8-84-3__sc-aiai24-0 hqOVzy')
zestimate_value = zestimate_element.find('span').text.strip() if zestimate_element else 'N/A'

# Get the property name (you need to define how you'll obtain this)
property_name = os.getenv("PROP_ADD")

# Create a timestamp for the last updated time
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Check if the property_name already exists in the database
check_query = "SELECT property_name FROM property_values WHERE property_name = %s"
db_cursor.execute(check_query, (property_name,))
existing_property = db_cursor.fetchall()

if existing_property:
    try:
        # Update the existing row
        update_query = """
        UPDATE property_values
        SET redfin_value = %s, zillow_value = %s, last_updated = %s
        WHERE property_name = %s
        """
        update_values = (redfin_value, zestimate_value, timestamp, property_name)
        db_cursor.execute(update_query, update_values)
        db_connection.commit()
        print("Property values updated in the database.")
    except Exception as e:
        print("Error updating property values:", str(e))
else:
    # Insert a new row
    insert_query = """
    INSERT INTO property_values (property_name, redfin_value, zillow_value, last_updated)
    VALUES (%s, %s, %s, %s)
    """
    insert_values = (property_name, redfin_value, zestimate_value, timestamp)
    db_cursor.execute(insert_query, insert_values)
    db_connection.commit()
    print("New property values saved to the database.")

# Close the database cursor and connection
db_cursor.close()
db_connection.close()