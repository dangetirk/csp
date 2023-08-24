import pandas as pd

def clean_data(file_path):
    df = pd.read_csv(file_path)

    # Convert 'LLC_BI__lookupKey__c' to string and then strip any whitespace
    df['LLC_BI__lookupKey__c'] = df['LLC_BI__lookupKey__c'].astype(str).str.strip()

    # Round 'LLC_BI__Total_Current_Lien_Amount__c' to 2 decimal places
    df['LLC_BI__Total_Current_Lien_Amount__c'] = df['LLC_BI__Total_Current_Lien_Amount__c'].round(2)

    return df

df_cleaned = clean_data("Collateral_Aggregate_Comparison_Report.csv")

# Filter out the Salesforce and BigQuery records again
sf_record_cleaned = df_cleaned[df_cleaned['_merge'] == 'Salesforce'].iloc[0]
bq_record_cleaned = df_cleaned[df_cleaned['_merge'] == 'BigQuery'].iloc[0]

different_columns_cleaned = []

for col in df_cleaned.columns:
    if sf_record_cleaned[col] != bq_record_cleaned[col] and col != '_merge':
        different_columns_cleaned.append(col)

print("Columns with differences after cleaning:", different_columns_cleaned)
