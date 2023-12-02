import pandas as pd
import glob

# Specify the path to the directory containing your CSV files
csv_files_path = '*.csv'

# Use glob to get a list of all CSV files in the specified directory
csv_files = glob.glob(csv_files_path)

# Initialize an empty DataFrame to store the merged data
merged_data = pd.DataFrame()

# Loop through each CSV file and append its data to the merged_data DataFrame
for csv_file in csv_files:
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)
    
    # Append the data to the merged_data DataFrame
    merged_data = merged_data.append(df, ignore_index=True)

# Write the merged data to a new CSV file
merged_data.to_csv('aufile.csv', index=False)
