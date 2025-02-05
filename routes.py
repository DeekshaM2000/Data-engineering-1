import pandas as pd

# Load existing flights table
flights_df = pd.read_csv(r"C:\Users\DELL\web scraping\Flights\data\flights.csv")  # Replace with actual file path

# Create Routes Table
routes_data = []
unique_routes = flights_df.groupby(["Origin", "destination", "Airline"])["Price"].agg(["min", "max"]).reset_index()

for _, row in unique_routes.iterrows():
    routes_data.append([f"{row['Origin']} - {row['destination']}", row["Origin"], row["destination"], row["Airline"], row["min"], row["max"]])

routes_df = pd.DataFrame(routes_data, columns=["Route ID", "Origin", "Destination", "Airlines Operating", "Minimum Price", "Maximum Price"])
routes_df.to_csv("C:/Users/DELL/web scraping/Flights/data/routes.csv", index=False)

print("Routes table has been created successfully!")
