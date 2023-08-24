from simple_salesforce import Salesforce
from google.cloud import bigquery
import csv
import os

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


def execute_bigquery_query(sql_query):
    # Initialize the BigQuery client
    client = bigquery.Client()

    # Execute the SQL query
    query_job = client.query(sql_query)

    # Fetch the results
    results = query_job.result()

    # Print or process the results as needed
    print("BigQuery Query result:")
    for row in results:
        print(row)

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
                    execute_bigquery_query(bigquery_sql_query)
            else:
                print(f"BigQuery SQL file '{bigquery_sql_file}' not found for test case '{tcname}'")
                
            if os.path.exists(salesforce_sql_file):
                print(f"Processing test case '{tcname}' for Salesforce:")
                with open(salesforce_sql_file, 'r') as sf_file:
                    salesforce_sql_query = sf_file.read()
                    output_file = f"{tcname}_salesforce_output.csv"
                    execute_salesforce_query(salesforce_sql_query, output_file)
                    print(f"Output stored in {output_file}")
            else:
                print(f"Salesforce SQL file '{salesforce_sql_file}' not found for test case '{tcname}'")

if __name__ == "__main__":
    input_csv_file = "input.csv"
    process_test_cases(input_csv_file)
