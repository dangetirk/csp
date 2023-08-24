from google.cloud import bigquery
import pandas as pd

# Create a BigQuery client
client = bigquery.Client()

# Define your query
query = """
    SELECT COUNT(*) FROM `dmn01-rsksoi-bld-01-2017.dmn01_rsksoi_euwe2_rsk_csp_downstream_raw`.rskcsp_ds_account
"""

# Run the query
query_job = client.query(query)

# Wait for the job to complete
df = query_job.to_dataframe()

# Write the results to a CSV file
df.to_csv('query_result.csv', index=False)