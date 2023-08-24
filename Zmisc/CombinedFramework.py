import os
import pandas as pd
import numpy as np
import logging
from datetime import datetime
from google.cloud import bigquery
from simple_salesforce import Salesforce
from jinja2 import Template, UndefinedError
import yaml

def load_configuration(filepath):
    with open(filepath, 'r') as ymlfile:
        cfg = yaml.safe_load(ymlfile)
    return cfg

def setup_logging(enabled):
    log_dir = 'logs'
    if enabled:
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        log_filename = datetime.now().strftime(f'{log_dir}/logfile_%Y_%m_%d_%H_%M_%S.log')
        logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    else:
        logging.disable(logging.CRITICAL)

def load_test_cases(relative_path, filename):
    df = pd.read_csv(os.path.join(relative_path, filename))
    df.columns = df.columns.str.strip()
    required_cols = ['Test Name', 'Bigquery SQL', 'salesforce SQL', 'bigquery index', 'salesforce index', 'execute', 'SQL subfolder', 'comments']

    if df.empty:
        logging.error("Test cases dataframe is empty. Check your 'tests.csv' file.")
        raise ValueError("Test cases dataframe is empty. Check your 'tests.csv' file.")

    if not all(x in df.columns for x in required_cols):
        logging.error("Not all columns found in the dataframe. Check your 'tests.csv' file.")
        raise ValueError("Not all columns found in the dataframe. Check your 'tests.csv' file.")

    return df

def flatten(data, prefix=''):
    result = {}
    for key, value in data.items():
        new_key = f'{prefix}{key}'
        if isinstance(value, dict):
            result.update(flatten(value, f'{new_key}_'))
        elif value is None and new_key.endswith('__r'):
            result[f'{new_key}_LLC_BI__lookupKey__c'] = None
        else:
            result[new_key] = value
    return result

def handle_nested_dicts(df):
    for column in df.columns:
        if column.startswith('attributes'):
            continue
        if isinstance(df[column].iloc[0], dict):
            dict_keys = df[column].iloc[0].keys()
            for key in dict_keys:
                if key == 'attributes':
                    continue
                df[f'{column}_{key}'] = df[column].apply(lambda x: x[key] if isinstance(x, dict) else np.nan)
            df = df.drop(columns=[column])
    return df

def get_sql_query(query_or_filename, relative_path, variables=None, subfolder=''):
    query_template = None

    if query_or_filename.endswith('.txt') or query_or_filename.endswith('.sql'):
        try:
            if subfolder:
                file_path = os.path.join(relative_path, 'SQL', subfolder, query_or_filename)
            else:
                file_path = os.path.join(relative_path, 'SQL', query_or_filename)

            with open(file_path, 'r') as file:
                query_template = file.read().strip()
        except FileNotFoundError:
            print(f'Error: File {query_or_filename} not found in directory {file_path}. Skipping this query.')
            return None
    else:
        query_template = query_or_filename

    if variables:
        template = Template(query_template)
        try:
            query = template.render(variables)
        except UndefinedError as e:
            print(f"Undefined variable in template: {e}")
            query = None
        return query
    else:
        return query_template

def run_test_cases(test_cases, client, sf, variables, relative_path, total_tests, total_passed, total_failed, all_results):
    results_dir = os.path.join(relative_path, 'Results')
    os.makedirs(results_dir, exist_ok=True)
    failed_tests = []

    for _, row in test_cases.iterrows():
        if row['execute'] == 1:
            test_name = row['Test Name']
            sql_subfolder = row['SQL subfolder'] if not pd.isnull(row['SQL subfolder']) else ''
            bigquery_query = get_sql_query(row['Bigquery SQL'], relative_path, variables, sql_subfolder)
            salesforce_query = get_sql_query(row['salesforce SQL'], relative_path, variables, sql_subfolder)
            bigquery_index = [int(index) for index in row['bigquery index'].strip("[]").split(",")]
            salesforce_index = [int(index) for index in row['salesforce index'].strip("[]").split(",")]

            logging.info(f"Final BigQuery query: {bigquery_query}")
            logging.info(f"Final Salesforce query: {salesforce_query}")

            if bigquery_query is None or salesforce_query is None:
                logging.info(f"Skipping test case '{test_name}' due to invalid SQL query or filename.")
                continue

            df_bigquery = client.query(bigquery_query).to_dataframe()
            df_bigquery = df_bigquery.astype(str)
            df_bigquery.replace('None', '', inplace=True)
            bigquery_record_count = len(df_bigquery)

            sf_data = sf.query_all(salesforce_query)
            salesforce_record_count = sf_data['totalSize']

            if salesforce_record_count == 0:
                test_status = 'FAIL ,SALESFORCE RESTULS EMPTY, TEST SKIPPED'
                reason = 'Salesforce dataframe is empty.'
                total_failed += 1
                log_message = f"Test {test_name} Skipped: {reason}"
                logging.info(log_message)

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

            log_message = f"Raw Salesforce JSON Response for test '{test_name}': {sf_data}"
            logging.info(log_message)

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

            log_message = f"BigQuery columns before index list creation: {df_bigquery.columns}"
            logging.info(log_message)

            log_message = f"Salesforce columns before index list creation: {df_salesforce.columns}"
            logging.info(log_message)

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

            index_mapping = dict(zip(salesforce_index, bigquery_index))
            log_message = f"Index Mapping: {index_mapping}"
            logging.info(log_message)

            log_message = f"BigQuery columns: {df_bigquery.columns}"
            logging.info(log_message)

            log_message = f"Salesforce columns: {df_salesforce.columns}"
            logging.info(log_message)

            index_mapping_inverse = {v: k for k, v in index_mapping.items()}
            df_salesforce.rename(columns=index_mapping_inverse, inplace=True)
            df_bigquery.rename(columns=index_mapping_inverse, inplace=True)

            index_mapping = {k.lower(): v.lower() for k, v in index_mapping.items()}

            merged_df = pd.merge(df_bigquery, df_salesforce, on=list(index_mapping_inverse.values()), how='outer', indicator=True)
            merged_df['_merge'] = merged_df['_merge'].map({'left_only': 'bigquery_only', 'right_only': 'salesforce_only', 'both': 'both'})

            df_bigquery.reset_index(drop=True, inplace=True)
            df_salesforce.reset_index(drop=True, inplace=True)

            temp_cols = [col for col in df_salesforce.columns if col != 'index']

            merged_df = pd.merge(df_bigquery, df_salesforce, on=temp_cols, how='outer', indicator=True)
            merged_df['_merge'] = merged_df['_merge'].map({'left_only': 'bigquery_only', 'right_only': 'salesforce_only', 'both': 'both'})

            total_rows = merged_df.shape[0]
            matching_rows = merged_df[merged_df['_merge'] == 'both'].shape[0]
            non_matching_rows = total_rows - matching_rows

            matching_fields = np.sum(merged_df['_merge'] == 'both')
            total_fields = merged_df.size
            non_matching_fields = total_fields - matching_fields

            summary_df = pd.DataFrame({
                'Total Rows': [total_rows],
                'Matching Rows': [matching_rows],
                'Non-matching Rows': [non_matching_rows],
            })

            summary_file_path = os.path.join(results_dir, f'{test_name}_results.csv')
            summary_df.to_csv(summary_file_path)

            differences_df = merged_df[merged_df['_merge'] != 'both']
            log_message = f"Differences between datasets: {differences_df}"
            logging.info(log_message)

            if df_bigquery.sort_values(by=list(df_bigquery.columns)).reset_index(drop=True).equals(df_salesforce.sort_values(by=list(df_salesforce.columns)).reset_index(drop=True)):
                log_message = f"Test {test_name} Passed: Both BigQuery and Salesforce results match."
                logging.info(log_message)
            else:
                log_message = f"Test {test_name} Failed: BigQuery and Salesforce results do not match."
                logging.info(log_message)
                failed_tests.append(f"Test {test_name} Failed: BigQuery and Salesforce results do not match.")

            total_rows = len(merged_df)
            matching_rows = len(merged_df[merged_df['_merge'] == 'both'])
            non_matching_rows = total_rows - matching_rows
            total_rows1 = bigquery_record_count + salesforce_record_count

            test_status = 'Pass' if non_matching_rows == 0 else 'Fail'

            merged_df.to_csv(os.path.join(results_dir, f'{test_name}_results.csv'), index=True)

            if not df_bigquery.sort_values(by=list(df_bigquery.columns)).reset_index(drop=True).equals(df_salesforce.sort_values(by=list(df_salesforce.columns)).reset_index(drop=True)):
                failed_tests.append(test_name)

            summary_df = pd.DataFrame({
                'Test_Name': [test_name],
                'Test Status': [test_status],
                'Total Rows': [total_rows1],
                'Matching Rows': [matching_rows],
                'Non-matching Rows': [non_matching_rows],
                'BigQuery Record Count': [bigquery_record_count],
                'Ncino Record Count': [salesforce_record_count]
            }, index=[0])

            total_tests += 1
            if test_status == 'Pass':
                total_passed += 1
            else:
                total_failed += 1

            all_results.append(summary_df)

    return total_tests, total_passed, total_failed, all_results, results_dir

def main():
    config_path = "config.yml"
    cfg = load_configuration(config_path)
    setup_logging(cfg.get('logging', False))
    logging.info("Started script execution.")

    sf_config = cfg['salesforce']
    csv_filename = cfg['csv']['filename']
    project_ID = cfg['bigquery']['project_ID']
    dataset1 = cfg['bigquery']['dataset1']

    total_tests = total_passed = total_failed = 0
    all_results = []

    client = bigquery.Client()
    sf = Salesforce(username=sf_config['username'], password=sf_config['password'], consumer_key=sf_config['consumer_key'], consumer_secret=sf_config['consumer_secret'], domain=sf_config['domain'])

    relative_path = os.path.dirname(os.path.abspath(__file__))
    test_cases = load_test_cases(relative_path, csv_filename)

    variables = {
        'project_ID': project_ID,
        'dataset1': dataset1
    }
    logging.info(f"Loaded project_ID: {variables['project_ID']}")

    total_tests, total_passed, total_failed, all_results, results_dir = run_test_cases(test_cases, client, sf, variables, relative_path, total_tests, total_passed, total_failed, all_results)

    all_results_df = pd.concat(all_results)
    summary_stats_df = pd.DataFrame({
        'Test_Name': ['Total Tests', 'Total Passed', 'Total Failed'],
        'Test Status': ['-', '-', '-'],
        'Total Rows': [total_tests, total_passed, total_failed],
        'Matching Rows': [np.nan, np.nan, np.nan],
        'Non-matching Rows': [np.nan, np.nan, np.nan],
        'BigQuery Record Count': [np.nan, np.nan, np.nan],
        'Ncino Record Count': [np.nan, np.nan, np.nan]
    }, index=[total_tests, total_tests+1, total_tests+2])
    all_results_df = pd.concat([all_results_df, summary_stats_df])
    cols = ['Test_Name', 'Test Status', 'Total Rows', 'Matching Rows', 'Non-matching Rows', 'BigQuery Record Count', 'Ncino Record Count']
    all_results_df = all_results_df[cols]
    all_results_df.to_csv(os.path.join(results_dir, f'execution_report_{datetime.now().strftime("%Y%m%d%H%M%S")}.csv'), index=False)

    logging.info("Script execution completed successfully.")

    failed_tests = []
    if failed_tests:
        error_msg = 'Failed tests:\n' + '\n'.join(failed_tests)
        logging.error(error_msg)
        raise Exception(error_msg)

if __name__ == "__main__":
    main()
