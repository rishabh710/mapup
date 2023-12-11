import pandas as pd
import argparse
from datetime import datetime, timedelta
import os
import warnings
warnings.simplefilter("ignore")

def extract_trips(input_file, output_dir):
    # Read Parquet file
    data = pd.read_parquet(input_file)
    
    # Convert timestamp column to datetime
    data['timestamp'] = pd.to_datetime(data['timestamp'])
    
    # Sort data by unit and timestamp
    data.sort_values(by=['unit', 'timestamp'], inplace=True)
    
    # Group data by unit
    grouped = data.groupby('unit')
    
    # Process each unit
    for unit, unit_data in grouped:
        trip_number = 0
        prev_time = None
        trip_data = pd.DataFrame()
        
        for index, row in unit_data.iterrows():
            if prev_time is None or (row['timestamp'] - prev_time > timedelta(hours=7)):
                # Start a new trip
                if not trip_data.empty:
                    # Save previous trip data
                    trip_file = os.path.join(output_dir, f"{unit}_{trip_number}.csv")
                    trip_data=trip_data.drop(['unit'],axis=1)
                    trip_data.to_csv(trip_file, index=False)
                    trip_number += 1
                    trip_data = pd.DataFrame()
            
            # Add row to the current trip data
            trip_data = trip_data.append(row, ignore_index=True)
            prev_time = row['timestamp']
        
        # Save the last trip data
        if not trip_data.empty:
            trip_file = os.path.join(output_dir, f"{unit}_{trip_number}.csv")
            trip_data=trip_data.drop(['unit'],axis=1)
            trip_data.to_csv(trip_file, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process GPS data to extract trips')
    parser.add_argument('--to_process', type=str, help='Path to the Parquet file')
    parser.add_argument('--output_dir', type=str, help='Output directory for CSV files')
    args = parser.parse_args()

    input_file = args.to_process
    output_directory = args.output_dir

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    extract_trips(input_file, output_directory)
