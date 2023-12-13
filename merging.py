#Merging Datasheet from DiffusionFER with the aufile.csv we created
import pandas as pd

# Opening the csv files
aus_df = pd.read_csv('aufile.csv')
dataset_df = pd.read_csv('dataset_sheet_updated.csv')
dataset_df
# Merging the files  with respect to the file name
merged_df = pd.merge(aus_df, dataset_df, on='file')

# Write the merged data to a new CSV file
merged_df.to_csv('merged.csv', index=False)
