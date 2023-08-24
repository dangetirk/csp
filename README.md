## README.md

### Data Comparison Script

This script is designed to facilitate data comparison between Salesforce and BigQuery data. It reads specific SQL files, executes queries against both platforms, saves the results to CSV files, and then performs a data comparison, generating a summary and detailed report when differences are detected.

---

### Prerequisites:
1. Python (version required for libraries used in the script)
2. Required Python libraries:
   - os
   - pandas
   - csv
   - datetime
   - simple_salesforce
   - google.cloud.bigquery
   - logging
   - configparser
3. Configuration file (`config.ini`) containing settings and authentication information.

---

### Getting Started:
1. **Setup Configuration File**: Ensure that the `config.ini` is properly set up. It should contain paths, log levels, log formats, authentication information for Salesforce, and other necessary configurations.

2. **Input CSV**: The `INPUT_CSV` should contain test cases that the script will process. Each test case should define which SQL files to execute, among other necessary details.

3. **Directory Structure**: Make sure the directory structure mentioned in the `config.ini` exists. This includes the `RESULTS_PATH`, `SOURCE_FOLDER`, `REPORT_FOLDER`, etc.

4. **Salesforce & BigQuery Credentials**: The script uses the `simple_salesforce` library for Salesforce operations and the `google.cloud.bigquery` library for BigQuery operations. Ensure that all required credentials are set up and working.

5. **Logging**: The script generates logs that are saved in the `script.log` file. Logging level and format can be adjusted in the `config.ini` file.

---

### How to Run:
1. Navigate to the directory containing the script.
2. Run the script:
   ```bash
   python script_name.py
   ```

3. Monitor the `script.log` for any issues or logs.
4. Check the `REPORT_FOLDER` (as mentioned in `config.ini`) for generated reports.

---

### Script Functions:
1. **get_next_serial_number**: Fetches the next serial number for the report.
2. **execute_salesforce_query**: Executes a Salesforce query and saves the result to a CSV.
3. **execute_bigquery_query**: Executes a BigQuery query and saves the result to a CSV.
4. **generate_timestamped_folder_name**: Generates a folder name with the current timestamp.
5. **compare_csv_files**: Compares two CSV files.
6. **generate_summary_report**: Generates a summary report after data comparison.
7. **append_to_master_summary**: Appends summary details to a master summary file.
8. **generate_comparison_report**: Generates a comparison report based on detected differences.
9. **process_test_cases**: Processes the test cases from the `INPUT_CSV`.
10. **main**: The main function that drives the script.

---

### Troubleshooting:
- If encountering issues, check `script.log` for any error logs.
- Ensure that the `config.ini` file is correctly set up and paths exist.
- Verify that Salesforce and BigQuery credentials are correct and have the necessary permissions.

---

**Note**: Always keep your `config.ini` file secure and avoid exposing sensitive credentials. Consider using environment variables or secure vaults for storing secrets.
