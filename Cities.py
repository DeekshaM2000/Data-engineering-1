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
    "Berlin": "https://www.lonelyplanet.com/germany/berlin",
    "Vienna": "https://www.lonelyplanet.com/austria/vienna",
    "Paris": "https://www.lonelyplanet.com/france/paris",
    "Tokyo": "https://www.lonelyplanet.com/japan/tokyo",
    "Barcelona": "https://www.lonelyplanet.com/spain/barcelona",
    "London": "https://www.lonelyplanet.com/england/london",
    "Rome": "https://www.lonelyplanet.com/italy/rome",
    "New York": "https://www.lonelyplanet.com/usa/new-york-city",
    "Antalya": "https://www.lonelyplanet.com/turkey/mediterranean-coast/antalya",
    "Dubai": "https://www.lonelyplanet.com/united-arab-emirates/dubai"
}

# Lists to store data
cities = []
countries = []
continents = []
image_urls = []
descriptions = []
cities_urls = []

# Function to extract description dynamically
def extract_description():
    description_xpaths = [
        "/html/body/div[1]/div[2]/main/section[2]/div/div/div[1]/p",
        "//section[contains(@class, 'content')]/p",
        "//div[contains(@class, 'description')]/p",
        "//p[contains(@class, 'text')]",
        "//article//p"
    ]
    description = "N/A"
    for xpath in description_xpaths:
        try:
            description_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            description = description_element.text.strip()
            break
        except:
            continue
    return description

# Function to scrape data for a single city
def scrape_city(city_name, city_url):
    driver.get(city_url)
    time.sleep(5)  # Wait for the page to load

    try:
        # Extract city name dynamically
        city = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        ).text.strip()
    except:
        city = city_name

    try:
        # Extract country dynamically using multiple possible XPaths
        country_xpaths = [
            "//ul[contains(@class, 'breadcrumbs')]//li[last()]/a",
            "//header/div/nav/ol/li[1]/a/span"
        ]
        country = "N/A"
        for xpath in country_xpaths:
            try:
                country_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, xpath))
                )
                country = country_element.text.strip()
                break
            except:
                continue
    except:
        country = "N/A"

    try:
        # Extract continent dynamically using multiple possible XPaths
        continent_xpaths = [
            "//header/div/nav/ol/li[2]/a/span"
        ]
        continent = "N/A"
        for xpath in continent_xpaths:
            try:
                continent_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, xpath))
                )
                continent = continent_element.text.strip()
                break
            except:
                continue
    except:
        continent = "N/A"

    try:
        # Extract main image URL dynamically with different XPath approaches
        image_xpaths = [
            "//meta[@property='og:image']",  # Meta tag image
            "//img[contains(@class, 'feature-image')]",  # Standard image class
            "//div[contains(@class, 'hero-image')]//img"  # Hero image section
        ]
        image_url = "N/A"
        for xpath in image_xpaths:
            try:
                image_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, xpath))
                )
                image_url = image_element.get_attribute("content") if xpath == image_xpaths[0] else image_element.get_attribute("src")
                break
            except:
                continue
    except:
        image_url = "N/A"

    # Extract description using the new function
    description = extract_description()

    # Append data to lists
    cities.append(city)
    countries.append(country)
    continents.append(continent)
    image_urls.append(image_url)
    descriptions.append(description)
    cities_urls.append(city_url)

    # Debugging - Print extracted values
    print(f"City: {city}")
    print(f"Country: {country}")
    print(f"Continent: {continent}")
    print(f"Image URL: {image_url}")
    print(f"Description: {description}")
    print(f"City URL: {city_url}")

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
    "Description": descriptions,
    "City URL": cities_urls
})

# Save to CSV
df.to_csv("C:\\Users\\DEEKSHA M\\Documents\\python\\cities_data1.csv", index=False)

print("Scraping completed! Data saved as 'cities_data.csv'.")
