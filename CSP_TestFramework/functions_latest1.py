import numpy as np
import os
from jinja2 import Template, UndefinedError
import yaml

# Recursively flatten dictionary
def flatten(data, prefix=''):
    """Flatten a dictionary with nested dictionaries."""
    result = {}
    for key, value in data.items():
        new_key = f'{prefix}{key}'
        if isinstance(value, dict):
            result.update(flatten(value, f'{new_key}_'))
        elif value is None and new_key.endswith('__r'):
            result[f'{new_key}_LLC_BI__lookupKey__c'] = None #to handle the specific dictionary types
        else:
            result[new_key] = value
    return result

def handle_nested_dicts(df):
    for column in df.columns:
        if column.startswith('attributes'):   # Ignore attributes fields
            continue
        if isinstance(df[column].iloc[0], dict):
            dict_keys = df[column].iloc[0].keys()
            for key in dict_keys:
                if key == 'attributes':  # Ignore nested attributes fields
                    continue
                df[f'{column}_{key}'] = df[column].apply(lambda x: x[key] if isinstance(x, dict) else np.nan)
            df = df.drop(columns=[column])
    return df


def get_sql_query(query_or_filename, relative_path, variables=None, subfolder=''):
    """
    This function reads the content of a file or a string query, and returns it as a string.
    If variables are provided, it uses them to render a Jinja2 template.
    If subfolder is provided, it changes the directory of SQL files.
    
    :param query_or_filename: The name of the file, or the query string.
    :param relative_path: The path to the directory containing the file.
    :param variables: A dictionary of variables for the Jinja2 template.
    :param subfolder: A string that specifies a subfolder in the 'SQL' directory.
    :return: The content of the file or the query string as a string, or None if the file does not exist.
    """
    query_template = None

    if query_or_filename.endswith('.txt') or query_or_filename.endswith('.sql'):
        try:
            # Determine the file path
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