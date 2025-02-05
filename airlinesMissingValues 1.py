import pandas as pd

def clean_airline_data(input_file: str, output_file: str):
    """
    Removes rows where the airline name is 'NOT FOUND' and saves the cleaned dataset.
    
    :param input_file: Path to the input CSV file.
    :param output_file: Path to save the cleaned CSV file.
    """
    # Load the dataset
    df = pd.read_csv(input_file)
    
    # Remove rows where the Name column is "NOT FOUND"
    df_cleaned = df[df["Name"] != "NOT FOUND"]
    
    # Save the cleaned dataset
    df_cleaned.to_csv(output_file, index=False)
    
    print(f"Cleaned data saved to {output_file}")

clean_airline_data('"C:/Users/DELL/web scraping/Flights/airlines.csv', '"C:/Users/DELL/web scraping/Flights/cleaned_airlines.csv')