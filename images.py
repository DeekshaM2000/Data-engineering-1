import pandas as pd

# Load existing tables
airlines_df = pd.read_csv("C:/Users/DELL/web scraping/Flights/data/airlines.csv")  # Replace with actual file path
cities_df = pd.read_csv("C:/Users/DELL/web scraping/Flights/data/cities.csv")      # Replace with actual file path

# Create Images Table
images_data = []

# Add airline images
for _, row in airlines_df.iterrows():
    images_data.append(["Airline", row["Name"], row["Logo"]])

# Add city images
for _, row in cities_df.iterrows():
    images_data.append(["City", row["City"], row["Image"]])

images_df = pd.DataFrame(images_data, columns=["Entity Type", "Entity Name", "Image URL"])
images_df.to_csv(r"C:\Users\DELL\web scraping\Flights\data\images.csv", index=False)

print("Images table has been created successfully!")