import os
import pandas as pd
import csv
from simple_salesforce import Salesforce
from google.cloud import bigquery

def compare_csv_files(file1, file2):
    try:
        df1 = pd.read_csv(file1)
        df2 = pd.read_csv(file2)
        
        common_columns = list(set(df1.columns) & set(df2.columns))
        
        # Identify the differences
        differences = pd.concat([df1[common_columns], df2[common_columns]]).drop_duplicates(keep=False)
        
        return differences
    
    except Exception as e:
        print("An error occurred:", str(e))
        return pd.DataFrame()

def generate_comparison_report(test_case_name, sf_csv, bq_csv):
    comparison_result = compare_csv_files(sf_csv, bq_csv)
    
    if not comparison_result.empty:
        report_file = os.path.join("results", f"{test_case_name}_Comparison_Report.csv")
        comparison_result.to_csv(report_file, index=False)
        print(f"Differences found between {sf_csv} and {bq_csv}. Comparison report saved to {report_file}")
    else:
        print(f"No differences found between {sf_csv} and {bq_csv}.")

def execute_salesforce_query(sql_query, output_file):
    sf = Salesforce(username='ratna-kumar.dangeti@lloydsbanking.com.devpoc', password='Sony@4076', consumer_key='3MVG9od6vNol.eBijuSl01nDrsc_Ngz.DmtOGEn0Ja4DdL75sh_rzjhKqKo0C1DVygt2QyQ1xeGkrwtkfRE1L', consumer_secret= 'FB008DFDC0E87E35543FBD64DB3F5EA2B7AD7789E423138986F0B4F4203C8B03', domain='test')
    result = sf.query_all(sql_query)
    records = result['records']

    with open(output_file, 'w', newline='') as output:
        csv_writer = csv.writer(output)

        # Write header row
        headers = [field for field in records[0].keys() if field != 'attributes']
        csv_writer.writerow(headers)

        # Write data rows
        for record in records:
            csv_writer.writerow([record[field] for field in headers])

def execute_bigquery_query(sql_query, output_file):
    client = bigquery.Client()
    query_job = client.query(sql_query)
    results = query_job.result()

    with open(output_file, 'w', newline='') as output:
        csv_writer = csv.writer(output)

        # Write header row
        headers = [field.name for field in results.schema]
        csv_writer.writerow(headers)

        # Write data rows
        for row in results:
            csv_writer.writerow(row.values())


def process_test_cases(csv_file):
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            tcname = row['tcname']
            bigquery_sql_file = row['biqquerysqlfile']
            salesforce_sql_file = row['salesforcesqlfile']

            if os.path.exists(bigquery_sql_file):
                bq_output_file = os.path.join("results", f"{tcname}_BG.csv")
                with open(bigquery_sql_file, 'r') as bq_file:
                    bigquery_sql_query = bq_file.read()
                    execute_bigquery_query(bigquery_sql_query, bq_output_file)
            else:
                print(f"BigQuery SQL file '{bigquery_sql_file}' not found for test case '{tcname}'")
                continue

            if os.path.exists(salesforce_sql_file):
                sf_output_file = os.path.join("results", f"{tcname}_SF.csv")
                with open(salesforce_sql_file, 'r') as sf_file:
                    salesforce_sql_query = sf_file.read()
                    execute_salesforce_query(salesforce_sql_query, sf_output_file)
            else:
                print(f"Salesforce SQL file '{salesforce_sql_file}' not found for test case '{tcname}'")
                continue

            generate_comparison_report(tcname, sf_output_file, bq_output_file)

if __name__ == "__main__":
    input_csv_file = "input.csv"
    process_test_cases(input_csv_file)
