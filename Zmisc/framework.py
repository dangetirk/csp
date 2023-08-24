# Script - Framework.py
import os
import pandas as pd
import numpy as np
import logging
from datetime import datetime
from google.cloud import bigquery
from simple_salesforce import Salesforce
from functions import flatten, handle_nested_dicts, get_sql_query
import yaml
from test_case_execution import run_test_cases


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


def main():
    # Load configurations
    config_path = "config.yml"
    cfg = load_configuration(config_path)
    setup_logging(cfg.get('logging', False))
    
    logging.info("Started script execution.")
    
    # Access the configurations
    sf_config = cfg['salesforce']
    csv_filename = cfg['csv']['filename']
    project_ID = cfg['bigquery']['project_ID']
    dataset1 = cfg['bigquery']['dataset1']

    # Initialize counters for test summary
    total_tests = total_passed = total_failed = 0
    all_results = []

    # Create BigQuery client and Salesforce connection
    client = bigquery.Client()
    sf = Salesforce(username=sf_config['username'], password=sf_config['password'], consumer_key=sf_config['consumer_key'], consumer_secret=sf_config['consumer_secret'], domain=sf_config['domain'])
    
    relative_path = os.path.dirname(os.path.abspath(__file__))
    test_cases = load_test_cases(relative_path, csv_filename)
    
    # BigQuery variables
    variables = {
        'project_ID': project_ID,
        'dataset1': dataset1
    }
    logging.info(f"Loaded project_ID: {variables['project_ID']}")

    # Call test case execution
    total_tests, total_passed, total_failed, all_results, results_dir = run_test_cases(test_cases, client, sf, variables, relative_path, total_tests, total_passed, total_failed, all_results)

    # Processing results
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
    
    # After all tests have run, raise exceptions for any failed tests at the end
    failed_tests = []  # This should be filled during the execution. For now, it's just a placeholder.
    if failed_tests:
        error_msg = 'Failed tests:\n' + '\n'.join(failed_tests)
        logging.error(error_msg)
        raise Exception(error_msg)


if __name__ == "__main__":
    main()
