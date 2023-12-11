import os
import json
import csv
import argparse

def process_json_files(input_dir, output_dir):
    toll_data = []
    
    for file_name in os.listdir(input_dir):
        if file_name.endswith('.json'):
            file_path = os.path.join(input_dir, file_name)
            
            with open(file_path, 'r') as json_file:
                data = json.load(json_file)
                # print(data)
                # if data and 'tolls' in data and data['tolls']:
                    
                    
                for toll in data['route']['tolls']:
                    trip_id = file_name.replace('.json', '')
                    units=file_name.split("_")[0]
                    # print(toll)
                    # print(toll["start"]['id'])
                    toll_info = {
                        'unit': units,
                        'trip_id': trip_id,
                        'toll_loc_id_start': toll["start"]['id'],
                        'toll_loc_id_end': toll["end"]['id'],
                        'toll_loc_name_start': toll["start"]['name'],
                        'toll_loc_name_end': toll["end"]['name'],
                        'toll_system_type': toll["type"],
                        'entry_time': toll["start"]['arrival']['time'],
                        'exit_time': toll["end"]['arrival']['time'],
                        'tag_cost': toll["tagCost"],
                        'cash_cost': toll["cashCost"],
                        'license_plate_cost': toll["licensePlateCost"]
                    }
                    
                    # Handle null values by replacing them with an empty string
                    for key in toll_info:
                        if toll_info[key] is None:
                            toll_info[key] = ''

                    toll_data.append(toll_info)
    
    if toll_data:
        output_file = os.path.join(output_dir, 'transformed_data.csv')
        with open(output_file, 'w', newline='') as csv_file:
            fieldnames = ['unit', 'trip_id', 'toll_loc_id_start', 'toll_loc_id_end', 'toll_loc_name_start',
                          'toll_loc_name_end', 'toll_system_type', 'entry_time', 'exit_time', 'tag_cost',
                          'cash_cost', 'license_plate_cost']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            
            writer.writeheader()
            writer.writerows(toll_data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process toll information from JSON files')
    parser.add_argument('--to_process', type=str, help='Path to the JSON responses folder')
    parser.add_argument('--output_dir', type=str, help='Output directory for transformed_data.csv')
    args = parser.parse_args()

    input_directory = args.to_process
    output_directory = args.output_dir

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    process_json_files(input_directory, output_directory)
