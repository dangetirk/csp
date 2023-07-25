import json
import csv

def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def write_csv_file(file_path, data, fieldnames):
    with open(file_path, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def separate_data(json_data):
    metadata = json_data.get('metadata', {})
    results = json_data.get('results', [])
    args = metadata.pop('env', {})

    return metadata, results, args

# Read the JSON file
json_data = read_json_file('/Users/Ratna-Kumar.Dangeti/Documents/GitHub/csp/target/run_results.json')

# Separate the data
metadata, results, args = separate_data(json_data)

# Write metadata to CSV
write_csv_file('metadata.csv', [metadata], metadata.keys())

# Write results to CSV
write_csv_file('results.csv', results, results[0].keys())

# Convert args to a list of dictionaries
args_data = [{'key': key, 'value': value} for key, value in args.items()]

# Write args to CSV
write_csv_file('args.csv', args_data, ['key', 'value'])


print("Data separated and saved successfully!")
