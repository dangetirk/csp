from google.cloud import bigquery
from google.api_core.exceptions import BadRequest
import csv
import os
import datetime
import logging
import sys


def get_log_directory(source):
    script_directory = os.path.dirname(os.path.abspath(__file__))
    log_directory = os.path.join(script_directory, "Log", source)
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)
    return log_directory

if len(sys.argv) != 3:
    print("Usage: py BQ_Run_Tests.py <Source> <TestCaseFile>")
    sys.exit(1)
source = sys.argv[1]
log_directory = get_log_directory(source)
logging.basicConfig(filename=os.path.join(log_directory, 'script_log.txt'), level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set up logging
logging.basicConfig(filename='script_log.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
log_file_name = datetime.datetime.now().strftime("error_log_%Y%m%d_%H%M%S.csv")

# Initialize a BigQuery client
client = bigquery.Client()

def get_table_name_only(full_table_name):
    """Extract table name from the full table reference."""
    return full_table_name.split('.')[-1]

def initialize_summary():
    """Initialize the summary dictionary to keep track of test results."""
    return {
        'tables': {},
        'test_types': {
            'length': {'executed': 0, 'passed': 0, 'failed': 0},
            'duplicates': {'executed': 0, 'passed': 0, 'failed': 0},
            'nulls': {'executed': 0, 'passed': 0, 'failed': 0},
            'datatype': {'executed': 0, 'passed': 0, 'failed': 0}
        }
    }

test_summary = initialize_summary()
logged_errors = set()  # This will store unique errors
def log_error_to_file(table_name, column, error_msg, test_type):
    """Log unique errors related to tests to a CSV file."""
    table_name = get_table_name_only(table_name)
    if "Unrecognized name:" in error_msg:
        column_name = error_msg.split("Unrecognized name:")[1].split("at")[0].strip()
        error_msg = f"Info: Unrecognized column name '{column_name}'"

    script_directory = os.path.dirname(os.path.abspath(__file__))
    log_directory = os.path.join(script_directory, "Log", source)
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)
    log_file_path = os.path.join(log_directory, log_file_name)
    file_exists = os.path.isfile(log_file_path)

    # Create a unique error string
    error_str = f"{table_name}|{column}|{error_msg}|{test_type}"
    
    # Check if we've already logged this error
    if error_str not in logged_errors:
        logged_errors.add(error_str)  # Add the error to our set
        with open(log_file_path, 'a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(['Table Name', 'Column Name', 'Error Message', 'TestCaseName'])
            writer.writerow([table_name, column, error_msg, test_type])
def update_summary(table_name, test_type, status):
    """Update the test summary with executed, passed, and failed tests."""
    if table_name not in test_summary['tables']:
        test_summary['tables'][table_name] = {'executed': 0, 'passed': 0, 'failed': 0}
    test_summary['tables'][table_name]['executed'] += 1
    test_summary['test_types'][test_type]['executed'] += 1
    
    if status:
        test_summary['tables'][table_name]['passed'] += 1
        test_summary['test_types'][test_type]['passed'] += 1
    else:
        test_summary['tables'][table_name]['failed'] += 1
        test_summary['test_types'][test_type]['failed'] += 1


# Check functions (only showing one for brevity)
def check_length(table_name, column, expected_length):
    query = f"SELECT {column} FROM `{table_name}` WHERE LENGTH({column}) > {expected_length}"
    status = False
    try:
        results = client.query(query).result()
        if results.total_rows == 0:
            status = True
        else:
            for row in results:
                error_msg = f"Value '{row[column]}' in column '{column}' exceeds length {expected_length}."
                log_error_to_file(table_name, column, error_msg, "Length Check")
    except BadRequest as e:
        log_error_to_file(table_name, column, str(e), "Length Check")
    update_summary(table_name, 'length', status)
    log_test_case_result(table_name, column, "Length Check", status) 
    return status

def check_duplicates(table_name, column, primary_key):
    query = f"SELECT {column}, COUNT(*) as cnt FROM `{table_name}` GROUP BY {column} HAVING cnt > 1"
    try:
        results = client.query(query).result()
        for row in results:
            error_msg = f"Value '{row[column]}' in column '{column}' is duplicated {row['cnt']} times."
            log_error_to_file(table_name, column, error_msg, "duplicates")
            update_summary(table_name, 'duplicates', False)  # Update the summary for duplicates check failure
            log_test_case_result(table_name, column, "Duplicates Check", False)
            return False
    except BadRequest as e:
        log_error_to_file(table_name, column, str(e), "duplicates")

    # If the function hasn't returned yet, it means no duplicates were found
    update_summary(table_name, 'duplicates', True)  # Update the summary for duplicates check success
    log_test_case_result(table_name, column, "Duplicates Check", True)
    return True

def check_nulls(table_name, column):
    query = f"SELECT {column} FROM `{table_name}` WHERE {column} IS NULL"
    status = False
    try:
        results = client.query(query).result()
        if results.total_rows == 0:
            status = True
        else:
            for _ in results:
                error_msg = f"Null value found in column '{column}'."
                log_error_to_file(table_name, column, error_msg, "Not Null Check")
    except BadRequest as e:
        log_error_to_file(table_name, column, str(e), "Not Null Check")
    update_summary(table_name, 'nulls', status)
    log_test_case_result(table_name, column, "Not Null Check", status) 
    return status


def check_data_type(database, schema, table, column, expected_data_type):
    # Form the fully qualified table name
    fully_qualified_table_name = f"{database}.{schema}.{table}"
    
    # Retrieve the table schema from BigQuery
    try:
        table = client.get_table(fully_qualified_table_name)
        for field in table.schema:
            if field.name == column:
                actual_data_type = field.field_type.upper()
                if actual_data_type == expected_data_type.upper():
                    status = True
                else:
                    error_msg = f"Expected datatype '{expected_data_type}' but found '{actual_data_type}' for column '{column}'."
                    log_error_to_file(fully_qualified_table_name, column, error_msg, "Datatype Check")
                    status = False
                update_summary(fully_qualified_table_name, 'datatype', status)
                log_test_case_result(fully_qualified_table_name, column, "Datatype Check", status)
                return status
        else:
            error_msg = f"Column '{column}' not found in table '{fully_qualified_table_name}'."
            log_error_to_file(fully_qualified_table_name, column, error_msg, "Datatype Check")
            update_summary(fully_qualified_table_name, 'datatype', False)
            log_test_case_result(fully_qualified_table_name, column, "Datatype Check", False)
            return False
    except BadRequest as e:
        log_error_to_file(fully_qualified_table_name, column, str(e), "Datatype Check")
        update_summary(fully_qualified_table_name, 'datatype', False)
        log_test_case_result(fully_qualified_table_name, column, "Datatype Check", False)
        return False

def print_test_summary():
    """Prints a summary of all the executed tests and writes it to a file in the log directory."""

    script_directory = os.path.dirname(os.path.abspath(__file__))
    log_directory = os.path.join(script_directory, "Log", source)
    summary_file_path = os.path.join(log_directory, 'test_summary_report.csv')

    logging.info("Test Summary Report")

    # Get the unique test names
    unique_test_names = set()
    for table in test_summary['tables']:
        for test_type in test_summary['test_types']:
            unique_test_names.add(test_type.capitalize() + ' Tests')

    # Open the file in write mode
    with open(summary_file_path, 'w') as summary_file:
        header_line = "Table," + ",".join([f"{test_name},Total Tests,Passed,Failed" for test_name in unique_test_names]) + "\n"
        summary_file.write(header_line)
        logging.info("Table-wise and Test Type-wise Summary:")

        for table, results in test_summary['tables'].items():
            summary_line = f"{table}"
            
            for test_type, stats in test_summary['test_types'].items():
                test_name = test_type.capitalize() + ' Tests'
                total_tests = stats['executed']
                passed = stats['passed']
                failed = stats['failed']
                
                summary_line += f",{test_name},{total_tests},{passed},{failed}"

            logging.info(summary_line)
            summary_file.write(summary_line + "\n")
def log_test_case_result(table_name, column, test_type, status):
    """Log the result of a test case to the output file."""
    result = "pass" if status else "fail"
    output_directory = get_log_directory(source)
    output_file_path = os.path.join(output_directory, 'test_case_results.csv')
    file_exists = os.path.isfile(output_file_path)
    
    with open(output_file_path, 'a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Table Name', 'Column Name', 'TestCaseName', 'Result'])
        writer.writerow([table_name, column, test_type, result])

def run_tests_from_csv(testcase_file):
    directory_path = os.path.dirname(testcase_file)
    with open(testcase_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            full_column_details_path = os.path.join(directory_path, row['column_details_file'])
            with open(full_column_details_path, 'r') as detail_csv:
                detail_reader = csv.DictReader(detail_csv)
                for detail in detail_reader:
                    table_name = detail['table_name']
                    column = detail['FieldName']
                    datatype = detail['datatype']
                    length = detail['length']
                    notnull = detail['notnull']
                    primary_key = detail['PrimaryKey'].strip()  # Strip leading and trailing spaces

                    # Split the table name
                    database, schema, table = table_name.split('.')

                    if row['test_type'] == 'length' and length:
                        check_length(table_name, column, int(length))
                    elif row['test_type'] == 'duplicates' and primary_key.lower() == 'yes':
                        # This will check for unique values and no null values
                        check_duplicates(table_name, column, primary_key)  # Call check_duplicates function
                    elif row['test_type'] == 'nulls' and notnull.lower() == 'no':
                        # This will only check if there are null values in the column
                        check_nulls(table_name, column)
                    elif row['test_type'] == 'datatype':
                        check_data_type(database, schema, table, column, datatype)


if __name__ == "__main__":
    test_case_filename = sys.argv[2]
    script_directory = os.path.dirname(os.path.abspath(__file__))
    log_directory = os.path.join(script_directory, "Log", source)
    
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    # Remove the existing output file before running the tests
    output_file_path = os.path.join(get_log_directory(source), 'test_case_results.csv')
    if os.path.exists(output_file_path):
        os.remove(output_file_path)
   
    full_path = os.path.join(script_directory, "TestCase", source, test_case_filename)
    run_tests_from_csv(full_path)
    print_test_summary()