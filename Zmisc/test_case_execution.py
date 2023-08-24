# 2nd Script  - test_case_execution.py
from functions import flatten, handle_nested_dicts, get_sql_query
from google.cloud import bigquery
import pandas as pd
import numpy as np
import logging
import os
from datetime import datetime

def run_test_cases(test_cases, client, sf, variables, relative_path, total_tests, total_passed, total_failed, all_results):
# Create results directory before entering the loop
    results_dir = os.path.join(relative_path, 'Results')
    os.makedirs(results_dir, exist_ok=True)

    # Initialize an empty list to store the failed tests
    failed_tests = []

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
            df_bigquery = df_bigquery.astype(str)  # This line converts all columns to strings
            df_bigquery.replace('None', '', inplace=True) 
            bigquery_record_count = len(df_bigquery) #print(f'bigquery reocord count : {bigquery_record_count}')

            # Salesforce
            sf_data = sf.query_all(salesforce_query)
            salesforce_record_count = sf_data['totalSize']
            #print(f'salesforce reocord count : {salesforce_record_count}')

            # Add the empty check
            if  salesforce_record_count == 0:  #or bigquery_record_count == 0 
                test_status = 'FAIL ,SALESFORCE RESTULS EMPTY, TEST SKIPPED'
                reason = 'Salesforce dataframe is empty.'
                total_failed += 1
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
            df_salesforce = df_salesforce.astype(str) # This line converts all columns to strings 
            df_salesforce.replace('nan', '', inplace=True)  # Replace 'nan' with an empty string
            df_salesforce.replace('None', '', inplace=True) 

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

    return total_tests, total_passed, total_failed, all_results, results_dir
