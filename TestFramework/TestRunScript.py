import os
import pandas as pd
import csv
from datetime import datetime
from simple_salesforce import Salesforce
from google.cloud import bigquery
import logging
import configparser

# Read the configuration file
config = configparser.ConfigParser(interpolation=None)
config.read('config.ini')
# Fetching configuration from the .ini file
RESULTS_PATH = config['DEFAULT']['RESULTS_PATH']
LOG_LEVEL = config['DEFAULT']['LOG_LEVEL']
log_format = config['DEFAULT']['LOG_FORMAT']
LOG_FILENAME = config['DEFAULT']['LOG_FILENAME']
LOG_FILEMODE = config['DEFAULT']['LOG_FILEMODE']
NUMERIC_TOLERANCE = config.getfloat('DEFAULT', 'NUMERIC_TOLERANCE')
MASTER_SUMMARY_FILE = config['DEFAULT']['MASTER_SUMMARY_FILE']
INPUT_CSV = config['DEFAULT']['INPUT_CSV']
SOURCE_FOLDER = config['DEFAULT']['SOURCE_FOLDER']
REPORT_FOLDER = config['DEFAULT']['REPORT_FOLDER']
RESULTS_FOLDER = config['DEFAULT']['RESULTS_FOLDER']
SQL_PATH = config['DEFAULT']['SQL_PATH']
df = pd.read_csv(INPUT_CSV)
value = df.iloc[0, 3] 
if not os.path.exists(REPORT_FOLDER):
    os.makedirs(REPORT_FOLDER)
log_format = config['DEFAULT']['LOG_FORMAT']
logging.basicConfig(level=logging.INFO,
                    format=log_format,
                    filename='script.log',
                    filemode='w')


def get_next_serial_number(master_summary_file):
    """
    Fetch the next serial number for the report. 
    If the file doesn't exist, it starts from 1.
    If it does exist, it increments the last number.
    """
    if os.path.exists(master_summary_file):
        with open(master_summary_file, 'r') as f:
            last_line = f.readlines()[-1]
            last_serial_no = int(last_line.split(",")[0])
            return last_serial_no + 1
    return 1

def execute_salesforce_query(sql_query, output_file):
    sf = Salesforce(
        username=config.get('SALESFORCE', 'USERNAME'),
        password=config.get('SALESFORCE', 'PASSWORD'),
        consumer_key=config.get('SALESFORCE', 'CONSUMER_KEY'),
        consumer_secret= config.get('SALESFORCE', 'CONSUMER_SECRET'),
        domain='test'
    )
    result = sf.query_all(sql_query)
    records = result['records']

    with open(output_file, 'w', newline='') as output:
        csv_writer = csv.writer(output)
        headers = [field for field in records[0].keys() if field != 'attributes']
        csv_writer.writerow(headers)
        for record in records:
            csv_writer.writerow([record[field] for field in headers])

def execute_bigquery_query(sql_query, output_file):
    client = bigquery.Client()
    query_job = client.query(sql_query)
    results = query_job.result()

    with open(output_file, 'w', newline='') as output:
        csv_writer = csv.writer(output)
        headers = [field.name for field in results.schema]
        csv_writer.writerow(headers)
        for row in results:
            csv_writer.writerow(row.values())



# Functions for generating timestamped folder names, comparing CSV files, and generating reports
def generate_timestamped_folder_name():
    return datetime.now().strftime('%Y%m%d_%H%M%S')

def compare_csv_files(file1, file2, numeric_tolerance=1e-10):
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    common_columns = [col for col in df1.columns if col in df2.columns and col != '_merge']

    # Identify numeric columns
    numeric_columns = df1.select_dtypes(include=['float64']).columns.intersection(common_columns)

    # Round numeric columns to the desired precision
    for col in numeric_columns:
        df1[col] = df1[col].round(10)
        df2[col] = df2[col].round(10)

    combined = pd.concat([df1[common_columns].assign(_merge='Salesforce'), df2[common_columns].assign(_merge='BigQuery')])

    differences = combined[combined.duplicated(subset=common_columns, keep=False) == False]

    return differences

def generate_summary_report(sf_csv, bq_csv, comparison_result):
    sf_count = len(pd.read_csv(sf_csv))
    bq_count = len(pd.read_csv(bq_csv))
    differences_count = len(comparison_result)
    
    if sf_count and bq_count:
        percentage_diff = abs(sf_count - bq_count) * 100.0 / max(sf_count, bq_count)
    else:
        percentage_diff = 0

    summary = {
        'Test Case Name': None,  # Placeholder for Test Case Name; will be assigned later
        'Salesforce Record Count': sf_count,
        'BigQuery Record Count': bq_count,
        'Percentage Difference (%)': round(percentage_diff, 2),
        'Differences Found': differences_count,
        'Result': 'Pass' if differences_count == 0 else 'Fail',
        'Comparison Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    return summary
def append_to_master_summary(tcname, summary, timestamp):

    master_summary_file = os.path.join(REPORT_FOLDER, value, f"{value}_TestResult_{timestamp}.csv")
   
    #master_summary_file = f"results/master_summary_{timestamp}.csv"
    #master_summary_file = os.path.join(RESULTS_FOLDER, "master_summary.csv")

    summary['TC#'] = get_next_serial_number(master_summary_file)
    summary['Test Case Name'] = tcname

    # We need to reorder the dictionary to include the new 'Result' column
    ordered_summary = {k: summary[k] for k in ['TC#', 'Test Case Name', 'Salesforce Record Count', 'BigQuery Record Count', 'Differences Found', 'Result', 'Comparison Timestamp']}

    if not os.path.exists(master_summary_file):
        with open(master_summary_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=ordered_summary.keys())
            writer.writeheader()
            writer.writerow(ordered_summary)
    else:
        with open(master_summary_file, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=ordered_summary.keys())
            writer.writerow(ordered_summary)
def generate_comparison_report(test_case_name, source_folder, sf_csv, bq_csv, timestamped_folder, timestamp):
    comparison_result = compare_csv_files(sf_csv, bq_csv)
    
    # report_file = os.path.join("results", source_folder, "reports", timestamped_folder, f"{test_case_name}_Comparison_Report.csv")
    report_file = os.path.join(REPORT_FOLDER, value, "reports", timestamped_folder, f"{test_case_name}_Comparison_Report.csv")
    #print(f"Saving report to: {report_file}")  # Debug print
    summary = generate_summary_report(sf_csv, bq_csv, comparison_result)
    append_to_master_summary(test_case_name, summary, timestamp)

    if not comparison_result.empty:
        comparison_result.to_csv(report_file, index=False)
        print(f"Differences found between {sf_csv} and {bq_csv}. Comparison report saved to {report_file}")
    else:
        print(f"No differences found between {sf_csv} and {bq_csv}.")

# Process test cases function
def process_test_cases(csv_file):
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    timestamped_folder = generate_timestamped_folder_name()

    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                tcname = row['tcname']
                base_report_folder = config.get('DEFAULT', 'RESULTS_FOLDER')
                reports_dir1 = config.get('DEFAULT', 'RESULTS_FOLDER')
                source_folder = config.get('DEFAULT', 'SOURCE_FOLDER')
                source_name = row['Source']
                # Modified path creation
                results_path = os.path.join(base_report_folder, "Results")
                extracts_dir = os.path.join(results_path, source_name, "extracts", timestamped_folder)
                reports_dir = os.path.join(results_path, source_name, "reports", timestamped_folder)

                # Directory creation
                for dir_path in [extracts_dir, reports_dir]:
                    if not os.path.exists(dir_path):
                       # print(f"Creating directory: {dir_path}")  # Debug print
                        os.makedirs(dir_path)

                bigquery_sql_file = os.path.join(source_folder, row['biqquerysqlfile'])
                salesforce_sql_file = os.path.join(source_folder, row['salesforcesqlfile'])

                
                print(f"Processing test case: {tcname} for source: {source_name}")  # This will print the current test case name and source name
                #print(source_name)  # This will print the current test case name and source name


                               
                if os.path.exists(bigquery_sql_file):
                    bq_output_file = os.path.join(extracts_dir, f"{tcname}_BG.csv")
                    with open(bigquery_sql_file, 'r') as bq_file:
                        bigquery_sql_query = bq_file.read()
                        execute_bigquery_query(bigquery_sql_query, bq_output_file)
                else:
                    logging.warning(f"BigQuery SQL file '{bigquery_sql_file}' not found for test case '{tcname}'")
                    continue

                if os.path.exists(salesforce_sql_file):
                    sf_output_file = os.path.join(extracts_dir, f"{tcname}_SF.csv")
                    with open(salesforce_sql_file, 'r') as sf_file:
                        salesforce_sql_query = sf_file.read()
                        execute_salesforce_query(salesforce_sql_query, sf_output_file)
                else:
                    logging.warning(f"Salesforce SQL file '{salesforce_sql_file}' not found for test case '{tcname}'")
                    continue

                generate_comparison_report(tcname, source_folder, sf_output_file, bq_output_file, timestamped_folder, timestamp)
                
            except Exception as e:
                logging.error(f"Error processing test case {row['tcname']}. Error: {e}")
                continue

if __name__ == "__main__":
    try:
        file_path = os.path.join(INPUT_CSV)
        print(f"Attempting to access file at: {file_path}")
        process_test_cases(file_path)
    except Exception as e:
        logging.error(f"Script encountered an error: {e}")

