from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# Set up Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.0.0 Safari/537.36")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Load flights data
flights_path = "C:/Users/DELL/web scraping/Flights/Booking_flights.csv"
flights_df = pd.read_csv(flights_path)

# Extract distinct airline names
distinct_airlines = flights_df['Airline'].dropna().unique()

# Airline ratings website base URL
base_url = "https://www.airlineratings.com/airlines/"

def extract_airline_data(airline_name):
    search_url = base_url + "-".join(airline_name.lower().split())
    driver.get(search_url)
    time.sleep(3)  # Allow page to load

    try:
        airline_name_extracted = driver.find_element(By.TAG_NAME, "h1").text.strip()
    except:
        return None  

    try:
        logo = driver.find_element(By.CSS_SELECTOR, 
            "body > div > main > div.w-full.max-w-full.overflow-x-clip.flex-grow > div > div.w-full.flex.flex-col.items-center.pt-48.mobile\:pt-16.pb-16.relative > div.flex.flex-col.items-center.gap-8.relative.z-10 > img"
        ).get_attribute("src")
    except:
        logo = "No logo available"

    return {
        "Name": airline_name_extracted,
        "Logo": f'"{logo}"',  # Wrapping logo in double quotes
        "URL": search_url
    }

# Collect airline data
airlines_data = []
for airline in distinct_airlines:
    airline_info = extract_airline_data(airline)
    if airline_info:
        airlines_data.append(airline_info)

# Save airline data
airlines_df = pd.DataFrame(airlines_data)
airlines_df.to_csv("C:/Users/DELL/web scraping/Flights/airlines.csv", index=False)

driver.quit()
print("Airlines data scraping completed! Data saved.")
