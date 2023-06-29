
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


def convert_df_to_str(df):
    for col in df.columns:
        if df[col].dtype == 'float64':
            df[col] = df[col].apply(lambda x: '{:.9f}'.format(x))  # This will use 5 decimal places
        else:
            df[col] = df[col].astype(str)
    df.replace('nan', np.nan, inplace=True)
    df.replace('None', np.nan, inplace=True)
    return df



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

# For each test case
for _, row in test_cases.iterrows():
    if row['execute'] == 1:
        # Extract the queries and indices from the row
        test_name = row['Test Name']
        sql_subfolder = row['SQL subfolder'] if not pd.isnull(row['SQL subfolder']) else ''
        bigquery_query = get_sql_query(row['Bigquery SQL'], relative_path, variables, sql_subfolder)
        salesforce_query = get_sql_query(row['salesforce SQL'], relative_path, variables, sql_subfolder)
        bigquery_index = [int(index) for index in row['bigquery index'].strip("[]").split(",")]
        salesforce_index = [int(index) for index in row['salesforce index'].strip("[]").split(",")]

        # Just before executing the query
        log_message = "Final BigQuery query: {}".format(bigquery_query)
        logging.info(log_message)

        log_message = "Final Salesforce query: {}".format(salesforce_query)
        logging.info(log_message)   

        # Check if we got valid queries before proceeding
        if bigquery_query is None or salesforce_query is None:
            logging.info(f"Skipping test case '{test_name}' due to invalid SQL query or filename.")
            continue


        # BigQuery
        df_bigquery = client.query(bigquery_query).to_dataframe()
        df_bigquery = convert_df_to_str(df_bigquery)  # This line converts all columns to strings
        bigquery_record_count = len(df_bigquery)
        #print(f'bigquery reocord count : {bigquery_record_count}')

        # Salesforce
        sf_data = sf.query_all(salesforce_query)
        salesforce_record_count = sf_data['totalSize']
        #print(f'salesforce reocord count : {salesforce_record_count}')

        # Add the empty check
        if  salesforce_record_count == 0:  #or bigquery_record_count == 0 
            test_status = 'SALESFORCE RESTULS EMPTY, TEST SKIPPED'
            reason = 'Salesforce dataframe is empty.'
            #reason = 'BigQuery dataframe is empty.' if bigquery_record_count == 0 else 'Salesforce dataframe is empty.'
            log_message = f"Test {test_name} Skipped: {reason}"
            logging.info(log_message)
            
            # Prepare the summary dataframe
            summary_df = pd.DataFrame({
                'Test_Name': [test_name],
                'Test Status': [test_status],
                'Total Rows': [None],
                'Matching Rows': [None],
                'Non-matching Rows': [None],
                'BigQuery Record Count': [bigquery_record_count],
                'Ncino Record Count': [salesforce_record_count]
            }, index=[0])

            total_tests += 1
            all_results.append(summary_df)
            continue

        # Log the raw JSON response
        log_message = "Raw Salesforce JSON Response for test '{}': {}".format(test_name, sf_data)
        logging.info(log_message)

        # Apply 'flatten' function to the list of records
        sf_data_records = [flatten(record) for record in sf_data['records']]
        df_salesforce = pd.DataFrame(sf_data_records)
        df_salesforce = convert_df_to_str(df_salesforce) # This line converts all columns to strings 

        # Handle nested dictionaries
        df_salesforce = handle_nested_dicts(df_salesforce)

        # Drop columns that contain 'attributes' in their name
        df_salesforce = df_salesforce[df_salesforce.columns.drop(list(df_salesforce.filter(regex='attributes')))]

        if 'attributes' in df_salesforce.columns:
            df_salesforce = df_salesforce.drop(columns='attributes')

        # Standardize column names
        df_bigquery.columns = df_bigquery.columns.str.strip().str.lower()
        df_salesforce.columns = df_salesforce.columns.str.strip().str.lower()

         # Log columns before creating index lists
        log_message = "BigQuery columns before index list creation: {}".format(df_bigquery.columns)
        logging.info(log_message)
        
        log_message = "Salesforce columns before index list creation: {}".format(df_salesforce.columns)
        logging.info(log_message)

        # Create the index lists after dropping the 'attributes' columns
        try:
            bigquery_index = df_bigquery.columns[bigquery_index].tolist()
        except KeyError as e:
            logging.error(f"KeyError when creating bigquery_index: {e}")
            continue

        try:
            salesforce_index = df_salesforce.columns[salesforce_index].tolist()
        except KeyError as e:
            logging.error(f"KeyError when creating salesforce_index: {e}")
            continue

        # Create a mapping dictionary for the index columns
        index_mapping = dict(zip(salesforce_index, bigquery_index))
        log_message = "Index Mapping: {}".format(index_mapping)
        logging.info(log_message)

        log_message = "BigQuery columns: {}".format(df_bigquery.columns)
        logging.info(log_message)

        log_message = "Salesforce columns: {}".format(df_salesforce.columns)
        logging.info(log_message)
        
        # Rename the columns in df_salesforce and df_bigquery based on the index mapping
        index_mapping_inverse = {v: k for k, v in index_mapping.items()}
        df_salesforce.rename(columns=index_mapping_inverse, inplace=True)
        df_bigquery.rename(columns=index_mapping_inverse, inplace=True)
        
        # Change to lower case
        index_mapping = {k.lower(): v.lower() for k, v in index_mapping.items()}

        # Merge the dataframes on the index
        merged_df = pd.merge(df_bigquery, df_salesforce, on=list(index_mapping_inverse.values()), how='outer', indicator=True)

        # Rename the labels of the '_merge' column
        merged_df['_merge'] = merged_df['_merge'].map({'left_only': 'bigquery_only', 'right_only': 'salesforce_only', 'both': 'both'})
  
        # Reset index
        df_bigquery.reset_index(drop=True, inplace=True)
        df_salesforce.reset_index(drop=True, inplace=True)

        # Create temporary column names based on Salesforce column names
        temp_cols = [col for col in df_salesforce.columns if col != 'index']

        # Now merge using the temporary column names
        merged_df = pd.merge(df_bigquery, df_salesforce, on=temp_cols, how='outer', indicator=True)

        # Rename the labels of the '_merge' column
        merged_df['_merge'] = merged_df['_merge'].map({'left_only': 'bigquery_only', 'right_only': 'salesforce_only', 'both': 'both'})

        # Count number of matching and non-matching rows
        total_rows = merged_df.shape[0]
        matching_rows = merged_df[merged_df['_merge'] == 'both'].shape[0]
        non_matching_rows = total_rows - matching_rows

        # Count number of matching and non-matching fields
        matching_fields = np.sum(merged_df['_merge'] == 'both')
        total_fields = merged_df.size
        non_matching_fields = total_fields - matching_fields

        # Append the summary to the top of the dataframe
        summary_df = pd.DataFrame({
            'Total Rows': [total_rows],
            'Matching Rows': [matching_rows],
            'Non-matching Rows': [non_matching_rows],
        })

        # Save the summary dataframe to a CSV file
        results_dir = os.path.join(relative_path, 'Results')
        os.makedirs(results_dir, exist_ok=True)
        summary_file_path = os.path.join(results_dir, f'{test_name}_results.csv')
        summary_df.to_csv(summary_file_path)

        # Append the merged dataframe to the same CSV file
        merged_df.to_csv(summary_file_path, mode='a')

        # If you only want to see the differences, you can filter the rows where '_merge' is not 'both'
        differences_df = merged_df[merged_df['_merge'] != 'both']
        log_message = "Differences between datasets: {}".format(differences_df) 
        logging.info(log_message)
        #logging.info(differences_df)

        # Check if the DataFrames are equal
        if df_bigquery.sort_values(by=list(df_bigquery.columns)).reset_index(drop=True).equals(df_salesforce.sort_values(by=list(df_salesforce.columns)).reset_index(drop=True)):
            log_message = "Test {} Passed: Both BigQuery and Salesforce results match.".format(test_name)
            logging.info(log_message)

        else:
            log_message = "Test {} Failed: BigQuery and Salesforce results do not match.".format(test_name)
            logging.info(log_message)
            failed_tests.append(f"Test {test_name} Failed: BigQuery and Salesforce results do not match.")

        # Compute total and matching rows
        total_rows = len(merged_df)
        matching_rows = len(merged_df[merged_df['_merge'] == 'both'])
        non_matching_rows = total_rows - matching_rows
        total_rows1 = bigquery_record_count + salesforce_record_count

        # Prepare the test status
        test_status = 'Pass' if non_matching_rows == 0 else 'Fail'

        # Write the results dataframe to a separate CSV file
        merged_df.to_csv(os.path.join(results_dir, f'{test_name}_results.csv'), index=True)


        # If the test failed, add it to the list of failed tests
        if not df_bigquery.sort_values(by=list(df_bigquery.columns)).reset_index(drop=True).equals(df_salesforce.sort_values(by=list(df_salesforce.columns)).reset_index(drop=True)):
            failed_tests.append(test_name)
        
        # Prepare the summary dataframe
        summary_df = pd.DataFrame({
            'Test_Name': [test_name],
            'Test Status': [test_status],
            'Total Rows': [total_rows1],
            'Matching Rows': [matching_rows],
            'Non-matching Rows': [non_matching_rows],
            'BigQuery Record Count': [bigquery_record_count],
            'Ncino Record Count': [salesforce_record_count]
        }, index=[0])

        # collect results for summary
        total_tests += 1
        if test_status == 'Pass':
            total_passed += 1
        else:
            total_failed += 1

        # Store the test result summary
        all_results.append(summary_df)

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
