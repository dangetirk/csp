from simple_salesforce import Salesforce
from google.cloud import bigquery
import csv
import os
from deepdiff import DeepDiff

def execute_salesforce_query(sql_query):
    sf = Salesforce(username='ratna-kumar.dangeti@lloydsbanking.com.devpoc', password='Sony@4076', consumer_key='3MVG9od6vNol.eBijuSl01nDrsc_Ngz.DmtOGEn0Ja4DdL75sh_rzjhKqKo0C1DVygt2QyQ1xeGkrwtkfRE1L', consumer_secret= 'FB008DFDC0E87E35543FBD64DB3F5EA2B7AD7789E423138986F0B4F4203C8B03', domain='test')
    result = sf.query_all(sql_query)
    records = result['records']

    return records

def execute_bigquery_query(sql_query):
    client = bigquery.Client()
    query_job = client.query(sql_query)
    results = query_job.result()

    return list(results)

def compare_results(result1, result2):
    # Compare two sets of results using DeepDiff
    diff = DeepDiff(result1, result2)
    return diff

def process_test_cases(csv_file):
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            tcname = row['tcname']
            bigquery_sql_file = row['biqquerysqlfile']
            salesforce_sql_file = row['salesforcesqlfile']
            
            if os.path.exists(bigquery_sql_file):
                print(f"Processing test case '{tcname}' for BigQuery:")
                with open(bigquery_sql_file, 'r') as bq_file:
                    bigquery_sql_query = bq_file.read()
                    bigquery_result = execute_bigquery_query(bigquery_sql_query)
            else:
                print(f"BigQuery SQL file '{bigquery_sql_file}' not found for test case '{tcname}'")
                continue
                
            if os.path.exists(salesforce_sql_file):
                print(f"Processing test case '{tcname}' for Salesforce:")
                with open(salesforce_sql_file, 'r') as sf_file:
                    salesforce_sql_query = sf_file.read()
                    salesforce_result = execute_salesforce_query(salesforce_sql_query)
            else:
                print(f"Salesforce SQL file '{salesforce_sql_file}' not found for test case '{tcname}'")
                continue
            
            # Compare the results
            comparison_result = compare_results(salesforce_result, bigquery_result)
            if not comparison_result:
                print("Results match!")
            else:
                print("Results do not match. Differences:")
                print(comparison_result)

if __name__ == "__main__":
    input_csv_file = "input.csv"
    process_test_cases(input_csv_file)
