
import logging
import os
from datetime import datetime
from google.cloud import bigquery
import pandas as pd
import numpy as np
from functions import flatten, handle_nested_dicts, get_sql_query

def configure_logging(log_filename):
    log_format = "%(asctime)s - %(levelname)s - %(message)s"
    logging.basicConfig(filename=log_filename, level=logging.INFO, format=log_format)

def run_test_cases(test_cases, client, sf, variables, relative_path):
    results_dir = os.path.join(relative_path, 'Results')
    os.makedirs(results_dir, exist_ok=True)
    log_filename = os.path.join(results_dir, 'test_log.log')
    configure_logging(log_filename)

    total_tests = 0
    total_passed = 0
    total_failed = 0
    all_results = []

    for _, row in test_cases.iterrows():
        if row['execute'] == 1:
            test_name = row['Test Name']
            sql_subfolder = row.get('SQL subfolder', '')
            bigquery_query = get_sql_query(row['Bigquery SQL'], relative_path, variables, sql_subfolder)
            salesforce_query = get_sql_query(row['salesforce SQL'], relative_path, variables, sql_subfolder)
            bigquery_index = [int(index) for index in row['bigquery index'].strip("[]").split(",")]
            salesforce_index = [int(index) for index in row['salesforce index'].strip("[]").split(",")]

            logging.info("Running test: %s", test_name)
            logging.info("Final BigQuery query: %s", bigquery_query)
            logging.info("Final Salesforce query: %s", salesforce_query)

            if bigquery_query is None or salesforce_query is None:
                logging.warning("Skipping test case '%s' due to invalid SQL query or filename.", test_name)
                continue

            try:
                df_bigquery = client.query(bigquery_query).to_dataframe()
                df_bigquery = df_bigquery.astype(str)
                df_bigquery.replace('None', '', inplace=True)
                bigquery_record_count = len(df_bigquery)

                sf_data = sf.query_all(salesforce_query)
                salesforce_record_count = sf_data['totalSize']

                if salesforce_record_count == 0:
                    test_status = 'FAIL ,SALESFORCE RESULTS EMPTY, TEST SKIPPED'
                    reason = 'Salesforce dataframe is empty.'
                    total_failed += 1
                    logging.warning("Test %s Skipped: %s", test_name, reason)
                    summary_df = pd.DataFrame({
                        'Test_Name': [test_name],
                        'Test Status': [test_status],
                        'Total Rows': [None],
                        'Matching Rows': [None],
                        'Non-matching Rows': [None],
                        'BigQuery Record Count': [bigquery_record_count],
                        'Salesforce Record Count': [salesforce_record_count]
                    }, index=[0])
                    total_tests += 1
                    all_results.append(summary_df)
                    continue

                logging.info("Raw Salesforce JSON Response for test '%s': %s", test_name, sf_data)
                sf_data_records = [flatten(record) for record in sf_data['records']]
                df_salesforce = pd.DataFrame(sf_data_records)
                df_salesforce = df_salesforce.astype(str)
                df_salesforce.replace('nan', '', inplace=True)
                df_salesforce.replace('None', '', inplace=True)

                df_salesforce = handle_nested_dicts(df_salesforce)
                df_salesforce = df_salesforce[df_salesforce.columns.drop(list(df_salesforce.filter(regex='attributes')))]

                if 'attributes' in df_salesforce.columns:
                    df_salesforce = df_salesforce.drop(columns='attributes')

                df_bigquery.columns = df_bigquery.columns.str.strip().str.lower()
                df_salesforce.columns = df_salesforce.columns.str.strip().str.lower()

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
                log_message = "Index Mapping: %s", index_mapping
                logging.info(log_message)

                log_message = "BigQuery columns: %s", df_bigquery.columns
                logging.info(log_message)

                log_message = "Salesforce columns: %s", df_salesforce.columns
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

                # ... (rest of the code)

            except Exception as e:
                logging.error("Error in test '%s': %s", test_name, e)

            # ... (rest of the code)

    return total_tests, total_passed, total_failed, all_results, results_dir
