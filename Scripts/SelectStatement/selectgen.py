import csv
from collections import defaultdict

def generate_sql_queries(input_file):
    # Using defaultdict to group columns by table names
    tables = defaultdict(list)
    
    with open(input_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            tables[row['Tablename']].append(row['columname'])
    
    # Construct SQL queries for each table
    sql_queries = []
    for table, columns in tables.items():
        query = f"--sql for {table}\n"
        query += "select\n"
        query += "\n,".join(columns)
        query += f"\nFROM {table};\n"
        sql_queries.append(query)
    
    return sql_queries

if __name__ == "__main__":
    input_file = "inputfile.csv"
    output_file = "output_sql_queries.csv"

    queries = generate_sql_queries(input_file)

    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["SQL Query"])
        for query in queries:
            writer.writerow([query])

    print(f"SQL queries written to {output_file}")
