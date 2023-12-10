import requests
import os
import argparse
import pandas as pd
from dotenv import load_dotenv

def adjust_timestamp_format(timestamp):
    # Convert timestamp to the expected format
    formatted_timestamp = pd.to_datetime(timestamp).strftime('%Y-%m-%dT%H:%M:%SZ')
    return formatted_timestamp

def upload_to_tollguru(input_dir, output_dir, api_key, api_url):
    load_dotenv()  # Load environment variables from .env file
    api_key = os.getenv('TOLLGURU_API_KEY')
    api_url = os.getenv('TOLLGURU_API_URL')
    # Iterate through CSV files in the input directory
    for file_name in os.listdir(input_dir):
        if file_name.endswith('.csv'):
            file_path = os.path.join(input_dir, file_name)
            url = f"{api_url}?mapProvider=osrm&vehicleType=5AxlesTruck"
            headers = {'x-api-key': api_key, 'Content-Type': 'text/csv'}

            # Read CSV file
            df = pd.read_csv(file_path)
            
            # Adjust timestamp format
            df['timestamp'] = df['timestamp'].apply(adjust_timestamp_format)
            
            # Save the adjusted CSV temporarily
            adjusted_file_path = os.path.join(output_dir, 'adjusted.csv')
            df.to_csv(adjusted_file_path, index=False)
            
            with open(adjusted_file_path, 'rb') as file:
                response = requests.post(url, data=file, headers=headers)
                
                if response.status_code == 200:
                    # Save JSON response with the same filename in the output directory
                    output_file_path = os.path.join(output_dir, file_name.replace('.csv', '.json'))
                    with open(output_file_path, 'w') as output_file:
                        output_file.write(response.text)
                else:
                    print(f"Failed to upload {file_name}: {response.text}")

            # Remove the adjusted file
            os.remove(adjusted_file_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Upload GPS tracks to TollGuru API')
    parser.add_argument('--to_process', type=str, help='Path to the CSV folder')
    parser.add_argument('--output_dir', type=str, help='Output directory for JSON files')
    args = parser.parse_args()

    input_directory = args.to_process
    output_directory = args.output_dir
    # api_key = ''  # Replace with your actual TollGuru API key
    # api_url = 'https://apis.tollguru.com/toll/v2/gps-tracks-csv-upload'

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    upload_to_tollguru(input_directory, output_directory)
