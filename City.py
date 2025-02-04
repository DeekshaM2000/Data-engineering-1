from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# Set up Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.0.0 Safari/537.36")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Direct URLs for cities
city_urls = {
    "Antalya": "https://www.lonelyplanet.com/turkey/mediterranean-coast/antalya",
    "Dubai": "https://www.lonelyplanet.com/united-arab-emirates/dubai",
    "Paris": "https://www.lonelyplanet.com/france/paris",
    "London": "https://www.lonelyplanet.com/england/london"
}

# Lists to store data
cities = []
countries = []
continents = []
image_urls = []
descriptions = []

# Function to scrape data for a single city
def scrape_city(city_name, city_url):
    driver.get(city_url)
    time.sleep(5)  # Wait for the page to load

    try:
        # Extract city name
        city = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        ).text.strip()
    except:
        city = city_name

    try:
        # Extract country dynamically
        country = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/destinations') or contains(@class, 'Breadcrumb')]"))
        ).text.strip()
    except:
        country = "N/A"

    # Assign continents dynamically
    continent_mapping = {
        "Turkey": "Europe/Asia", "UAE": "Asia", "France": "Europe", "United Kingdom": "Europe"
    }
    continent = continent_mapping.get(country, "N/A")

    try:
        # Extract main image URL dynamically
        image_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//meta[@property='og:image']"))
        )
        image_url = image_element.get_attribute("content")
    except:
        image_url = "N/A"

    try:
        # Extract description dynamically with multiple XPath approaches
        description_xpaths = [
            "//section[contains(@class, 'content')]/p",
            "//div[contains(@class, 'description')]/p",
            "//meta[@name='description']"
        ]
        description = "N/A"
        for xpath in description_xpaths:
            try:
                description_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, xpath))
                )
                description = description_element.text.strip() if xpath != description_xpaths[2] else description_element.get_attribute("content")
                break
            except:
                continue
    except:
        description = "N/A"

    # Append data to lists
    cities.append(city)
    countries.append(country)
    continents.append(continent)
    image_urls.append(image_url)
    descriptions.append(description)

    # Debugging - Print extracted values
    print(f"City: {city}")
    print(f"Country: {country}")
    print(f"Continent: {continent}")
    print(f"Image URL: {image_url}")
    print(f"Description: {description}")

# Scrape data for each city
for city, url in city_urls.items():
    scrape_city(city, url)

# Close the WebDriver
driver.quit()

# Create a DataFrame
df = pd.DataFrame({
    "City": cities,
    "Country": countries,
    "Continent": continents,
    "Image URL": image_urls,
    "Description": descriptions
})

# Save to CSV
df.to_csv("C:\\Users\\DEEKSHA M\\Documents\\python\\city_data.csv", index=False)

print("Scraping completed! Data saved as 'cities_data.csv'.")
