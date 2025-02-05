from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import re


options = webdriver.ChromeOptions()
options.add_argument("--headless")  
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.0.0 Safari/537.36")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

urls = [ 
    "https://flights.booking.com/flights/FRA.CITY-PMI.AIRPORT/?type=ROUNDTRIP&adults=2&cabinClass=ECONOMY&children=10%2C8&from=FRA.CITY&to=PMI.AIRPORT&fromCountry=DE&toCountry=ES&fromLocationName=Frankfurt%2FMain&toLocationName=Palma+de+Mallorca+Airport&depart=2025-06-01&return=2025-09-01&sort=BEST&travelPurpose=leisure&aid=304142&label=gen173bo-1DEg1mbGlnaHRzX2luZGV4KIICQgVpbmRleEgxWANoO4gBAZgBMbgBF8gBDNgBA-gBAfgBBogCAZgCAqgCA7gCk-DzvAbAAgHSAiRiNjQ4OTI1Yy0wODY4LTRkYTMtYWQ1Ni1hZTg3MDNiYWU5MTjYAgTgAgE&adplat=www-index-web_shell_header-flight-missing_creative-CrAksofCVeaQ3cIeUQG6V",  
    "https://flights.booking.com/flights/FRA.CITY-VIE.AIRPORT/?type=ROUNDTRIP&adults=2&cabinClass=ECONOMY&children=10%2C8&from=FRA.CITY&to=VIE.AIRPORT&fromCountry=DE&toCountry=AT&fromLocationName=Frankfurt%2FMain&toLocationName=Vienna+International+Airport&depart=2025-06-01&return=2025-09-01&sort=BEST&travelPurpose=leisure&aid=304142&label=gen173bo-1DEg1mbGlnaHRzX2luZGV4KIICQgVpbmRleEgxWANoO4gBAZgBMbgBF8gBDNgBA-gBAfgBBogCAZgCAqgCA7gCk-DzvAbAAgHSAiRiNjQ4OTI1Yy0wODY4LTRkYTMtYWQ1Ni1hZTg3MDNiYWU5MTjYAgTgAgE&adplat=www-index-web_shell_header-flight-missing_creative-CrAksofCVeaQ3cIeUQG6V",  
    "https://flights.booking.com/flights/FRA.CITY-PAR.CITY/?type=ROUNDTRIP&adults=2&cabinClass=ECONOMY&children=10%2C8&from=FRA.CITY&to=PAR.CITY&fromCountry=DE&toCountry=FR&fromLocationName=Frankfurt%2FMain&toLocationName=Paris&depart=2025-06-01&return=2025-09-01&sort=BEST&travelPurpose=leisure&aid=304142&label=gen173bo-1DEg1mbGlnaHRzX2luZGV4KIICQgVpbmRleEgxWANoO4gBAZgBMbgBF8gBDNgBA-gBAfgBBogCAZgCAqgCA7gCk-DzvAbAAgHSAiRiNjQ4OTI1Yy0wODY4LTRkYTMtYWQ1Ni1hZTg3MDNiYWU5MTjYAgTgAgE&adplat=www-index-web_shell_header-flight-missing_creative-CrAksofCVeaQ3cIeUQG6V",  
    "https://flights.booking.com/flights/FRA.CITY-DEL.AIRPORT/?type=ROUNDTRIP&adults=2&cabinClass=ECONOMY&children=10%2C8&from=FRA.CITY&to=DEL.AIRPORT&fromCountry=DE&toCountry=IN&fromLocationName=Frankfurt%2FMain&toLocationName=Delhi+International+Airport&depart=2025-06-01&return=2025-09-01&sort=BEST&travelPurpose=leisure&aid=304142&label=gen173bo-1DEg1mbGlnaHRzX2luZGV4KIICQgVpbmRleEgxWANoO4gBAZgBMbgBF8gBDNgBA-gBAfgBBogCAZgCAqgCA7gCk-DzvAbAAgHSAiRiNjQ4OTI1Yy0wODY4LTRkYTMtYWQ1Ni1hZTg3MDNiYWU5MTjYAgTgAgE&adplat=www-index-web_shell_header-flight-missing_creative-CrAksofCVeaQ3cIeUQG6V"
    "https://flights.booking.com/flights/FRA.CITY-BCN.AIRPORT/?type=ROUNDTRIP&adults=2&cabinClass=ECONOMY&children=10%2C8&from=FRA.CITY&to=BCN.AIRPORT&fromCountry=DE&toCountry=ES&fromLocationName=Frankfurt%2FMain&toLocationName=Barcelona+El+Prat+Airport&depart=2025-06-01&return=2025-09-01&sort=BEST&travelPurpose=leisure&aid=304142&label=gen173bo-1DEg1mbGlnaHRzX2luZGV4KIICQgVpbmRleEgxWANoO4gBAZgBMbgBF8gBDNgBA-gBAfgBBogCAZgCAqgCA7gCk-DzvAbAAgHSAiRiNjQ4OTI1Yy0wODY4LTRkYTMtYWQ1Ni1hZTg3MDNiYWU5MTjYAgTgAgE&adplat=www-index-web_shell_header-flight-missing_creative-CrAksofCVeaQ3cIeUQG6V",  
    "https://flights.booking.com/flights/FRA.CITY-LON.CITY/?type=ROUNDTRIP&adults=2&cabinClass=ECONOMY&children=10%2C8&from=FRA.CITY&to=LON.CITY&fromCountry=DE&toCountry=GB&fromLocationName=Frankfurt%2FMain&toLocationName=London&depart=2025-06-01&return=2025-09-01&sort=BEST&travelPurpose=leisure&aid=304142&label=gen173bo-1DEg1mbGlnaHRzX2luZGV4KIICQgVpbmRleEgxWANoO4gBAZgBMbgBF8gBDNgBA-gBAfgBBogCAZgCAqgCA7gCk-DzvAbAAgHSAiRiNjQ4OTI1Yy0wODY4LTRkYTMtYWQ1Ni1hZTg3MDNiYWU5MTjYAgTgAgE&adplat=www-index-web_shell_header-flight-missing_creative-CrAksofCVeaQ3cIeUQG6V",  
    "https://flights.booking.com/flights/FRA.CITY-TYO.CITY/?type=ROUNDTRIP&adults=2&cabinClass=ECONOMY&children=10%2C8&from=FRA.CITY&to=TYO.CITY&fromCountry=DE&toCountry=JP&fromLocationName=Frankfurt%2FMain&toLocationName=Tokyo&depart=2025-06-01&return=2025-09-01&sort=BEST&travelPurpose=leisure&aid=304142&label=gen173bo-1DEg1mbGlnaHRzX2luZGV4KIICQgVpbmRleEgxWANoO4gBAZgBMbgBF8gBDNgBA-gBAfgBBogCAZgCAqgCA7gCk-DzvAbAAgHSAiRiNjQ4OTI1Yy0wODY4LTRkYTMtYWQ1Ni1hZTg3MDNiYWU5MTjYAgTgAgE&adplat=www-index-web_shell_header-flight-missing_creative-CrAksofCVeaQ3cIeUQG6V",
    "https://flights.booking.com/flights/FRA.CITY-CAI.AIRPORT/?type=ROUNDTRIP&adults=2&cabinClass=ECONOMY&children=10%2C8&from=FRA.CITY&to=CAI.AIRPORT&fromCountry=DE&toCountry=EG&fromLocationName=Frankfurt%2FMain&toLocationName=Cairo+International+Airport&depart=2025-06-01&return=2025-09-01&sort=BEST&travelPurpose=leisure&aid=304142&label=gen173bo-1DEg1mbGlnaHRzX2luZGV4KIICQgVpbmRleEgxWANoO4gBAZgBMbgBF8gBDNgBA-gBAfgBBogCAZgCAqgCA7gCk-DzvAbAAgHSAiRiNjQ4OTI1Yy0wODY4LTRkYTMtYWQ1Ni1hZTg3MDNiYWU5MTjYAgTgAgE&adplat=www-index-web_shell_header-flight-missing_creative-CrAksofCVeaQ3cIeUQG6V",
    "https://flights.booking.com/flights/FRA.CITY-AYT.AIRPORT/?type=ROUNDTRIP&adults=2&cabinClass=ECONOMY&children=10%2C8&from=FRA.CITY&to=AYT.AIRPORT&fromCountry=DE&toCountry=TR&fromLocationName=Frankfurt%2FMain&toLocationName=Antalya+Airport&depart=2025-06-01&return=2025-09-01&sort=BEST&travelPurpose=leisure&aid=304142&label=gen173bo-1DEg1mbGlnaHRzX2luZGV4KIICQgVpbmRleEgxWANoO4gBAZgBMbgBF8gBDNgBA-gBAfgBBogCAZgCAqgCA7gCk-DzvAbAAgHSAiRiNjQ4OTI1Yy0wODY4LTRkYTMtYWQ1Ni1hZTg3MDNiYWU5MTjYAgTgAgE&adplat=www-index-web_shell_header-flight-missing_creative-CrAksofCVeaQ3cIeUQG6V",  
    "https://flights.booking.com/flights/FRA.CITY-DXB.CITY/?type=ROUNDTRIP&adults=2&cabinClass=ECONOMY&children=10%2C8&from=FRA.CITY&to=DXB.CITY&fromCountry=DE&toCountry=AE&fromLocationName=Frankfurt%2FMain&toLocationName=Dubai&depart=2025-06-01&return=2025-09-01&sort=BEST&travelPurpose=leisure&aid=304142&label=gen173bo-1DEg1mbGlnaHRzX2luZGV4KIICQgVpbmRleEgxWANoO4gBAZgBMbgBF8gBDNgBA-gBAfgBBogCAZgCAqgCA7gCk-DzvAbAAgHSAiRiNjQ4OTI1Yy0wODY4LTRkYTMtYWQ1Ni1hZTg3MDNiYWU5MTjYAgTgAgE&adplat=www-index-web_shell_header-flight-missing_creative-CrAksofCVeaQ3cIeUQG6V"  ,
    "https://flights.booking.com/flights/FRA.CITY-BKK.CITY/?type=ROUNDTRIP&adults=2&cabinClass=ECONOMY&children=10%2C8&from=FRA.CITY&to=BKK.CITY&fromCountry=DE&toCountry=TH&fromLocationName=Frankfurt%2FMain&toLocationName=Bangkok&depart=2025-06-01&return=2025-09-01&sort=BEST&travelPurpose=leisure&aid=304142&label=gen173bo-1DEg1mbGlnaHRzX2luZGV4KIICQgVpbmRleEgxWANoO4gBAZgBMbgBF8gBDNgBA-gBAfgBBogCAZgCAqgCA7gCk-DzvAbAAgHSAiRiNjQ4OTI1Yy0wODY4LTRkYTMtYWQ1Ni1hZTg3MDNiYWU5MTjYAgTgAgE&adplat=www-index-web_shell_header-flight-missing_creative-CrAksofCVeaQ3cIeUQG6V",
    "https://flights.booking.com/flights/FRA.CITY-HKG.AIRPORT/?type=ROUNDTRIP&adults=2&cabinClass=ECONOMY&children=10%2C8&from=FRA.CITY&to=HKG.AIRPORT&fromCountry=DE&toCountry=HK&fromLocationName=Frankfurt%2FMain&toLocationName=Hong+Kong+International+Airport&depart=2025-06-01&return=2025-09-01&sort=BEST&travelPurpose=leisure&aid=304142&label=gen173bo-1DEg1mbGlnaHRzX2luZGV4KIICQgVpbmRleEgxWANoO4gBAZgBMbgBF8gBDNgBA-gBAfgBBogCAZgCAqgCA7gCk-DzvAbAAgHSAiRiNjQ4OTI1Yy0wODY4LTRkYTMtYWQ1Ni1hZTg3MDNiYWU5MTjYAgTgAgE&adplat=www-index-web_shell_header-flight-missing_creative-CrAksofCVeaQ3cIeUQG6V",
    "https://flights.booking.com/flights/FRA.CITY-MAD.AIRPORT/?type=ROUNDTRIP&adults=2&cabinClass=ECONOMY&children=10%2C8&from=FRA.CITY&to=MAD.AIRPORT&fromCountry=DE&toCountry=ES&fromLocationName=Frankfurt%2FMain&toLocationName=Adolfo+Suarez+Madrid-Barajas+Airport&depart=2025-06-01&return=2025-09-01&sort=BEST&travelPurpose=leisure&aid=304142&label=gen173bo-1DEg1mbGlnaHRzX2luZGV4KIICQgVpbmRleEgxWANoO4gBAZgBMbgBF8gBDNgBA-gBAfgBBogCAZgCAqgCA7gCk-DzvAbAAgHSAiRiNjQ4OTI1Yy0wODY4LTRkYTMtYWQ1Ni1hZTg3MDNiYWU5MTjYAgTgAgE&adplat=www-index-web_shell_header-flight-missing_creative-CrAksofCVeaQ3cIeUQG6V",
    "https://flights.booking.com/flights/FRA.CITY-RIO.CITY/?type=ROUNDTRIP&adults=2&cabinClass=ECONOMY&children=10%2C8&from=FRA.CITY&to=RIO.CITY&fromCountry=DE&toCountry=BR&fromLocationName=Frankfurt%2FMain&toLocationName=Rio+de+Janeiro&depart=2025-06-01&return=2025-09-01&sort=BEST&travelPurpose=leisure&aid=304142&label=gen173bo-1DEg1mbGlnaHRzX2luZGV4KIICQgVpbmRleEgxWANoO4gBAZgBMbgBF8gBDNgBA-gBAfgBBogCAZgCAqgCA7gCk-DzvAbAAgHSAiRiNjQ4OTI1Yy0wODY4LTRkYTMtYWQ1Ni1hZTg3MDNiYWU5MTjYAgTgAgE&adplat=www-index-web_shell_header-flight-missing_creative-CrAksofCVeaQ3cIeUQG6V",
    "https://flights.booking.com/flights/FRA.CITY-BUE.CITY/?type=ROUNDTRIP&adults=2&cabinClass=ECONOMY&children=10%2C8&from=FRA.CITY&to=BUE.CITY&fromCountry=DE&toCountry=AR&fromLocationName=Frankfurt%2FMain&toLocationName=Buenos+Aires&depart=2025-06-01&return=2025-09-01&sort=BEST&travelPurpose=leisure&aid=304142&label=gen173bo-1DEg1mbGlnaHRzX2luZGV4KIICQgVpbmRleEgxWANoO4gBAZgBMbgBF8gBDNgBA-gBAfgBBogCAZgCAqgCA7gCk-DzvAbAAgHSAiRiNjQ4OTI1Yy0wODY4LTRkYTMtYWQ1Ni1hZTg3MDNiYWU5MTjYAgTgAgE&adplat=www-index-web_shell_header-flight-missing_creative-CrAksofCVeaQ3cIeUQG6V",
    "https://flights.booking.com/flights/FRA.CITY-TUN.AIRPORT/?type=ROUNDTRIP&adults=2&cabinClass=ECONOMY&children=10%2C8&from=FRA.CITY&to=TUN.AIRPORT&fromCountry=DE&toCountry=TN&fromLocationName=Frankfurt%2FMain&toLocationName=Tunis%E2%80%93Carthage+Airport&depart=2025-06-01&return=2025-09-01&sort=BEST&travelPurpose=leisure&aid=304142&label=gen173bo-1DEg1mbGlnaHRzX2luZGV4KIICQgVpbmRleEgxWANoO4gBAZgBMbgBF8gBDNgBA-gBAfgBBogCAZgCAqgCA7gCk-DzvAbAAgHSAiRiNjQ4OTI1Yy0wODY4LTRkYTMtYWQ1Ni1hZTg3MDNiYWU5MTjYAgTgAgE&adplat=www-index-web_shell_header-flight-missing_creative-CrAksofCVeaQ3cIeUQG6V",
    "https://flights.booking.com/flights/FRA.CITY-HEL.AIRPORT/?type=ROUNDTRIP&adults=2&cabinClass=ECONOMY&children=10%2C8&from=FRA.CITY&to=HEL.AIRPORT&fromCountry=DE&toCountry=FI&fromLocationName=Frankfurt%2FMain&toLocationName=Helsinki-Vantaa+Airport&depart=2025-06-01&return=2025-09-01&sort=BEST&travelPurpose=leisure&aid=304142&label=gen173bo-1DEg1mbGlnaHRzX2luZGV4KIICQgVpbmRleEgxWANoO4gBAZgBMbgBF8gBDNgBA-gBAfgBBogCAZgCAqgCA7gCk-DzvAbAAgHSAiRiNjQ4OTI1Yy0wODY4LTRkYTMtYWQ1Ni1hZTg3MDNiYWU5MTjYAgTgAgE&adplat=www-index-web_shell_header-flight-missing_creative-CrAksofCVeaQ3cIeUQG6V",
    "https://flights.booking.com/flights/FRA.CITY-RAK.AIRPORT/?type=ROUNDTRIP&adults=2&cabinClass=ECONOMY&children=10%2C8&from=FRA.CITY&to=RAK.AIRPORT&fromCountry=DE&toCountry=MA&fromLocationName=Frankfurt%2FMain&toLocationName=Marrakech-Menara+Airport&depart=2025-06-01&return=2025-09-01&sort=BEST&travelPurpose=leisure&aid=304142&label=gen173bo-1DEg1mbGlnaHRzX2luZGV4KIICQgVpbmRleEgxWANoO4gBAZgBMbgBF8gBDNgBA-gBAfgBBogCAZgCAqgCA7gCk-DzvAbAAgHSAiRiNjQ4OTI1Yy0wODY4LTRkYTMtYWQ1Ni1hZTg3MDNiYWU5MTjYAgTgAgE&adplat=www-index-web_shell_header-flight-missing_creative-CrAksofCVeaQ3cIeUQG6V"
]

departure_times = []
destination_times = []
durations = []
stops_list = []
airlines_list = []
prices_list = []
destinations=[]
origins=[]
cities =[]
polis = [
    "Palma de Mallorca",
    "Vienna",
    "Paris",
    "Tokyo",
    "Barcelona",
    "London",
    "Cairo",
    "Delhi",
    "Antalya",
    "Dubai",
    "Bangkok",
    "Hong Kong",
    "Madrid",
    "Rio de janeiro",
    "Buenos Aires",
    "Tunis",
    "Helsinki",
    "Marrakech"
]

def citymaker(location, polis):
    for poli in polis:
        if poli.lower() in location.lower():
            return poli

MAX_FLIGHTS = 120 # Limit per link
def add_all_airports(location: str) -> str:
    if "airport" not in location.lower():
        return location + ", All Airports"
    return location
def clean_price(price_text):
    """ Cleans price text by removing symbols and keeping only numbers, commas, and periods. """
    if price_text:
        price_text = price_text.replace("â‚¬", "").strip()
        price_text = re.sub(r"[^\d.,]", "", price_text)  
    return price_text
cities =[]
def scrape_flights(source, destination):
    """ Scrape flight details and store them in lists, stopping at 100 flights. """
    global flight_count
    flight_cards = driver.find_elements(By.XPATH, "//div[contains(@id, 'flight-card-')]")
    
    for flight in flight_cards:
        if flight_count >= MAX_FLIGHTS:
            return  # S
        
        try:
            dep_time = flight.find_element(By.XPATH, ".//div[@data-testid='flight_card_segment_departure_time_0']").text
        except:
            dep_time = "N/A"

        try:
            dest_time = flight.find_element(By.XPATH, ".//div[@data-testid='flight_card_segment_destination_time_0']").text
        except:
            dest_time = "N/A"

        try:
            duration = flight.find_element(By.XPATH, ".//div[@data-testid='flight_card_segment_duration_0']").text
        except:
            duration = "N/A"

        try:
            stops = flight.find_element(By.XPATH, ".//span[@data-testid='flight_card_segment_stops_0']").text
        except:
            stops = "N/A"

        import re

        try:
            airline_elements = flight.find_elements(By.XPATH, ".//div[@data-testid='flight_card_carrier_0']//div[contains(@class, 'Text-module__root--variant-small')]")
            airline = ", ".join([a.text.strip() for a in airline_elements if a.text.strip()])
            
            # Remove symbols but keep words intact
            airline = re.sub(r'[^\w\s]', '', airline)  # Removes only special characters but keeps spaces
            
            # Remove everything after "operated" (case-insensitive)
            airline = re.split(r'\boperated\b', airline, flags=re.IGNORECASE)[0].strip()
        except:
            airline = "N/A"
 

        try:
            price_element = flight.find_element(By.XPATH, ".//div[contains(@data-testid, 'flight_card_price_main_price')]")
            price_raw = price_element.get_attribute("textContent").strip()
            price = clean_price(price_raw)
        except Exception as e:
            price = "error price"
            print(f"Price extraction failed: {e}")



        departure_times.append(dep_time)
        destination_times.append(dest_time)
        durations.append(duration)
        stops_list.append(stops)
        airlines_list.append(airline)
        prices_list.append(price)
        destinations.append(add_all_airports(destination))
        origins.append(source +" airport")
        cities.append(citymaker(destination,polis))   
        flight_count += 1  # Increment flight count

for url in urls:
    driver.get(url)
    time.sleep(15)  

    source = re.search(r"fromLocationName=([^&]+)", url).group(1).replace("+", " ")
    destination = re.search(r"toLocationName=([^&]+)", url).group(1).replace("+", " ")

    flight_count = 0  # Reset flight count for each link
    scrape_flights(source, destination)
    while flight_count < MAX_FLIGHTS:
        try:
            next_button = driver.find_element(By.XPATH, "//*[@id='BEST']/div[2]/div[1]/div/div/div[3]/button")
            if not next_button.is_enabled():
                print(f"Last page reached for {source} → {destination}.")
                break

            driver.execute_script("arguments[0].click();", next_button)
            time.sleep(15)  
            scrape_flights(source, destination)

        except :
            print(f"No more pages for {source} → {destination} or an error occurred:")
            break

driver.quit()

df = pd.DataFrame({
    "Origin": origins,
    "destination":destinations,
    "Airline": airlines_list,
    "Departure Time": departure_times,
    "Arrival Time": destination_times,
    "Duration": durations,
    "Number of Stops": stops_list,
    "Price": prices_list,
    "Currency":"$",
    "City":cities
})



df.to_csv(r"C:/Users/DELL/web scraping/Flights/Booking_flights.csv", index=False)
print(f"Scraping completed! {len(df)} flights saved in 'Booking_flights.csv'.")
