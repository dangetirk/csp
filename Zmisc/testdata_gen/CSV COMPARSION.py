import sys
import os
import pandas as pd

def compare_csv_files(file1, file2):
    try:
        df1 = pd.read_csv(file1)
        df2 = pd.read_csv(file2)
        
        common_columns = list(set(df1.columns) & set(df2.columns))
        
        # Identify the differences
        differences = pd.concat([df1[common_columns], df2[common_columns]]).drop_duplicates(keep=False)
        
        if not differences.empty:
            # Create the output file name based on input file names
            file1_name = os.path.splitext(os.path.basename(file1))[0]
            file2_name = os.path.splitext(os.path.basename(file2))[0]
            output_file = f"{file1_name}_vs_{file2_name}_differences.csv"
            
            # Add 'Source' and 'Input_File' columns to differences
            differences['Source'] = ''
            differences.loc[differences.index.isin(df1.index), 'Source'] = 'file1'
            differences.loc[differences.index.isin(df2.index), 'Source'] = 'file2'
            differences['Input_File'] = differences['Source'].apply(lambda x: file1 if x == 'file1' else file2)
            
            differences.to_csv(output_file, index=False)
            print(f"Differences written to {output_file}")
        else:
            print("No differences found between the CSV files.")
    
    except Exception as e:
        print("An error occurred:", str(e))

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py file1.csv file2.csv")
    else:
        file1 = sys.argv[1]
        file2 = sys.argv[2]
        compare_csv_files(file1, file2)
