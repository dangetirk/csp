#This Python script performs the following operations:

#It reads the test cases from a CSV file.
#It loops through each test case and checks if it needs to be executed.
#For each test case to be executed, it fetches data from both BigQuery and Salesforce using the SQL queries provided in the CSV file.
#It then handles any nested dictionaries in the Salesforce data.
#It checks if any columns in Salesforce data are dictionaries and if so, extracts the relevant data.
#It creates a mapping dictionary for the index columns and renames Salesforce columns to match BigQuery columns.
#It standardizes the column names in both data sets.
#It sorts both data sets based on index columns and resets the index.
#It compares the two data sets and records the differences.
#Finally, it writes the comparison results to a CSV file.

#the headings in the results are based on the column names in the saleforce queries. 

from simple_salesforce import Salesforce
from google.cloud import bigquery
from functions import flatten, handle_nested_dicts, get_sql_query
import yaml
import logging
import pandas as pd
import os
import numpy as np
import collections
from datetime import datetime
from test_case_execution import run_test_cases

# Load the configuration file
with open("config.yml", 'r') as ymlfile:
    cfg = yaml.safe_load(ymlfile)

# Access the configurations
sf_username = cfg['salesforce']['username']
sf_password = cfg['salesforce']['password']
sf_consumer_key = cfg['salesforce']['consumer_key']
sf_consumer_secret = cfg['salesforce']['consumer_secret']
sf_domain = cfg['salesforce']['domain']
csv_filename = cfg['csv']['filename']
project_ID = cfg['bigquery']['project_ID']
dataset1 = cfg['bigquery']['dataset1']
logging_enabled = cfg.get('logging', False)  # default to False if 'logging' is not set

# Create 'logs' directory if it doesn't exist
if not os.path.exists('logs'):
    os.makedirs('logs')

# Set up logging
if logging_enabled:
    # Create 'logs' directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # Create a filename with a timestamp
    log_filename = datetime.now().strftime('logs/logfile_%Y_%m_%d_%H_%M_%S.log')

    logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
else:
    logging.disable(logging.CRITICAL)  # disable all logging calls

# test timestamp for summary
run_timestamp = datetime.now()
run_timestamp_str = run_timestamp.strftime('%Y%m%d%H%M%S')

# counters for test summary
total_tests = 0
total_passed = 0
total_failed = 0

# for storing all results
all_results = []

# create a BigQuery client
client = bigquery.Client()

# Use the configurations
sf = Salesforce(username=sf_username, password=sf_password, consumer_key=sf_consumer_key, consumer_secret=sf_consumer_secret, domain=sf_domain)

# Define the relative path
relative_path = os.path.dirname(os.path.abspath(__file__))

# Read test cases from CSV
test_cases = pd.read_csv(os.path.join(relative_path, csv_filename))
test_cases.columns = test_cases.columns.str.strip() #remove whitespace

assert not test_cases.empty, "Test cases dataframe is empty. Check your 'tests.csv' file."
assert all(x in test_cases.columns for x in ['Test Name', 'Bigquery SQL', 'salesforce SQL', 'bigquery index', 'salesforce index', 'execute', 'SQL subfolder', 'comments']), "Not all columns found in the dataframe. Check your 'tests.csv' file."

# Initialize an empty list to store the failed tests
failed_tests = []

#big query variables
variables = {
    'project_ID': cfg['bigquery']['project_ID'],
    'dataset1': cfg['bigquery']['dataset1'],
    # Add more variables as needed...
}

# After loading variables
log_message = "Loaded project_ID: {}".format(variables['project_ID'])
logging.info(log_message)

#call test case execution
total_tests, total_passed, total_failed, all_results, results_dir = run_test_cases(
    test_cases, client, sf, variables, relative_path, total_tests, total_passed, total_failed, all_results
)

# After test have run Concatenate all results
all_results_df = pd.concat(all_results)

# Add total tests, total passed, and total failed at the bottom
summary_stats_df = pd.DataFrame({
    'Test_Name': ['Total Tests', 'Total Passed', 'Total Failed'],
    'Test Status': ['-', '-', '-'],
    'Total Rows': [total_tests, total_passed, total_failed],
    'Matching Rows': [np.nan, np.nan, np.nan],
    'Non-matching Rows': [np.nan, np.nan, np.nan],
    'BigQuery Record Count': [np.nan, np.nan, np.nan],  # Adjusted for the added column
    'Ncino Record Count': [np.nan, np.nan, np.nan]
}, index=[total_tests, total_tests+1, total_tests+2])
all_results_df = pd.concat([all_results_df, summary_stats_df])

# Order the columns
cols = ['Test_Name', 'Test Status', 'Total Rows', 'Matching Rows', 'Non-matching Rows', 'BigQuery Record Count', 'Ncino Record Count']
all_results_df = all_results_df[cols]

# Write the merged results dataframe to a separate CSV file
all_results_df.to_csv(os.path.join(results_dir, f'execution_report_{run_timestamp_str}.csv'), index=False)


# After all tests have run, raise exceptions for any failed tests at the end
if failed_tests:
    raise Exception('Failed tests:\n' + '\n'.join(failed_tests))