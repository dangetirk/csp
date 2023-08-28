

# BigQuery Testing Script

This script is designed to automate the testing of various data quality aspects in Google BigQuery tables. It utilizes the Google Cloud BigQuery Python client library to interact with the BigQuery service. The script is intended to be used as part of a data validation pipeline to ensure that data stored in BigQuery tables meets certain quality standards.

## Features

The script provides the following features:

- **Length Check**: Validates whether string-type column values in a table exceed a specified length.
- **Duplicates Check**: Detects duplicated values in a column, useful for checking primary key violations.
- **Not Null Check**: Identifies null values in columns that are not allowed to have nulls.
- **Datatype Check**: Verifies that the data type of a column matches the expected data type.

## Prerequisites

Before using the script, make sure you have the following:

- Google Cloud Platform account with the BigQuery API enabled.
- Installed the required Python packages using the following command:

  ```bash
  pip install google-cloud-bigquery
  ```

## Usage

1. Ensure you have a properly formatted CSV file containing test cases and their configurations. Each test case entry should include the table name, column name, and relevant test configurations (e.g., expected length, data type).

2. Execute the script by providing two command-line arguments:

   ```bash
   python BQ_Run_Tests.py <Source> <TestCaseFile>
   ```

   - `<Source>`: A unique identifier for the data source being tested.
   - `<TestCaseFile>`: The path to the CSV file containing test case details.

3. The script will generate log files and reports in the `Log/<Source>` directory. These logs will include details about executed tests, their status, and any errors encountered.

4. Review the generated test summary report located in the `Log/<Source>` directory. This report provides an overview of executed tests and their outcomes.

## Example Test Case CSV

The following is an example of how a test case CSV file should be structured:

```csv
column_details_file,test_type
table1_column_details.csv,length
table2_column_details.csv,duplicates
table3_column_details.csv,nulls
table4_column_details.csv,datatype
```

Each entry in the CSV specifies the column details file and the test type to perform.

## Example Column Details CSV

The following is an example of how a column details CSV file should be structured:

```csv
table_name,FieldName,datatype,length,notnull,PrimaryKey
dataset_name.schema_name.table_name,column_name,string,50,no,no
dataset_name.schema_name.table_name,column_name,int64,,yes
```

Each entry in the CSV provides details about a specific column, including its name, data type, expected length (if applicable), nullability, and whether it's a primary key.

